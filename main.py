import json
from dataclasses import dataclass
import numpy as np

DAY1_FILENAME = "./data/day_1.json"
DAY1_FILENAME = "./data/day_1.json"
DAY1_FILENAME = "./data/day_1.json"


@dataclass
class Box:
    id: int
    weight: int


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
    stock: list[Box] | None


@dataclass
class Truck:
    afiliated_warehouse: Warehouse
    capacity: int


def parse_las_brickas() -> tuple[list[Warehouse], list[Customer], np.ndarray]:
    LAS_BRICKAS_FILENAME = "./data/las_brickas.json"

    matrix = np.full((5000, 5000), None, dtype=object)

    data = {}
    with open(LAS_BRICKAS_FILENAME) as f:
        data = json.load(f)

    parsed_customers = {}
    customers = data["Customers"]
    for customer in customers:
        coords = customer["Coordinates"]

        custom = Customer(customer["Id"], coords["X"], coords["Y"], [])
        matrix[custom.x, custom.y] = custom
        parsed_customers[custom.id] = custom

    parsed_warehouses = {}
    warehouses = data["Warehouses"]
    for warehouse in warehouses:
        coords = warehouse["Coordinates"]

        ware = Warehouse(warehouse["Id"], coords["X"], coords["Y"], [])
        matrix[ware.x, ware.y] = ware
        parsed_warehouses[ware.id] = ware

    return parsed_customers, parsed_warehouses, matrix


def parse_day(filename, warehouses: list[Warehouse], customers: list[Customer]):
    data = {}
    with open(filename) as f:
        data = json.load(f)

    parsed_trucks = []
    trucks = data["Trucks"]
    for truck in trucks:
        truck = Truck(warehouses[truck["AffiliatedWarehouseId"]], truck["Capacity"])
        parsed_trucks.append(truck)

    parsed_box = {}
    legos = data["Legos"]
    for lego in legos:
        box = Box(lego["Id"], lego["Weight"])
        parsed_box[box.id] = box

    new_customer_data = data["Customers"]
    for new_data in new_customer_data:
        for order_json in new_data["Orders"]:
            order = Order(
                order_json["LegoId"],
                parsed_box[order_json["LegoId"]],
                order_json["Quantity"],
            )
            customers[new_data["Id"]].orders.append(order)

    new_warehouse_data = data["Warehouses"]
    for new_data in new_warehouse_data:
        for box_json in new_data["Stock"]:
            box = parsed_box[box_json["LegoId"]]
            for _ in range(box_json["Quantity"]):
                warehouses[new_data["Id"]].stock.append(box)

    return warehouses, customers, parsed_trucks, parsed_box


def day1():
    customers, warehouses, matrix = parse_las_brickas()
    warehouses, customers, trucks, box = parse_day(DAY1_FILENAME, warehouses, customers)
    print(box)


if __name__ == "__main__":
    day1()
