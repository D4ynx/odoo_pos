# Restaurant POS for Odoo 18

A restaurant point-of-sale module for **Odoo 18 Community**. Orders flow from the table to the kitchen to
payment. At payment, ingredients are deducted from inventory using each dish's recipe, and the cost of goods sold (COGS) is calculated **FIFO** from what those ingredients actually cost when they were bought.

> 🚧 Work in progress, built milestone by milestone. See the [roadmap](#roadmap).

## Features
- **Tables & floor**: open an order on a table, which shows as occupied until the order is paid
- **Kitchen workflow**: `draft → kitchen → served → paid`
- **Recipe masterlist**: each dish lists its ingredients and quantities
- **Ingredient purchases**: every purchase adds stock at its own unit cost
- **FIFO inventory**: the oldest stock is consumed first, with automatic unit conversion (g ↔ kg, mL ↔ L)
- **COGS & margin**: real cost per order, plus a margin report per dish and per day

## How it works
1. Ingredients are purchased, and each purchase line becomes a **stock lot** with its own unit cost.
2. A waiter opens an order on a table and adds dishes.
3. The order is sent to the kitchen and then served.
4. On **payment**, each dish is expanded into ingredients using its recipe. Stock is consumed FIFO,
   COGS is recorded, and the table is freed. If any ingredient is short, payment is blocked and nothing is consumed.

### Example
Pizza Margherita uses **200 g flour**. Flour in stock:

| Lot | Qty | Unit cost |
|---|---|---|
| A (older) | 1 kg | ₱80 / kg |
| B (newer) | 1 kg | ₱100 / kg |

- **1 pizza**: 0.2 kg from lot A → COGS **₱16**
- **6 more pizzas** (1.2 kg): 0.8 kg from A (₱64) + 0.4 kg from B (₱40) → COGS **₱104**

## Tech
- Odoo 18.0 Community · Python 3.12 · PostgreSQL 16
- Depends on: `base`, `uom`

## Installation
```bash
git clone git@github.com:D4ynx/odoo_pos.git custom_addons
./odoo-bin --addons-path=addons,custom_addons -d <your_db> -i resto_pos
```

## Roadmap
- [ ] **M0** Repo setup, tooling, README
- [ ] **M1** Ingredients with units of measure
- [ ] **M2** Menu items and recipes
- [ ] **M3** Purchases, stock lots, FIFO (with tests)
- [ ] **M4** Tables, orders, kitchen workflow, COGS at payment
- [ ] **M5** Security: Waiter / Kitchen / Manager roles
- [ ] **M6** Customers on orders (extending `res.partner`)
- [ ] **M7** Receipt, kitchen ticket, margin report
- [ ] **M8** JSON endpoint and XML-RPC client
- [ ] **M9** OWL dashboard (stretch)

## Author
Ricofel Guinanao ([@D4ynx](https://github.com/D4ynx))
