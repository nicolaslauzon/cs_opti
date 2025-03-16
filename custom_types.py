from dataclasses import dataclass


@dataclass
class Box:
    id: int
    weight: int

@dataclass
class BoxInventory:
    id: int
    inventory: int


@dataclass
class Order:
    box_id: int
    box: Box
    qty: int


@dataclass
class Customer:
    id: int
    x: int
    y: int
    orders: list[Order] | None


@dataclass
class Warehouse:
    id: int
    x: int
    y: int
    stock: list[BoxInventory] | None


@dataclass
class Truck:
    afiliated_warehouse: Warehouse
    capacity: int
