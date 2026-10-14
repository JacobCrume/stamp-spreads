# Information notes

Entities in `diagrams/erd.mmd`: Customer, Order, OrderLine (the order line), Sheet (the sellable pack), Product (the flavour), Batch, Manufacturer, Campaign.

A Sheet includes one Product when the pack is a single flavour (8 stamps). The mixed sheet includes all four Products, two stamps of each. A Batch deposits one Product. A Batch supplies a Sheet only when the stamps passed the check. A Batch with release_rejects above zero failed release and those stamps are not on a dispatched Sheet.

## KPIs

**1. Repeat purchase rate.** Entity: Customer, counted from Order.

Formula: number of Customers with two or more Orders, divided by the number of Customers with at least one Order.

**2. Stamps per order.** Entity: OrderLine, using Sheet.

Formula: sum of (OrderLine.sheet_qty times Sheet.stamps_on_sheet) across all order lines, divided by the number of Orders. stamps_on_sheet is 8 on every pack, including mixed.

**3. On-time dispatch rate.** Entity: Order.

Formula: number of Orders whose dispatched_on is on or before promised_dispatch, divided by the number of Orders that have a dispatched_on. An order with no dispatch date is not in this rate.

**4. Batch rejection rate.** Entity: Batch.

Formula: (sum of weight_rejects + sum of release_rejects) divided by sum of stamps_checked. A weight reject is a stamp outside 10 g ± 0.5 g. A release reject is a stamp whose film will not release. Each checked stamp is counted once, under the first failure found. Rejected stamps are not packed and are not dispatched.

**5. Gross margin per sheet after manufacturer cost.** Entity: Sheet, for the shelf price. The cost term is an assumption, not a figure stored on Manufacturer, and not a quote from Griffiths & Co.

Formula, labelled as an assumption: shelf price $5.00, retailer share 35% ($1.75), so Stamp receives $5.00 times (1 minus 0.35) = $3.25. Subtract the assumed manufactured cost of $1.50. Gross margin per sheet = $3.25 minus $1.50 = $1.75. Change the 35% or the $1.50 and this margin changes. The recipes do not.

## Questions this model can answer

Which flavour is reordered? A flavour is a Product. Follow Customer to Order to OrderLine to Sheet to Product. A reorder of a flavour is a later Order from the same Customer for a single-flavour Sheet whose only included Product is that flavour. A mixed Sheet is a separate pack (two of each), not a reorder of one flavour.

Which batch failed release? Read Batch.release_rejects. Any Batch with release_rejects above zero failed the film-release check. Those stamps do not supply a Sheet and do not go to dispatch. Manufacturer says who ran that batch.

## Question this model cannot answer

Whether a flavour has a medical effect. No entity records a symptom, a diagnosis, a test result, or any health outcome. Orders, batches, and flavours cannot support that claim, and the product does not make it.
