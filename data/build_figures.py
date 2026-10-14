"""Market figures for the Stamp commercial business plan.

Figures are branded strictly following Stamp's visual identity:
- Exact Manrope typography matching the document:
  - Manrope-Bold (700) for titles, data callouts, and key metrics
  - Manrope-Semi (600) for axis labels and category names
  - Manrope-Medium (500) for tick marks and legends
- Figure backgrounds match the document container color (#EEF2F6) exactly.
- High-contrast Stamp brand colors:
  Deep Night Ink (#240340), Deep Solid Purple (#3B0764), Electric Lavender (#E24BFF),
  Wild Raspberry (#FF467A), Roasted Peanut (#FF8C30), Electric Butter (#FFD640)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "figures"
DATA = Path(__file__).resolve().parent / "sales-clean.csv"
FONT_DIR = Path(__file__).resolve().parent.parent / "brand" / "fonts"

# Exact font properties matching the document typography
F_BOLD = fm.FontProperties(fname=str(FONT_DIR / "Manrope-700.ttf"))
F_SEMI = fm.FontProperties(fname=str(FONT_DIR / "Manrope-600.ttf"))
F_MED = fm.FontProperties(fname=str(FONT_DIR / "Manrope-500.ttf"))
F_REG = fm.FontProperties(fname=str(FONT_DIR / "Manrope-400.ttf"))

# Exact container background color matching PDF containers
CONTAINER_BG = "#EEF2F6"

CATEGORY_ORDER = [
    "Breakfast Cereals",
    "Nutritional Cereal Bars",
    "Spreads",
    "Liquid Breakfasts",
]

TIER_ORDER = ["Value", "Standard", "Premium"]

BRAND_COLOURS = {
    "Breakfast Cereals": "#3B0764",       # Deep Solid Purple
    "Nutritional Cereal Bars": "#FF8C30", # Peanut Ochre
    "Spreads": "#E24BFF",                 # Electric Lavender (highlighted)
    "Liquid Breakfasts": "#FF467A",       # Wild Raspberry
    "2022": "#3B0764",                    # Deep Solid Purple
    "2025": "#E24BFF",                    # Electric Lavender
}


def quarterly_revenue(frame: pd.DataFrame) -> None:
    quarters = sorted(frame["Date"].unique())
    fig, ax = plt.subplots(figsize=(10.5, 5.2), dpi=200)
    fig.patch.set_facecolor(CONTAINER_BG)
    ax.set_facecolor(CONTAINER_BG)

    for category in CATEGORY_ORDER:
        part = frame[frame["Category"] == category]
        series = (
            part.groupby("Date")["Revenue (Thousands NZD)"].sum().reindex(quarters).fillna(0)
            / 1000
        )
        is_spreads = category == "Spreads"
        ax.plot(
            quarters,
            series.values,
            label=f"{category} (Focus)" if is_spreads else category,
            color=BRAND_COLOURS[category],
            linewidth=3.2 if is_spreads else 1.8,
            alpha=1.0 if is_spreads else 0.75,
            zorder=5 if is_spreads else 3,
        )

    ax.set_title(
        "Quarterly Breakfast Category Revenue in New Zealand (2022–2025)",
        fontproperties=F_BOLD,
        fontsize=13.5,
        color="#240340",
        pad=16,
    )
    ax.set_ylabel("Revenue (Million NZD)", fontproperties=F_SEMI, fontsize=10.5, color="#475569", labelpad=10)
    ax.set_xlabel("Quarter", fontproperties=F_SEMI, fontsize=10.5, color="#475569", labelpad=10)

    legend = ax.legend(
        frameon=True,
        facecolor=CONTAINER_BG,
        edgecolor="#CBD5E1",
        loc="upper left",
    )
    for text in legend.get_texts():
        text.set_fontproperties(F_SEMI)
        text.set_fontsize(9.5)
        text.set_color("#1A1024")

    ax.tick_params(axis="x", labelrotation=45, colors="#475569")
    for label in ax.get_xticklabels():
        label.set_fontproperties(F_MED)
        label.set_fontsize(9.0)

    ax.tick_params(axis="y", colors="#64748B")
    for label in ax.get_yticklabels():
        label.set_fontproperties(F_MED)
        label.set_fontsize(9.5)

    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1", zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    fig.tight_layout()
    fig.savefig(OUT / "01-quarterly-revenue-by-category.png", dpi=200, facecolor=CONTAINER_BG)
    plt.close(fig)


def tier_comparison(frame: pd.DataFrame) -> None:
    spreads = frame[frame["Category"] == "Spreads"].copy()
    spreads["year"] = spreads["Date"].str.slice(0, 4)
    part = spreads[spreads["year"].isin(["2022", "2025"])]
    totals = (
        part.groupby(["year", "Price Tier"])["Revenue (Thousands NZD)"].sum().unstack("year")
        / 1000
    )
    totals = totals.reindex(TIER_ORDER)

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200)
    fig.patch.set_facecolor(CONTAINER_BG)
    ax.set_facecolor(CONTAINER_BG)

    positions = np.arange(len(TIER_ORDER))
    width = 0.35

    rects1 = ax.bar(
        positions - width / 2,
        totals["2022"],
        width=width,
        label="2022 Revenue",
        color=BRAND_COLOURS["2022"],
        edgecolor="none",
        zorder=3,
    )
    rects2 = ax.bar(
        positions + width / 2,
        totals["2025"],
        width=width,
        label="2025 Revenue",
        color=BRAND_COLOURS["2025"],
        edgecolor="none",
        zorder=3,
    )

    # Direct value annotations above each bar using Manrope-Bold
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(
            f"${h:.1f}M",
            (rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontproperties=F_BOLD,
            fontsize=9.5,
            color="#3B0764",
        )

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(
            f"${h:.1f}M",
            (rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontproperties=F_BOLD,
            fontsize=9.5,
            color="#A21CAF",
        )

    ax.set_xticks(positions)
    ax.set_xticklabels(TIER_ORDER)
    for label in ax.get_xticklabels():
        label.set_fontproperties(F_BOLD)
        label.set_fontsize(11.0)
        label.set_color("#1A1024")

    ax.set_ylabel("Revenue (Million NZD)", fontproperties=F_SEMI, fontsize=10.5, color="#475569", labelpad=10)
    ax.set_title(
        "New Zealand Spreads Category Revenue by Price Tier (2022 vs 2025)",
        fontproperties=F_BOLD,
        fontsize=13.0,
        color="#240340",
        pad=16,
    )

    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1", zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    ax.tick_params(axis="y", colors="#64748B")
    for label in ax.get_yticklabels():
        label.set_fontproperties(F_MED)
        label.set_fontsize(9.5)

    ax.tick_params(axis="x", colors="#1A1024", length=0)
    ax.set_ylim(0, max(totals.max()) * 1.18)

    legend = ax.legend(
        frameon=True,
        facecolor=CONTAINER_BG,
        edgecolor="#CBD5E1",
        loc="upper left",
    )
    for text in legend.get_texts():
        text.set_fontproperties(F_SEMI)
        text.set_fontsize(9.5)
        text.set_color("#1A1024")

    fig.tight_layout()
    fig.savefig(OUT / "02-spreads-revenue-by-tier-2022-vs-2025.png", dpi=200, facecolor=CONTAINER_BG)
    plt.close(fig)


def price_distribution(frame: pd.DataFrame) -> None:
    spreads = frame[
        (frame["Category"] == "Spreads")
        & (frame["Market Segment"] == "Branded")
        & frame["price_usable"]
        & frame["price_per_100g"].notna()
    ].copy()

    sku = spreads.groupby(["Product Name", "Brand", "Weight"], as_index=False)[
        "price_per_100g"
    ].median()

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200)
    fig.patch.set_facecolor(CONTAINER_BG)
    ax.set_facecolor(CONTAINER_BG)

    # Histogram with Stamp brand colors
    n, bins, patches = ax.hist(
        sku["price_per_100g"],
        bins=26,
        color="#240340",
        edgecolor=CONTAINER_BG,
        linewidth=1.2,
        zorder=3,
    )

    for patch in patches:
        if patch.get_x() >= 5.0:
            patch.set_facecolor("#3B0764")

    # Stamp price line
    stamp_price = 6.25
    ax.axvline(stamp_price, color="#E24BFF", linestyle="-", linewidth=2.6, zorder=4)

    # 90th percentile benchmark line
    p90 = sku["price_per_100g"].quantile(0.9)
    ax.axvline(p90, color="#FF8C30", linestyle="--", linewidth=1.8, zorder=4)

    # Annotations in Manrope
    ylim = ax.get_ylim()[1]
    ax.text(
        stamp_price + 0.15,
        ylim * 0.88,
        "STAMP: $6.25 / 100 g\nFormat Innovation Premium",
        fontproperties=F_BOLD,
        fontsize=9.5,
        color="#A21CAF",
        va="top",
    )

    ax.text(
        p90 - 0.15,
        ylim * 0.72,
        f"90th Percentile: ${p90:.2f} / 100 g",
        fontproperties=F_SEMI,
        fontsize=8.5,
        color="#C2410C",
        ha="right",
        va="top",
    )

    ax.set_xlabel("Shelf Price per 100 g (NZD)", fontproperties=F_SEMI, fontsize=10.5, color="#475569", labelpad=8)
    ax.set_ylabel("Number of Branded Spread SKUs", fontproperties=F_SEMI, fontsize=10.5, color="#475569", labelpad=8)
    ax.set_title(
        "Shelf Price Distribution Across 154 Branded New Zealand Spread SKUs",
        fontproperties=F_BOLD,
        fontsize=13.0,
        color="#240340",
        pad=16,
    )

    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1", zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    ax.tick_params(axis="y", colors="#64748B")
    for label in ax.get_yticklabels():
        label.set_fontproperties(F_MED)
        label.set_fontsize(9.5)

    ax.tick_params(axis="x", colors="#1A1024")
    for label in ax.get_xticklabels():
        label.set_fontproperties(F_MED)
        label.set_fontsize(9.5)

    fig.tight_layout()
    fig.savefig(OUT / "03-branded-spreads-price-per-100g.png", dpi=200, facecolor=CONTAINER_BG)
    plt.close(fig)

    quantiles = sku["price_per_100g"].quantile([0.1, 0.25, 0.5, 0.75, 0.9])
    print("branded spread SKUs", len(sku))
    print(quantiles.to_string())
    print("min", round(sku["price_per_100g"].min(), 2), "max", round(sku["price_per_100g"].max(), 2))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(DATA)
    quarterly_revenue(frame)
    tier_comparison(frame)
    price_distribution(frame)
    print("Successfully regenerated branded figures with matching container background and Manrope typography")


if __name__ == "__main__":
    main()
