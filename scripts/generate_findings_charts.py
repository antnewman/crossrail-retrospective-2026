"""Generate three publication-quality charts for the Crossrail findings article.

Outputs six files (three PNGs at 300dpi and three SVGs) to outputs/.

British English throughout. Neutral colour palette. Clean minimal style.
"""

import os
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)

# ------------------------------ Shared style ------------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "normal",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#333333",
    "axes.linewidth": 0.8,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
})

C_DARK = "#2b2b2b"
C_MID = "#6c6c6c"
C_LIGHT = "#b0b0b0"
C_REF = "#404040"
C_BAND_LIGHT = "#f2f2f2"
C_BAND_MED = "#e4e4e4"


def save_both(fig, basename):
    png = f"outputs/{basename}.png"
    svg = f"outputs/{basename}.svg"
    fig.savefig(png, dpi=300)
    fig.savefig(svg)
    print(f"Saved: {png}")
    print(f"Saved: {svg}")
    plt.close(fig)


# ----------------------- Chart 1: Headline comparison -----------------------
fig, axes = plt.subplots(3, 1, figsize=(8, 6.4), constrained_layout=True)
fig.suptitle("2011 forecast vs 2024/25 outturn: three headline assumptions",
             fontsize=12, y=1.01)

# Cost
ax = axes[0]
labels = ["2011 forecast", "2024/25 outturn (cash)"]
vals = [14.8, 18.8]
bars = ax.barh(labels, vals, color=[C_MID, C_DARK], height=0.55)
# Forecast label (simple)
ax.text(vals[0] + 0.3, bars[0].get_y() + bars[0].get_height() / 2, f"£{vals[0]}bn",
        va="center", ha="left", fontsize=10, color=C_DARK)
# Outturn label with real-terms range inline
ax.text(vals[1] + 0.3, bars[1].get_y() + bars[1].get_height() / 2,
        f"£{vals[1]}bn  ·  real-terms £17.3-17.4bn",
        va="center", ha="left", fontsize=10, color=C_DARK)
ax.set_xlim(0, 32)
ax.set_xlabel("£ billion")
ax.set_title("Cost", loc="left", pad=6, fontsize=10.5, color=C_DARK)
ax.invert_yaxis()

# Demand
ax = axes[1]
labels = ["2011 forecast", "2024/25 outturn"]
vals = [200, 243]
bars = ax.barh(labels, vals, color=[C_MID, C_DARK], height=0.55)
for b, v in zip(bars, vals):
    ax.text(v + 3, b.get_y() + b.get_height() / 2, f"{v}m",
            va="center", ha="left", fontsize=10, color=C_DARK)
ax.set_xlim(0, 290)
ax.set_xlabel("Million annual journeys")
ax.set_title("Demand", loc="left", pad=6, fontsize=10.5, color=C_DARK)
ax.invert_yaxis()

# BCR
ax = axes[2]
labels = ["2011 forecast", "2024/25 restated"]
point_vals = [1.97, 1.97]
errs_lo = [0, 1.97 - 1.88]
errs_hi = [0, 2.06 - 1.97]
ax.barh(labels, point_vals, color=[C_MID, C_DARK], height=0.55,
        xerr=[errs_lo, errs_hi],
        error_kw={"ecolor": C_DARK, "elinewidth": 1.0, "capsize": 4})
ax.text(1.97 + 0.03, 0, "1.97", va="center", fontsize=10, color=C_DARK)
ax.text(2.06 + 0.03, 1, "1.88-2.06", va="center", fontsize=10, color=C_DARK)
ax.set_xlim(0, 2.5)
ax.set_xlabel("Benefit-cost ratio")
ax.set_title("BCR", loc="left", pad=6, fontsize=10.5, color=C_DARK)
ax.invert_yaxis()

save_both(fig, "chart_1_headline_comparison")


