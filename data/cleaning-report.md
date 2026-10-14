# Sales data cleaning

Source: `nz_breakfast_sales_2022_2025.xlsx`, sheet `Sales Data`, 12,020 rows.
Script: `data/clean_sales.py`.
Outputs: `data/sales-clean.csv`, `data/spreads-clean.csv`, `data/cleaning-log.csv`.

A row is one pack in one quarter (product name + brand + weight + quarter). Rows that share a name but have different weights were kept.

## What changed

| Action | Rows | Rule |
| --- | --- | --- |
| Price replaced with revenue ÷ units | 12 | Listed price was above $40 and the implied price was between $0.50 and $40. Example: Fix & Fogg Smooth Almond Butter, 2022-Q2, listed at $2,434.76, implied $18.49. |
| High price kept | 17 | Listed price was $41–$43.89 and revenue ÷ units agreed within 5%. All are Athena protein-water powders. Treated as a real shelf price. |
| Units filled | 60 | Units were blank. Filled as revenue ÷ usable price. |
| Revenue filled | 24 | Revenue was blank. Filled as price × units. |
| Price quarantined | 0 | No row had a high price that also disagreed with revenue. |
| Weight not parsed | 16 | Golden Days Original Sesame Snaps, weight `3pk`, no grams on the row. Excluded from per-100 g figures only. |
| Identity left as published | 4 | Usable price, but price × units differs from revenue by 5–7%. Clif Bar Crunchy Peanut Butter Energy Bar, Vogel's Cafe-Style muesli, Airborne Honey for Kids, The Crafty Weka Nutty Caramel Muesli Bites. Not overwritten. |
| Zero sales kept | 114 | Units and revenue both zero. |

`40g each` on Health Lab ball multipacks was read with the pack count in the product name (`3pack`), so those rows are 120 g.

## Spreads after cleaning

Revenue is the cleaned revenue column, in million NZD (the source column is thousands of NZD).

| Year | Revenue (million NZD) | Units (thousands) |
| --- | --- | --- |
| 2022 | 275.0 | 32,820 |
| 2023 | 305.3 | 36,346 |
| 2024 | 319.0 | 37,995 |
| 2025 | 341.4 | 40,236 |

2024 revenue is $3.4 million higher than the raw column because blank revenue cells in that year were filled. Other years barely moved. Tier comparison, cleaned revenue, million NZD:

| Tier | 2022 | 2025 |
| --- | --- | --- |
| Value | 36.1 | 39.1 |
| Standard | 150.6 | 188.9 |
| Premium | 88.3 | 113.4 |

Branded spreads, median quarterly price per 100 g, one point per SKU (168 SKUs): 10th percentile $1.46, median $2.15, 75th $2.77, 90th $5.19. The top of the range is manuka honey, not peanut butter or jam. Fix & Fogg's SKU medians sit around $2.65 per 100 g.

## Figures

- `data/figures/01-quarterly-revenue-by-category.png`
- `data/figures/02-spreads-revenue-by-tier-2022-vs-2025.png`
- `data/figures/03-branded-spreads-price-per-100g.png`

Figure 3 has no Stamp price marker yet. That line is added after the sheet price and the grams per stamp are chosen.
