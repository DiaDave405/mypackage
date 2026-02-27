from decimal import Decimal

import pytest

from mypackage import POSApp, top_n


def test_top_n_non_mutating_and_sorted():
    items = [8, 3, 2, 7, 4]
    assert top_n(items, 3) == [8, 7, 4]
    assert items == [8, 3, 2, 7, 4]


def test_pos_checkout_flow():
    app = POSApp(cashier="Dave", tax_rate=Decimal("0.075"))
    app.add_product("SKU1", "Milk", "2.50")
    app.add_product("SKU2", "Bread", "3.00")

    app.add_item("SKU1", quantity=2)
    app.add_item("SKU2", quantity=1)

    assert app.subtotal() == Decimal("8.00")
    assert app.tax_amount() == Decimal("0.60")
    assert app.total() == Decimal("8.60")

    sale = app.checkout("10")
    assert sale.sale_id == "S-000001"
    assert sale.change == Decimal("1.40")
    assert app.total() == Decimal("0.00")


def test_pos_insufficient_payment():
    app = POSApp(cashier="Dave")
    app.add_product("SKU1", "Milk", "2.50")
    app.add_item("SKU1")

    with pytest.raises(ValueError, match="Insufficient payment"):
        app.checkout("2.00")
