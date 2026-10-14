"""Market figures for the business plan.

Figures 1 and 2 use cleaned revenue. Figure 3 is the branded-spreads
price-per-100 g distribution. The Stamp shelf-price marker is added once
a sheet price and a grams-per-stamp decision exist.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

OUT = Path(__file__).resolve().parent / "figures"
DATA = Path(__file__).resolve().parent / "sales-clean.csv"

CATEGORY_ORDER = [
    "Breakfast Cereals",
    "Nutritional Cereal Bars",
    "Spreads",
    "Liquid Breakfasts",
]
TIER_ORDER = ["Value", "Standard", "Premium"]
COLOURS = {
    "Breakfast Cereals": "#4C78A8",
    "Nutritional Cereal Bars": "#F58518",
    "Spreads": "#54A24B",
    "Liquid Breakfasts": "#E45756",
    "Value": "#9E9AC8",
    "Standard": "#4C78A8",
    "Premium": "#E45756",
}


def quarterly_revenue(frame: pd.DataFrame) -> None:
    quarters = sorted(frame["Date"].unique())
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    for category in CATEGORY_ORDER:
        part = frame[frame["Category"] == category]
        series = (
            part.groupby("Date")["Revenue (Thousands NZD)"].sum().reindex(quarters).fillna(0)
            / 1000
        )
        ax.plot(quarters, series.values, label=category, color=COLOURS[category], linewidth=2.2)
    ax.set_title("Quarterly breakfast revenue by category, New Zealand")
    ax.set_ylabel("Revenue (million NZD)")
    ax.set_xlabel("Quarter")
    ax.legend(frameon=False)
    ax.tick_params(axis="x", labelrotation=60)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "01-quarterly-revenue-by-category.png", dpi=160)
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
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    positions = range(len(TIER_ORDER))
    width = 0.36
    ax.bar(
        [p - width / 2 for p in positions],
        totals["2022"],
        width=width,
        label="2022",
        color="#9ECAE1",
    )
    ax.bar(
        [p + width / 2 for p in positions],
        totals["2025"],
        width=width,
        label="2025",
        color="#2171B5",
    )
    ax.set_xticks(list(positions), TIER_ORDER)
    ax.set_ylabel("Revenue (million NZD)")
    ax.set_title("Spreads revenue by price tier, 2022 and 2025")
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "02-spreads-revenue-by-tier-2022-vs-2025.png", dpi=160)
    plt.close(fig)


def price_distribution(frame: pd.DataFrame) -> None:
    spreads = frame[
        (frame["Category"] == "Spreads")
        & (frame["Market Segment"] == "Branded")
        & frame["price_usable"]
        & frame["price_per_100g"].notna()
    ].copy()
    # One observation per SKU at its median quarterly price, so a product
    # that stays on shelf for 16 quarters does not dominate the shape.
    sku = spreads.groupby(["Product Name", "Brand", "Weight"], as_index=False)[
        "price_per_100g"
    ].median()
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    ax.hist(sku["price_per_100g"], bins=28, color="#54A24B", edgecolor="white")
    ax.axvline(6.25, color="#111111", linestyle="--", linewidth=1.4)
    ax.text(6.4, ax.get_ylim()[1] * 0.92, "Stamp sheet\n$6.25 / 100 g", fontsize=9, va="top")
    ax.set_xlabel("Price per 100 g (NZD)")
    ax.set_ylabel("Branded spread SKUs")
    ax.set_title("Shelf price per 100 g, branded New Zealand spreads")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "03-branded-spreads-price-per-100g.png", dpi=160)
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


if __name__ == "__main__":
    main()
