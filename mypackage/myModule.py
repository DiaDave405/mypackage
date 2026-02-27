"""Core utilities for the package."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List


def top_n(items, n):
    """Return the top ``n`` items in descending order without mutating input."""
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return []
    return sorted(list(items), reverse=True)[:n]


TWOPLACES = Decimal("0.01")


def _money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(TWOPLACES, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price: Decimal

    @classmethod
    def from_values(cls, sku: str, name: str, price: Decimal | int | float | str) -> "Product":
        return cls(sku=sku, name=name, price=_money(price))


@dataclass
class CartLine:
    product: Product
    quantity: int = 1

    def subtotal(self) -> Decimal:
        return _money(self.product.price * self.quantity)


@dataclass
class Sale:
    sale_id: str
    created_at: datetime
    lines: List[CartLine]
    total: Decimal
    payment: Decimal
    change: Decimal


@dataclass
class POSApp:
    cashier: str
    tax_rate: Decimal = Decimal("0.00")
    _catalog: Dict[str, Product] = field(default_factory=dict)
    _cart: Dict[str, CartLine] = field(default_factory=dict)
    _sales: List[Sale] = field(default_factory=list)

    def add_product(self, sku: str, name: str, price: Decimal | int | float | str) -> Product:
        product = Product.from_values(sku=sku, name=name, price=price)
        self._catalog[sku] = product
        return product

    def add_item(self, sku: str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be > 0")
        if sku not in self._catalog:
            raise KeyError(f"Unknown SKU: {sku}")

        if sku in self._cart:
            self._cart[sku].quantity += quantity
        else:
            self._cart[sku] = CartLine(product=self._catalog[sku], quantity=quantity)

    def update_quantity(self, sku: str, quantity: int) -> None:
        if sku not in self._cart:
            raise KeyError(f"Item not in cart: {sku}")
        if quantity <= 0:
            del self._cart[sku]
            return
        self._cart[sku].quantity = quantity

    def cart_lines(self) -> List[CartLine]:
        return list(self._cart.values())

    def subtotal(self) -> Decimal:
        return _money(sum(line.subtotal() for line in self._cart.values()))

    def tax_amount(self) -> Decimal:
        return _money(self.subtotal() * self.tax_rate)

    def total(self) -> Decimal:
        return _money(self.subtotal() + self.tax_amount())

    def checkout(self, payment: Decimal | int | float | str) -> Sale:
        payment_value = _money(payment)
        total = self.total()
        if total <= 0:
            raise ValueError("Cannot checkout an empty cart")
        if payment_value < total:
            raise ValueError("Insufficient payment")

        sale = Sale(
            sale_id=f"S-{len(self._sales) + 1:06d}",
            created_at=datetime.utcnow(),
            lines=[CartLine(line.product, line.quantity) for line in self._cart.values()],
            total=total,
            payment=payment_value,
            change=_money(payment_value - total),
        )
        self._sales.append(sale)
        self._cart.clear()
        return sale

    def sales_history(self) -> List[Sale]:
        return list(self._sales)
