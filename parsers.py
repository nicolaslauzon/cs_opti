import numpy as np
import json
from custom_types import Box, Order, Warehouse, Customer, Truck


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
    print("parsed trucks")

    parsed_box = {}
    legos = data["Legos"]
    for lego in legos:
        box = Box(lego["Id"], lego["Weight"])
        parsed_box[box.id] = box
    print("parsed boxes")

    new_customer_data = data["Customers"]
    for new_data in new_customer_data:
        for order_json in new_data["Orders"]:
            order = Order(
                order_json["LegoId"],
                parsed_box[order_json["LegoId"]],
                order_json["Quantity"],
            )
            customers[new_data["Id"]].orders.append(order)
    print("parsed customers")

    new_warehouse_data = data["Warehouses"]
    for new_data in new_warehouse_data:
        for box_json in new_data["Stock"]:
            box = parsed_box[box_json["LegoId"]]
            for _ in range(box_json["Quantity"]):
                warehouses[new_data["Id"]].stock.append(box)
    print("parsed warehouses")

    return warehouses, customers, parsed_trucks, parsed_box
