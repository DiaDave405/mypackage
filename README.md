# mypackage POS starter

This repository now includes:

- A Python POS domain layer you can use as the foundation for a full app (desktop/web/API).
- An improved VBA module for your Excel-based POS workbook.

## Install

```bash
pip install -e .
```

## Python POS quick start

```python
from decimal import Decimal
from mypackage import POSApp

app = POSApp(cashier="Dave", tax_rate=Decimal("0.075"))
app.add_product("SKU1", "Milk", "2.50")
app.add_item("SKU1", 2)
sale = app.checkout("10")
print(sale.total, sale.change)
```

## Excel/VBA improvements

Use `docs/excel_pos_enhanced.bas` as a drop-in helper module. It improves:

- Kiosk UI toggle reliability.
- License validation safety and readability.
- Reusable payment checks.

## Recommended next step for a full functional app

Build a thin API/UI around `POSApp`:

1. **Backend**: FastAPI endpoints for products, cart, checkout.
2. **Frontend**: React or simple HTML POS screen.
3. **Persistence**: SQLite/PostgreSQL for products and sales.
4. **Sync**: Optional Excel import/export for migration from your macro workbook.
