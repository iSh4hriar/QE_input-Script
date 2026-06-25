import numpy as np
import matplotlib.pyplot as plt

# ১. ফাইল নাম সেট করুন (আপনার prefix অনুযায়ী পরিবর্তন করুন)
epsr_file = "epsr_your_prefix.dat"
epsi_file = "epsi_your_prefix.dat"

# ২. ডেটা লোড করা 
data_r = np.loadtxt(epsr_file, comments=['#', '@'])
data_i = np.loadtxt(epsi_file, comments=['#', '@'])

# প্রথম কলামে থাকে ফোটন এনার্জি (eV)
energy = data_r[:, 0]

# ৩. ৩টি অক্ষের গড় (Average) নেওয়া হলো
eps1 = (data_r[:, 1] + data_r[:, 2] + data_r[:, 3]) / 3.0  # Real part
eps2 = (data_i[:, 1] + data_i[:, 2] + data_i[:, 3]) / 3.0  # Imaginary part

# ৪. বাকি ৪টি অপটিক্যাল প্রোপার্টিজ গণনা (পেপারের গ্রাফের জন্য)
n = np.sqrt((np.sqrt(eps1**2 + eps2**2) + eps1) / 2.0)     # Refractive Index
k = np.sqrt((np.sqrt(eps1**2 + eps2**2) - eps1) / 2.0)     # Extinction Coefficient
R = ((n - 1)**2 + k**2) / ((n + 1)**2 + k**2)             # Reflectivity
L = eps2 / (eps1**2 + eps2**2)                             # Energy Loss Function

# ৫. পেপারের স্টাইলে ৪টি আলাদা গ্রাফ (2x2 Grid) প্লট করা
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# গ্রাফ (a): Reflectivity (R)
axs[0, 0].plot(energy, R, color='black', linewidth=1.8)
axs[0, 0].set_xlabel('Energy (eV)', fontsize=11)
axs[0, 0].set_ylabel('Reflectivity, $R$', fontsize=11)
axs[0, 0].set_title('(a) Reflectivity', fontsize=12, fontweight='bold')
axs[0, 0].grid(True, linestyle='--', alpha=0.5)
axs[0, 0].set_xlim(0, 20)
axs[0, 0].set_ylim(0, 0.20) # পেপারের স্কেল অনুযায়ী অ্যাডজাস্ট করা

# গ্রাফ (b): Energy Loss Function (L)
axs[0, 1].plot(energy, L, color='red', linewidth=1.8)
axs[0, 1].set_xlabel('Energy (eV)', fontsize=11)
axs[0, 1].set_ylabel('Energy Loss Function, $L$', fontsize=11)
axs[0, 1].set_title('(b) Energy Loss Function', fontsize=12, fontweight='bold')
axs[0, 1].grid(True, linestyle='--', alpha=0.5)
axs[0, 1].set_xlim(0, 20)

# গ্রাফ (c): Refractive Index (n)
axs[1, 0].plot(energy, n, color='blue', linewidth=1.8)
axs[1, 0].set_xlabel('Energy (eV)', fontsize=11)
axs[1, 0].set_ylabel('Refractive Index, $n$', fontsize=11)
axs[1, 0].set_title('(c) Refractive Index', fontsize=12, fontweight='bold')
axs[1, 0].grid(True, linestyle='--', alpha=0.5)
axs[1, 0].set_xlim(0, 20)

# গ্রাফ (d): Extinction Coefficient (k)
axs[1, 1].plot(energy, k, color='green', linewidth=1.8)
axs[1, 1].set_xlabel('Energy (eV)', fontsize=11)
axs[1, 1].set_ylabel('Extinction Coefficient, $k$', fontsize=11)
axs[1, 1].set_title('(d) Extinction Coefficient', fontsize=12, fontweight='bold')
axs[1, 1].grid(True, linestyle='--', alpha=0.5)
axs[1, 1].set_xlim(0, 20)

plt.tight_layout()
plt.savefig('paper_optical_properties.png', dpi=300)
plt.show()

# ৬. ওরিজিন (OriginPro) বা অন্যান্য সফটওয়্যারে প্লট করার জন্য সব ডেটা একসাথে সেভ করা
# এখানে আগের ডেটাসহ মোট ৮টি কলাম সেভ হবে
absorption = 101354.35 * energy * np.sqrt(0.5 * (np.sqrt(eps1**2 + eps2**2) - eps1))
optical_cond = energy * eps2 

np.savetxt('all_optical_properties.dat', 
           np.column_stack((energy, eps1, eps2, R, L, n, k, absorption, optical_cond)),
           header='Energy(eV) Eps1_Avg Eps2_Avg Reflectivity(R) Loss_Function(L) Refractive_Index(n) Extinction_Coeff(k) Absorption(cm^-1) Opt_Cond',
           fmt='%.6f')