# -------------------- Chart 2: Cost overrun decomposition --------------------
fig, ax = plt.subplots(figsize=(9, 4.4), constrained_layout=True)
fig.suptitle("Crossrail cost overrun decomposition: real-terms vs construction inflation",
             fontsize=12, y=1.02)

baseline = 14.8
outturn = 18.8
y_pos = [0, 1]
labels = ["Lower bound\n(real £2.5bn)", "Upper bound\n(real £3.7bn)"]
real_vals = [2.5, 3.7]
infl_vals = [1.5, 0.3]

ax.barh(y_pos, real_vals, left=baseline, color=C_DARK, height=0.45,
        label="Real-terms component")
ax.barh(y_pos, infl_vals,
        left=[baseline + r for r in real_vals],
        color=C_LIGHT, height=0.45,
        label="Construction inflation component")

ax.axvline(baseline, color=C_REF, linewidth=0.8, alpha=0.9)
ax.axvline(outturn, color=C_REF, linewidth=0.8, alpha=0.9)

ax.text(baseline, 1.75, "2010-11 baseline\n£14.8bn",
        ha="center", va="bottom", fontsize=9, color=C_REF)
ax.text(outturn, 1.75, "2024/25 cash outturn\n£18.8bn",
        ha="center", va="bottom", fontsize=9, color=C_REF)

ax.text(baseline + 3.7 / 2, 1, "£3.7bn real-terms",
        ha="center", va="center", fontsize=9, color="white")
ax.text(baseline + 3.7 + 0.3 / 2, 1, "£0.3bn",
        ha="center", va="center", fontsize=8, color=C_DARK)
ax.text(baseline + 2.5 / 2, 0, "£2.5bn real-terms",
        ha="center", va="center", fontsize=9, color="white")
ax.text(baseline + 2.5 + 1.5 / 2, 0, "£1.5bn inflation",
        ha="center", va="center", fontsize=9, color=C_DARK)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=10)
ax.set_xlim(14.2, 19.1)
ax.set_ylim(-0.6, 2.3)
ax.set_xlabel("£ billion")

ax.legend(loc="lower right", frameon=False, fontsize=9)

save_both(fig, "chart_2_cost_overrun_decomposition")


# ------------------------- Chart 3: BCR restatement -------------------------
fig, ax = plt.subplots(figsize=(8, 5.2), constrained_layout=True)
fig.suptitle("BCR restatement under three cost-treatment scenarios",
             fontsize=12, y=1.02)

scenarios = ["Nominal cost",
             "Real cost\n(no pre-2014\ncorrection)",
             "Real cost\n(7.5% pre-2014\ncorrection)"]
bcrs = [1.88, 1.92, 2.06]
x_pos = [0, 1, 2]

ax.axhspan(1.5, 2.0, facecolor=C_BAND_LIGHT, alpha=1.0, zorder=0)
ax.axhspan(2.0, 4.0, facecolor=C_BAND_MED, alpha=1.0, zorder=0)

ax.axhline(1.97, color=C_REF, linewidth=0.8, linestyle="--", alpha=0.9, zorder=2)
ax.axhline(2.0, color=C_REF, linewidth=1.0, linestyle="-", alpha=0.9, zorder=2)

ax.text(-0.44, 1.965, "2011 baseline 1.97",
        ha="left", va="top", fontsize=9, color=C_REF)
ax.text(-0.44, 2.005, "Band boundary 2.0",
        ha="left", va="bottom", fontsize=9, color=C_REF)

ax.text(2.42, 1.75, "Medium VFM\nband (1.5-2.0)",
        ha="left", va="center", fontsize=9, color=C_MID)
ax.text(2.42, 2.10, "High VFM\nband (2.0-4.0)",
        ha="left", va="center", fontsize=9, color=C_MID)

ax.scatter(x_pos, bcrs, color=C_DARK, s=70, zorder=5)
for x, y in zip(x_pos, bcrs):
    ax.annotate(f"{y}", xy=(x, y), xytext=(0, 10),
                textcoords="offset points", ha="center",
                fontsize=10, color=C_DARK)

