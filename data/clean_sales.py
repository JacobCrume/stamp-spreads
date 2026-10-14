"""Clean the NZ breakfast sales workbook.

A row is one pack variant in one quarter: product name + brand + weight + quarter.
Same name with two weights is two SKUs and is kept.

Price rule: a unit price above $40 is inspected. When units and revenue are
both present and revenue / units falls between $0.50 and $40, the listed price
is garbage and is replaced with that implied price. When the implied price
agrees with the listed price (within 5%), the row is a genuinely expensive
product and the price stays usable. Otherwise the price is quarantined and is
not used for imputation or per-100 g calculations.

Missing units or revenue are filled only when the surviving price is usable:
revenue = price x units, or units = revenue / price.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "nz_breakfast_sales_2022_2025.xlsx"
OUT_DIR = Path(__file__).resolve().parent

PRICE_SUSPECT = 40.0
IMPLIED_MIN = 0.50
IMPLIED_MAX = 40.0
IDENTITY_TOLERANCE = 0.05
HIGH_PRICE_AGREE = 0.05

WEIGHT_PACK = re.compile(
    r"^(\d+(?:\.\d+)?)\s*[xX×]\s*(\d+(?:\.\d+)?)\s*(g|ml|kg|l)$",
    re.IGNORECASE,
)
WEIGHT_SINGLE = re.compile(
    r"^(\d+(?:\.\d+)?)\s*(g|ml|kg|l)$",
    re.IGNORECASE,
)
WEIGHT_EACH = re.compile(r"^(\d+(?:\.\d+)?)\s*g\s*each$", re.IGNORECASE)
PACK_IN_NAME = re.compile(r"(\d+)\s*pack", re.IGNORECASE)


def to_grams(amount: float, unit: str) -> float:
    unit = unit.lower()
    if unit in ("kg", "l"):
        return amount * 1000
    return amount


def parse_weight(weight: str, product_name: str) -> tuple[float | None, float | None, str]:
    """Return pack count, total grams (ml treated as g), and a parse status."""
    text = str(weight).strip()
    packed = WEIGHT_PACK.fullmatch(text)
    if packed:
        count = float(packed.group(1))
        each = to_grams(float(packed.group(2)), packed.group(3))
        return count, count * each, "parsed_multipack"

    single = WEIGHT_SINGLE.fullmatch(text)
    if single:
        return 1.0, to_grams(float(single.group(1)), single.group(2)), "parsed_single"

    each = WEIGHT_EACH.fullmatch(text)
    if each:
        grams_each = float(each.group(1))
        named = PACK_IN_NAME.search(str(product_name))
        if named:
            count = float(named.group(1))
            return count, count * grams_each, "parsed_each_from_name"
        return None, None, "unparsed_each"

    return None, None, "unparsed"


def load() -> pd.DataFrame:
    frame = pd.read_excel(SOURCE, sheet_name="Sales Data")
    frame.insert(0, "row_id", range(1, len(frame) + 1))
    return frame


def clean(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["price_original"] = out["Unit Price (NZD)"]
    out["units_original"] = out["Units Sold (Thousands)"]
    out["revenue_original"] = out["Revenue (Thousands NZD)"]
    out["price_action"] = "kept"
    out["imputed_flag"] = ""
    out["price_usable"] = True

    for index, row in out.iterrows():
        price = row["price_original"]
        units = row["units_original"]
        revenue = row["revenue_original"]
        if price > PRICE_SUSPECT:
            if pd.notna(units) and pd.notna(revenue) and units != 0:
                implied = float(revenue) / float(units)
                if IMPLIED_MIN <= implied <= IMPLIED_MAX:
                    out.at[index, "Unit Price (NZD)"] = round(implied, 4)
                    out.at[index, "price_action"] = "replaced_with_implied"
                elif abs(implied - float(price)) / float(price) <= HIGH_PRICE_AGREE:
                    out.at[index, "price_action"] = "kept_high_consistent"
                else:
                    out.at[index, "price_action"] = "quarantined"
                    out.at[index, "price_usable"] = False
            else:
                out.at[index, "price_action"] = "quarantined"
                out.at[index, "price_usable"] = False

    for index, row in out.iterrows():
        if not row["price_usable"]:
            continue
        price = float(row["Unit Price (NZD)"])
        units = row["units_original"]
        revenue = row["revenue_original"]
        if pd.isna(units) and pd.notna(revenue) and price > 0:
            out.at[index, "Units Sold (Thousands)"] = round(float(revenue) / price, 4)
            out.at[index, "imputed_flag"] = "units"
        elif pd.isna(revenue) and pd.notna(units):
            out.at[index, "Revenue (Thousands NZD)"] = round(price * float(units), 4)
            out.at[index, "imputed_flag"] = "revenue"

    parsed = out.apply(
        lambda row: parse_weight(row["Weight"], row["Product Name"]),
        axis=1,
        result_type="expand",
    )
    parsed.columns = ["pack_count", "weight_g", "weight_parse"]
    out = pd.concat([out, parsed], axis=1)

    usable = out["price_usable"] & out["weight_g"].notna() & (out["weight_g"] > 0)
    out["price_per_100g"] = pd.NA
    out.loc[usable, "price_per_100g"] = (
        out.loc[usable, "Unit Price (NZD)"] / out.loc[usable, "weight_g"] * 100
    )

    both_present = out["Units Sold (Thousands)"].notna() & out["Revenue (Thousands NZD)"].notna()
    nonzero = both_present & (out["Units Sold (Thousands)"] != 0)
    expected = out["Unit Price (NZD)"] * out["Units Sold (Thousands)"]
    gap = (expected - out["Revenue (Thousands NZD)"]).abs() / expected.abs().clip(lower=0.01)
    out["identity_mismatch"] = nonzero & out["price_usable"] & (gap > IDENTITY_TOLERANCE)
    out["zero_sales"] = (out["Units Sold (Thousands)"].fillna(0) == 0) & (
        out["Revenue (Thousands NZD)"].fillna(0) == 0
    )
    return out


def write(frame: pd.DataFrame) -> None:
    keep = [
        "row_id",
        "Date",
        "Product Name",
        "Brand",
        "Category",
        "Is Plant Powered",
        "Is Weight Conscious",
        "Is Performance Focused",
        "Is Gluten Free",
        "Is Organic",
        "Unit Price (NZD)",
        "price_original",
        "price_action",
        "price_usable",
        "Weight",
        "pack_count",
        "weight_g",
        "weight_parse",
        "price_per_100g",
        "Market Segment",
        "Price Tier",
        "Units Sold (Thousands)",
        "units_original",
        "Revenue (Thousands NZD)",
        "revenue_original",
        "imputed_flag",
        "identity_mismatch",
        "zero_sales",
    ]
    full = frame[keep]
    full.to_csv(OUT_DIR / "sales-clean.csv", index=False)
    full[full["Category"] == "Spreads"].to_csv(OUT_DIR / "spreads-clean.csv", index=False)

    log_mask = (
        (frame["price_action"] != "kept")
        | (frame["imputed_flag"] != "")
        | frame["identity_mismatch"]
        | (frame["weight_parse"].str.startswith("unparsed"))
    )
    log_cols = [
        "row_id",
        "Date",
        "Product Name",
        "Brand",
        "Category",
        "Weight",
        "weight_parse",
        "price_original",
        "Unit Price (NZD)",
        "price_action",
        "units_original",
        "Units Sold (Thousands)",
        "revenue_original",
        "Revenue (Thousands NZD)",
        "imputed_flag",
        "identity_mismatch",
    ]
    frame.loc[log_mask, log_cols].to_csv(OUT_DIR / "cleaning-log.csv", index=False)


def main() -> None:
    frame = clean(load())
    write(frame)
    print(f"rows {len(frame)}")
    print(frame["price_action"].value_counts().to_string())
    print("imputed")
    print(frame["imputed_flag"].value_counts().to_string())
    print("weight_parse")
    print(frame["weight_parse"].value_counts().to_string())
    print("identity mismatches", int(frame["identity_mismatch"].sum()))
    print("zero sales", int(frame["zero_sales"].sum()))
    print("unusable price", int((~frame["price_usable"]).sum()))


if __name__ == "__main__":
    main()
