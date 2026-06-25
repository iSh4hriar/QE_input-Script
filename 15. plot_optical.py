import numpy as np
import matplotlib.pyplot as plt

# ১. ফাইল নাম সেট করুন (আপনার prefix অনুযায়ী পরিবর্তন করুন)
epsr_file = "epsr_your_prefix.dat"
epsi_file = "epsi_your_prefix.dat"

# ২. ডেটা লোড করা 
data_r = np.loadtxt(epsr_file, comments=['#', '@'])
data_i = np.loadtxt(epsi_file, comments=['#', '@'])

# প্রথম কলামে থাকে ফোটন এনার্জি (eV)
energy = data_r[:, 0]

# ৩. টেট্রাগোনাল ও কিউবিক উভয় সিস্টেমের জন্য ৩টি অক্ষের গড় (Average) নেওয়া হলো
eps1 = (data_r[:, 1] + data_r[:, 2] + data_r[:, 3]) / 3.0  # \varepsilon_1 (Real)
eps2 = (data_i[:, 1] + data_i[:, 2] + data_i[:, 3]) / 3.0  # \varepsilon_2 (Imaginary)

# ৪. পেপারের সূত্র অনুযায়ী Absorption Coefficient (\alpha) হিসাব করা
conversion_factor_alpha = 101354.35
alpha = conversion_factor_alpha * energy * np.sqrt(0.5 * (np.sqrt(eps1**2 + eps2**2) - eps1))

# ৫. Optical Conductivity (\sigma)-র ট্রেন্ড হিসাব করা
optical_cond = energy * eps2 

# ৬. ৪টি আলাদা গ্রাফ (2x2 Grid) প্লট করা
fig, axs = plt.subplots(2, 2, figsize=(13, 11))

# গ্রাফ (a): Real Dielectric Function
axs[0, 0].plot(energy, eps1, color='blue', linewidth=1.8)
axs[0, 0].set_xlabel('Energy (eV)', fontsize=11)
axs[0, 0].set_ylabel('Real Dielectric Function $\epsilon_1$', fontsize=11)
axs[0, 0].set_title('(a) Real Dielectric Function', fontsize=12, fontweight='bold')
axs[0, 0].grid(True, linestyle='--', alpha=0.6)
axs[0, 0].set_xlim(0, 20)

# গ্রাফ (b): Imaginary Dielectric Function
axs[0, 1].plot(energy, eps2, color='red', linewidth=1.8)
axs[0, 1].set_xlabel('Energy (eV)', fontsize=11)
axs[0, 1].set_ylabel('Imaginary Dielectric Function $\epsilon_2$', fontsize=11)
axs[0, 1].set_title('(b) Imaginary Dielectric Function', fontsize=12, fontweight='bold')
axs[0, 1].grid(True, linestyle='--', alpha=0.6)
axs[0, 1].set_xlim(0, 20)

# গ্রাফ (c): Absorption Coefficient
axs[1, 0].plot(energy, alpha / 1e5, color='green', linewidth=1.8)
axs[1, 0].set_xlabel('Energy (eV)', fontsize=11)
axs[1, 0].set_ylabel('Absorption Coefficient $\\alpha$ ($\\times 10^5$ cm$^{-1}$)', fontsize=11)
axs[1, 0].set_title('(c) Absorption Coefficient', fontsize=12, fontweight='bold')
axs[1, 0].grid(True, linestyle='--', alpha=0.6)
axs[1, 0].set_xlim(0, 20)

# গ্রাফ (d): Optical Conductivity
axs[1, 1].plot(energy, optical_cond, color='purple', linewidth=1.8)
axs[1, 1].set_xlabel('Energy (eV)', fontsize=11)
axs[1, 1].set_ylabel('Optical Conductivity (arb. units)', fontsize=11)
axs[1, 1].set_title('(d) Optical Conductivity', fontsize=12, fontweight='bold')
axs[1, 1].grid(True, linestyle='--', alpha=0.6)
axs[1, 1].set_xlim(0, 20)

plt.tight_layout()
plt.savefig('optical_properties_fixed.png', dpi=300)
plt.show()

# ওরিজিনের জন্য ডেটা সেভ করা
np.savetxt('calculated_optical_properties.dat', 
           np.column_stack((energy, eps1, eps2, alpha, optical_cond)),
           header='Energy(eV)   Eps1_Avg   Eps2_Avg   Absorption(cm^-1)   Optical_Cond(arb.units)',
           fmt='%.6f')
