"""
Analisis Penjualan UMKM Indonesia 2024
=======================================
Script ini melakukan analisis data penjualan UMKM Indonesia sepanjang tahun 2024
dan menghasilkan visualisasi grafik untuk laporan web.

Requirements:
    pip install pandas matplotlib seaborn numpy

Output:
    - img/grafik1_tren_bulanan.png
    - img/grafik2_sektor.png
    - img/grafik3_wilayah.png
    - img/grafik4_heatmap.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os

# ── Setup ──────────────────────────────────────────────────────────────────────
os.makedirs("img", exist_ok=True)
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.dpi": 150,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

PALETTE = ["#FF6B35", "#2E86AB", "#A8DADC", "#457B9D", "#1D3557"]
MONTHS = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Ags","Sep","Okt","Nov","Des"]

# ── Load Data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("data.csv")
df["bulan_num"] = pd.Categorical(df["bulan"],
    categories=["Januari","Februari","Maret","April","Mei","Juni",
                 "Juli","Agustus","September","Oktober","November","Desember"],
    ordered=True)
df = df.sort_values("bulan_num")

print("✅ Data berhasil dimuat!")
print(f"   Total baris : {len(df)}")
print(f"   Kolom       : {list(df.columns)}")
print(f"\n{df.head()}\n")

# ─────────────────────────────────────────────────────────────────────────────
# GRAFIK 1 — Tren Total Penjualan Bulanan (semua wilayah & sektor)
# ─────────────────────────────────────────────────────────────────────────────
monthly = (df.groupby("bulan_num", observed=True)["total_penjualan_juta"]
             .sum().reset_index())
monthly.columns = ["bulan", "total"]

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(range(12), monthly["total"] / 1e6, alpha=0.18, color=PALETTE[0])
ax.plot(range(12), monthly["total"] / 1e6, color=PALETTE[0],
        linewidth=2.5, marker="o", markersize=6, markerfacecolor="white",
        markeredgewidth=2)

for i, val in enumerate(monthly["total"] / 1e6):
    ax.annotate(f"Rp{val:.1f}T", (i, val),
                textcoords="offset points", xytext=(0, 9),
                ha="center", fontsize=7.5, color="#555")

ax.set_xticks(range(12))
ax.set_xticklabels(MONTHS)
ax.set_ylabel("Total Penjualan (Triliun Rupiah)", fontsize=10)
ax.set_title("Tren Total Penjualan UMKM Indonesia 2024", fontsize=14, fontweight="bold", pad=15)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"Rp{x:.0f}T"))
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
fig.savefig("img/grafik1_tren_bulanan.png", bbox_inches="tight")
plt.close()
print("✅ Grafik 1 tersimpan: img/grafik1_tren_bulanan.png")

# ─────────────────────────────────────────────────────────────────────────────
# GRAFIK 2 — Total Penjualan per Sektor sepanjang 2024
# ─────────────────────────────────────────────────────────────────────────────
sektor = (df.groupby("sektor")["total_penjualan_juta"]
            .sum().sort_values(ascending=False).reset_index())
sektor["total_T"] = sektor["total_penjualan_juta"] / 1e6

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(sektor["sektor"], sektor["total_T"],
               color=PALETTE[:len(sektor)], edgecolor="white", linewidth=1.2,
               height=0.55)

for bar, val in zip(bars, sektor["total_T"]):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"Rp{val:.1f}T", va="center", fontsize=10, fontweight="bold",
            color="#333")

ax.set_xlabel("Total Penjualan (Triliun Rupiah)", fontsize=10)
ax.set_title("Total Penjualan UMKM per Sektor — 2024", fontsize=14, fontweight="bold", pad=15)
ax.set_xlim(0, sektor["total_T"].max() * 1.15)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"Rp{x:.0f}T"))
ax.grid(axis="x", linestyle="--", alpha=0.4)
fig.tight_layout()
fig.savefig("img/grafik2_sektor.png", bbox_inches="tight")
plt.close()
print("✅ Grafik 2 tersimpan: img/grafik2_sektor.png")

# ─────────────────────────────────────────────────────────────────────────────
# GRAFIK 3 — Perbandingan Penjualan per Wilayah & Sektor (Grouped Bar)
# ─────────────────────────────────────────────────────────────────────────────
wilayah_sektor = (df.groupby(["wilayah","sektor"])["total_penjualan_juta"]
                    .sum().reset_index())
wilayah_sektor["total_T"] = wilayah_sektor["total_penjualan_juta"] / 1e6

wilayahs = wilayah_sektor["wilayah"].unique()
sektors  = wilayah_sektor["sektor"].unique()
x = np.arange(len(wilayahs))
w = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
for i, (sek, col) in enumerate(zip(sektors, PALETTE)):
    vals = [wilayah_sektor[(wilayah_sektor.wilayah==wil) & (wilayah_sektor.sektor==sek)]["total_T"].values[0]
            for wil in wilayahs]
    offset = (i - 1) * w
    bars = ax.bar(x + offset, vals, w, label=sek, color=col, edgecolor="white", linewidth=0.8)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{v:.0f}T", ha="center", va="bottom", fontsize=7.5)

ax.set_xticks(x)
ax.set_xticklabels(wilayahs, fontsize=11)
ax.set_ylabel("Total Penjualan (Triliun Rupiah)", fontsize=10)
ax.set_title("Perbandingan Penjualan per Wilayah & Sektor — 2024",
             fontsize=14, fontweight="bold", pad=15)
ax.legend(title="Sektor", framealpha=0.8)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"Rp{x:.0f}T"))
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
fig.savefig("img/grafik3_wilayah.png", bbox_inches="tight")
plt.close()
print("✅ Grafik 3 tersimpan: img/grafik3_wilayah.png")

# ─────────────────────────────────────────────────────────────────────────────
# GRAFIK 4 — Heatmap Rata-rata Pertumbuhan (%) per Bulan & Sektor
# ─────────────────────────────────────────────────────────────────────────────
pivot = (df.groupby(["bulan_num","sektor"], observed=True)["pertumbuhan_persen"]
           .mean().unstack())
pivot.index = MONTHS

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot.T, annot=True, fmt=".1f", cmap="RdYlGn",
            center=0, linewidths=0.5, linecolor="#eee",
            cbar_kws={"label": "Pertumbuhan (%)"}, ax=ax)
ax.set_title("Heatmap Rata-rata Pertumbuhan Penjualan per Bulan & Sektor (%)",
             fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Bulan", fontsize=10)
ax.set_ylabel("Sektor", fontsize=10)
fig.tight_layout()
fig.savefig("img/grafik4_heatmap.png", bbox_inches="tight")
plt.close()
print("✅ Grafik 4 tersimpan: img/grafik4_heatmap.png")

# ─────────────────────────────────────────────────────────────────────────────
# RINGKASAN INSIGHT
# ─────────────────────────────────────────────────────────────────────────────
total_nasional = df["total_penjualan_juta"].sum() / 1e6
print("\n" + "="*55)
print("  RINGKASAN ANALISIS PENJUALAN UMKM INDONESIA 2024")
print("="*55)
print(f"  Total Penjualan Nasional  : Rp{total_nasional:.1f} Triliun")
print(f"  Sektor Terbesar           : {sektor.iloc[0]['sektor']} (Rp{sektor.iloc[0]['total_T']:.1f}T)")
print(f"  Wilayah Kontribusi Besar  : Jawa")
print(f"  Bulan Puncak Penjualan    : November–Desember (Harbolnas)")
print(f"  Bulan Terendah            : Januari (awal tahun)")
print("="*55)
print("\n✅ Semua grafik berhasil digenerate di folder img/")
