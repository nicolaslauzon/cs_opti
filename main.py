from parsers import parse_las_brickas, parse_day

from custom_types import Box, Order, Warehouse, Customer, Truck

DAY1_FILENAME = "./data/day_1.json"
DAY2_FILENAME = "./data/day_2.json"
DAY3_FILENAME = "./data/day_3.json"


def day1():
    customers, warehouses, matrix = parse_las_brickas()
    warehouses, customers, trucks, box = parse_day(DAY1_FILENAME, warehouses, customers)
    print(box)


def addLoadActionToAnswer(truck, quantity, lego, steps):
    steps.append("load truck=" + truck + "  quantity=" + quantity + " lego=" + lego)
    return steps


def addMoveToCustomerActionToAnswer(truck, customer, steps):
    steps.append("move_to_customer truck=" + truck + " customer=" + customer)
    return steps


def addDeliverActionToAnswer(truck, quantity, lego, steps):
    steps.append("deliver truck=" + truck + " quantity=" + quantity + " lego=" + lego)
    return steps


def addMoveToWarehouseActionToAnswer(truck, warehouse, steps):
    steps.append("move_to_warehouse truck=" + truck + " warehouse=" + warehouse)
    return steps


if __name__ == "__main__":
    day1()
