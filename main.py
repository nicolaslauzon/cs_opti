import json
from dataclasses import dataclass

@dataclass
class Customer:
    id: int
    x: int
    y: int


@dataclass
class Warehouse:
    id: int
    x: int
    y: int


def parse_las_brickas():
    LAS_BRICKAS_FILENAME = "./data/las_brickas.json"

    data = {}
    with open(LAS_BRICKAS_FILENAME) as f:
        data = json.load(f)

    parsed_customers = []
    customers = data["Customers"]
    for customer in customers:
        coords = customer["Coordinates"]
        parsed_customers.append(Customer(customer["Id"], coords["X"], coords["Y"]))

    parsed_warehouses = []
    warehouses = data["Warehouses"]
    for warehouse in warehouses:
        coords = warehouse["Coordinates"]
        parsed_warehouses.append(Customer(warehouse["Id"], coords["X"], coords["Y"]))

    return parsed_customers, parsed_warehouses

def addLoadActionToAnswer(truck, quantity, lego, steps): 
    steps.append("load truck=" + truck +"  quantity=" + quantity + " lego=" + lego)
    return steps

def addMoveToCustomerActionToAnswer(truck, customer, steps): 
    steps.append("move_to_customer truck=" + truck +" customer=" + customer)
    return steps

def addDeliverActionToAnswer(truck, quantity, lego, steps): 
    steps.append("deliver truck=" + truck +" quantity=" + quantity +" lego=" + lego)
    return steps

def addMoveToWarehouseActionToAnswer(truck, warehouse, steps): 
    steps.append("move_to_warehouse truck=" + truck +" warehouse=" + warehouse)
    return steps


if __name__ == "__main__":
    parsed_customers, parsed_warehouses = parse_las_brickas()

    print(parsed_customers)
