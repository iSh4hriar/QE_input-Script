import numpy as np
import matplotlib.pyplot as plt

# ১. ফাইল নাম সেট করুন (আপনার prefix অনুযায়ী পরিবর্তন করুন)
epsr_file = "epsr_your_prefix.dat"
epsi_file = "epsi_your_prefix.dat"

# ২. ডেটা লোড করা 
data_r = np.loadtxt(epsr_file, comments=['#', '@'])
data_i = np.loadtxt(epsi_file, comments=['#', '@'])

# এনার্জি (eV) প্রথম কলামে থাকে
energy = data_r[:, 0]

# X-ডিরেকশনের ডেটা নেওয়া হলো (কিউবিক/আইসোট্রপিক সিস্টেমের জন্য)
eps1 = data_r[:, 1]  # Real part (\varepsilon_1)
eps2 = data_i[:, 1]  # Imaginary part (\varepsilon_2)

# ৩. পেপারের Equation (27) অনুযায়ী Absorption Coefficient (\alpha) হিসাব করা
# eV থেকে cm^-1 এ নেওয়ার জন্য কনভার্সন ফ্যাক্টর (2 / (\hbar * c)) \approx 101354
conversion_factor_alpha = 101354.35
alpha = conversion_factor_alpha * energy * np.sqrt(0.5 * (np.sqrt(eps1**2 + eps2**2) - eps1))

# ৪. পেপারের Equation (28) অনুযায়ী Optical Conductivity-র Real part (\sigma) হিসাব করা
optical_cond = energy * eps2  # রিলেটিভ ট্রেন্ড বা ট্রেন্ডলাইন দেখার জন্য

# ৫. গ্রাফ প্লট করা
plt.figure(figsize=(12, 10))

# গ্রাফ ১: Dielectric Function (\varepsilon_1 এবং \varepsilon_2)
plt.subplot(2, 2, 1)
plt.plot(energy, eps1, label=r'$\varepsilon_1$ (Real)', color='blue')
plt.plot(energy, eps2, label=r'$\varepsilon_2$ (Imaginary)', color='red')
plt.xlabel('Energy (eV)')
plt.ylabel('Dielectric Function')
plt.title('Dielectric Function vs Energy')
plt.legend()
plt.grid(True)

# গ্রাফ ২: Absorption Coefficient (\alpha)
plt.subplot(2, 2, 2)
plt.plot(energy, alpha / 1e5, color='green')  # 10^5 এককে দেখানোর জন্য
plt.xlabel('Energy (eV)')
plt.ylabel(r'Absorption Coefficient $\alpha$ ($\times 10^5$ cm$^{-1}$)')
plt.title('Absorption Coefficient vs Energy')
plt.grid(True)

# গ্রাফ ৩: Optical Conductivity (\sigma)
plt.subplot(2, 2, 3)
plt.plot(energy, optical_cond, color='purple')
plt.xlabel('Energy (eV)')
plt.ylabel('Optical Conductivity (arb. units)')
plt.title('Optical Conductivity vs Energy')
plt.grid(True)

plt.tight_layout()
plt.savefig('optical_properties.png', dpi=300)
plt.show()

# ৬. ডেটাগুলো নতুন ফাইলে সেভ করা (যাতে ওরিজিন প্রো-তে প্লট করতে পারেন)
np.savetxt('calculated_optical_properties.dat', 
           np.column_stack((energy, eps1, eps2, alpha, optical_cond)),
           header='Energy(eV)   Eps1   Eps2   Absorption(cm^-1)   Optical_Cond(arb.units)',
           fmt='%.6f')

print("সফলভাবে সবগুলো অপটিক্যাল প্রোপার্টি হিসাব করা হয়েছে এবং 'calculated_optical_properties.dat' ফাইলে সেভ করা হয়েছে!")
