import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# ১. আপনার নিজস্ব টেট্রাগোনাল সিস্টেম সেটআপ (এগুলো পরিবর্তন করুন)
# =====================================================================
PREFIX = "tetra_material"
PSEUDO_DIR = "/path/to/your/pseudos/"  # সিউডোপোটেনশিয়াল ফোল্ডারের পাথ
NCPUS = 4                              # প্রসেসর কোর সংখ্যা

# vc-relax থেকে পাওয়া টেট্রাগোনাল রিল্যাক্সড ল্যাটিস ম্যাট্রিক্স (Angstrom ইউনিটে)
# মনে রাখবেন: টেট্রাগোনালে ১ম ও ২য় লাইনের মান সমান (a=b) হলেও ৩য় লাইনের মান ভিন্ন (c) হবে
CELL_BASE = np.array([
    [4.0000, 0.0000, 0.0000],  # a
    [0.0000, 4.0000, 0.0000],  # b
    [0.0000, 0.0000, 6.5000]   # c (এই z-অক্ষ বরাবরই স্ট্রেন অ্যাপ্লাই হবে)
])

# রিল্যাক্সড অ্যাটমিক পজিশনস (vc-relax আউটপুট থেকে হুবহু কপি করুন)
ATOMIC_POSITIONS_STR = """
Ti  0.000000000  0.000000000  0.000000000
O   0.500000000  0.500000000  0.000000000
"""

# =====================================================================
# ২. স্ট্রেন রেঞ্জ এবং ইনিশিয়াল সেটআপ
# =====================================================================
# -২% থেকে +২% পর্যন্ত ৫টি পয়েন্টে স্ট্রেন দেওয়া হচ্ছে
strains = np.array([-0.02, -0.01, 0.00, 0.01, 0.02])
energies = []

# টেট্রাগোনাল রিল্যাক্সড সেলের ভলিউম হিসাব (V0 = a * b * c)
V0 = np.dot(CELL_BASE[0], np.cross(CELL_BASE[1], CELL_BASE[2]))
print(f"Relaxed Tetragonal Volume (V0): {V0:.4f} Angstrom^3")

# =====================================================================
# ৩. লুপ চালিয়ে Tetragonal Z-Uniaxial Strain অ্যাপ্লাই ও QE রান করা
# =====================================================================
for delta in strains:
    print(f"Running simulation for Tetragonal Uniaxial strain (C33) delta = {delta}...")
    
    # টেট্রাগোনাল C33 এর জন্য সঠিক Uniaxial Strain Matrix (শুধুমাত্র z-অক্ষে পরিবর্তন)
    strain_matrix = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0 + delta]
    ])
    
    # নতুন স্ট্রেনড সেল তৈরি
    strained_cell = np.dot(CELL_BASE, strain_matrix)
    
    # QE ইনপুট টেক্সট জেনারেট করা
    input_data = f"""&CONTROL
    calculation = 'scf'
    prefix = '{PREFIX}'
    outdir = './tmp/'
    pseudo_dir = '{PSEUDO_DIR}'
/
&SYSTEM
    ibrav = 0, nat = 2, ntyp = 2,
    ecutwfc = 50.0,
/
&ELECTRONS
    conv_thr = 1.0d-8
/
ATOMIC_SPECIES
   Ti  47.867   Ti.pbe-spn-kjpaw_psl.1.0.0.UPF
   O   15.999   O.pbe-n-kjpaw_psl.1.0.0.UPF

CELL_PARAMETERS (angstrom)
  {strained_cell[0][0]:.8f}  {strained_cell[0][1]:.8f}  {strained_cell[0][2]:.8f}
  {strained_cell[1][0]:.8f}  {strained_cell[1][1]:.8f}  {strained_cell[1][2]:.8f}
  {strained_cell[2][0]:.8f}  {strained_cell[2][1]:.8f}  {strained_cell[2][2]:.8f}

ATOMIC_POSITIONS (crystal)
{ATOMIC_POSITIONS_STR.strip()}

K_POINTS (automatic)
  6 6 4 0 0 0
"""
    
    in_filename = f"scf_tetra_c33_{delta}.in"
    out_filename = f"scf_tetra_c33_{delta}.out"
    with open(in_filename, "w") as f:
        f.write(input_data)
        
    # গ্লোবাল pw.x রান করা
    cmd = f"mpirun -np {NCPUS} pw.x < {in_filename} > {out_filename}"
    subprocess.run(cmd, shell=True)
    
    # আউটপুট থেকে টোটাল এনার্জি এক্সট্রাক্ট করা (Ry ইউনিটে)
    energy = None
    with open(out_filename, "r") as f:
        for line in f:
            if "!" in line:
                energy = float(line.split()[4])
                break
    
    if energy is not None:
        energies.append(energy)
        print(f"Energy: {energy} Ry")
    else:
        print(f"Error: Energy not found for strain {delta}!")
        exit(1)

# =====================================================================
# ৪. ডাটা ফিটিং এবং C33 ক্যালকুলেশন সূত্র
# =====================================================================
energies = np.array(energies)
delta_E = energies - min(energies)

# ২য় ঘাতের পলিনমিয়াল ফিটিং (y = Ax^2 + Bx + C)
coef = np.polyfit(strains, delta_E, 2)
A = coef[0] 

# Ry/Angstrom^3 থেকে GPa কনভার্সন ফ্যাক্টর
ry_to_gpa = 14710.516

# টেট্রাগোনাল Z-Uniaxial এর ক্ষেত্রে শক্তির সূত্র: Delta_E = 0.5 * V0 * C33 * delta^2
# তাই, C33 = (2 * A / V0) * ry_to_gpa
C33 = (2 * A / V0) * ry_to_gpa

print("\n================ RESULT ================")
print(f"Calculated Tetragonal C33 Elastic Constant: {C33:.2f} GPa")
print("========================================")

# =====================================================================
# ৫. গ্রাফ প্লট এবং ইমেজ ফাইল হিসেবে সেভ করা
# =====================================================================
plt.plot(strains, delta_E, 'ko', label='DFT Data (Z-Uniaxial Strain)')
fit_strains = np.linspace(min(strains), max(strains), 100)
plt.plot(fit_strains, np.polyval(coef, fit_strains), 'r-', label='Quadratic Fit')
plt.xlabel('Uniaxial Strain ($\delta$)')
plt.ylabel('$\Delta$E (Ry)')
plt.title(f'Tetragonal $C_{{33}}$ Fit ($C_{{33}}$ = {C33:.2f} GPa)')
plt.legend()
plt.grid(True)
plt.savefig('Tetragonal_C33_fit_plot.png')
print("Graph saved as 'Tetragonal_C33_fit_plot.png'")
plt.show()
