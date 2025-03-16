from parsers import parse_las_brickas, parse_day

from custom_types import Box, Order, Warehouse, Customer, Truck

DAY1_FILENAME = "./data/day_1.json"
DAY2_FILENAME = "./data/day_2.json"
DAY3_FILENAME = "./data/day_3.json"

customers, warehouses, matrix = parse_las_brickas()

def day1():
    #Fait a la main
    warehouses, customers, trucks, box = parse_day(DAY1_FILENAME, warehouses, customers)
    print(box)

def day2():
    warehouses, customers, trucks, box = parse_day(DAY2_FILENAME, warehouses, customers)
    steps = addAllLoadsForDay2(steps, customers)
    e = 3

def day3():
    steps = []
    warehouses, customers, trucks, box = parse_day(DAY3_FILENAME, warehouses, customers)
    e = 3

def getDistManhattan(x1, y1, x2, y2): 
    xDiff = abs(x2 - x1)
    yDiff = abs(y2 - y1)
    return xDiff + yDiff

def addAllLoadsForDay2(steps, customers):
    orderDict = {}
    for customer in customers: 
        for order in customer["Orders"]:
            if order["LegoId"] in orderDict:
                orderDict[order["LegoId"]] += 1
            else:
                orderDict[order["LegoId"]] = 1
    for legoType in orderDict:
        steps = addLoadActionToAnswer(0, orderDict[legoType], legoType, steps)
    return steps

def addLoadActionToAnswer(truck, quantity, lego, steps):
    steps.append("load truck=" + str(truck) + " quantity=" + str(quantity) + " lego=" + str(lego))
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