ax.text(1.0, 1.73,
        "Band change in one of three scenarios;\n"
        "sensitivity-dependent at 4.3% pre-2014 correction threshold",
        ha="center", va="top", fontsize=9, color=C_MID, style="italic")

ax.set_xticks(x_pos)
ax.set_xticklabels(scenarios, fontsize=9.5)
ax.set_xlim(-0.5, 3.2)
ax.set_ylim(1.7, 2.2)
ax.set_ylabel("Benefit-cost ratio")

save_both(fig, "chart_3_bcr_restatement")


# ------------- Chart 4: Revenue shortfall waterfall -------------
fig, ax = plt.subplots(figsize=(9.5, 5.5), constrained_layout=True)
fig.suptitle("Revenue shortfall decomposition: 2019 forecast to 2024/25 outturn",
             fontsize=12, y=1.02)

# Running totals (£m)
forecast = 1037
after_demand = forecast - 128  # 909
after_yield = after_demand - 293  # 616
outturn = after_yield + 36  # 652

x_pos = [0, 1, 2, 3, 4]
x_labels = ["2019\nforecast", "Demand\neffect", "Yield\neffect", "Interaction", "2024/25\noutturn"]

# Bar geometry: (bottom, height) per bar
#   Grounded bars (forecast and outturn): bottom=0, height=value
#   Floating bars (effects): bottom=lower edge of segment, height=magnitude
bottoms = [0, after_demand, after_yield, after_yield, 0]
heights = [forecast, 128, 293, 36, outturn]
colours = [C_DARK, C_MID, C_MID, C_LIGHT, C_DARK]

ax.bar(x_pos, heights, bottom=bottoms, color=colours, width=0.62)

# Value labels above each bar
value_texts = [f"£{forecast:,}m", "−£128m", "−£293m", "+£36m", f"£{outturn:,}m"]
for xi, btm, h, txt in zip(x_pos, bottoms, heights, value_texts):
    ax.text(xi, btm + h + 18, txt, ha="center", va="bottom",
            fontsize=10, color=C_DARK)

# Dashed connectors between consecutive bars (at running-total levels)
# Bar 0 top (forecast=1037) --> Bar 1 top (after_demand + 128 = 1037)
# Bar 1 bottom (after_demand = 909) --> Bar 2 top (after_demand = 909)
# Bar 2 bottom (after_yield = 616) --> Bar 3 bottom (after_yield = 616)
# Bar 3 top (after_yield + 36 = 652) --> Bar 4 top (outturn = 652)
connectors = [
    ((0 + 0.31, 1 - 0.31), forecast),
    ((1 + 0.31, 2 - 0.31), after_demand),
    ((2 + 0.31, 3 - 0.31), after_yield),
    ((3 + 0.31, 4 - 0.31), outturn),
]
for (x_start, x_end), y in connectors:
    ax.plot([x_start, x_end], [y, y], color=C_REF,
            linewidth=0.7, linestyle="--", alpha=0.55)

ax.set_xticks(x_pos)
ax.set_xticklabels(x_labels, fontsize=10)
ax.set_ylabel("£ million")
ax.set_ylim(0, 1150)
ax.set_xlim(-0.6, 4.6)

# Footnote with the arithmetic reconciliation
fig.text(0.5, -0.02,
         "Decomposition reconciles multiplicatively: demand ratio 0.877 × yield ratio 0.717 = 0.629  "
         "(= 1 − 0.371 revenue drift)",
         ha="center", va="top", fontsize=9, color=C_MID, style="italic")

save_both(fig, "chart_4_revenue_shortfall_decomposition")


# ------------------------ List outputs ------------------------
print()
print("=== outputs directory ===")
for f in sorted(os.listdir("outputs")):
    size = os.path.getsize(os.path.join("outputs", f))
    print(f"  {f}  ({size:,} bytes)")
