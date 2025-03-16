from parsers import parse_las_brickas, parse_day
import json
import requests

import numpy as np
from custom_types import Box, Order, Warehouse, Customer, Truck
import networkx as nx
from itertools import combinations

DAY1_FILENAME = "./data/day_1.json"
DAY2_FILENAME = "./data/day_2.json"
DAY3_FILENAME = "./data/day_3.json"


def build_graph_from_matrix(matrix):
    # points = [start] + customers
    G = nx.Graph()
    valid_points = []

    print("started validating points")
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y] is not None:
                valid_points.append((x, y))
    print(f"valid points done. There is {len(valid_points)} valid points")

    print("started adding edges")
    for (x1, y1), (x2, y2) in combinations(valid_points, 2):
        dist = abs(x1 - x2) + abs(y1 - y2)
        G.add_edge((x1, y1), (x2, y2), weight=dist)

    print("started solving traveling salesman")
    cycle = nx.approximation.traveling_salesman_problem(G, cycle=True)
    with open("out3.txt", "w") as f:
        for point in cycle:
            f.write(f"{point[0]},{point[1]}\n")  # Save as x,y coordinates

    print("TSP solution saved")


def day2():
    customers, warehouses, matrix = parse_las_brickas()
    warehouses, customers, trucks, box = parse_day(DAY2_FILENAME, warehouses, customers)

    warehouses = [warehouses[0]]
    steps = []
    steps = addAllLoadsForDay2(steps, customers)
    # print(steps)
    day2fromCycleFile(matrix, warehouses, steps)


def send_solution(obj):
    url = "https://opti.csgames.org/Solution"
    headers = {"accept": "text/plain", "Content-Type": "application/json"}

    response = requests.post(url, json=obj, headers=headers)

    if response.status_code == 200:
        print("Solution submitted successfully!")
        print("Response:", response.text)
    else:
        print("Error:", response.status_code, response.text)


def day2fromCycleFile(matrix, warehouses: list[Warehouse], steps):
    filename = "./out3.txt"

    data = np.loadtxt(filename, delimiter=",", dtype=int)

    cycle = [tuple(point) for point in data]

    x = 3525
    y = 4458
    if (x, y) not in cycle:
        print("Starting point not found in the file.")
        return None

    start_index = cycle.index((x, y))

    # Reorder the cycle starting from the found index
    ordered_cycle = cycle[start_index + 1 :] + cycle[:start_index]

    truckId = 0

    for coords in ordered_cycle:
        x, y = coords
        customer: Customer = matrix[x][y]
        addMoveToCustomerActionToAnswer(str(truckId), str(customer.id), steps)
        # print(x, y)
        for order in customer.orders:
            if order.box_id == 97 or order.box_id == 30:
                continue
            addDeliverActionToAnswer(
                str(truckId), str(order.qty), str(order.box_id), steps
            )

    addMoveToWarehouseActionToAnswer(str(truckId), str(warehouses[0].id), steps)
    obj = {
        "credentials": {"teamName": "Rouge", "password": "package-weak-those"},
        "dayNumber": 2,
        "steps": steps,
    }
    # send_solution(obj)
    with open("solution.json", "w") as f:
        json.dump(obj, f, indent=4)


def addAllLoadsForDay2(steps, customers):
    _97 = False
    orderDict = {}
    for customer in customers:
        for order in customers[customer].orders:
            if order.box_id == 30 or order.box_id -=:
                continue
            if order.box_id in orderDict:
                orderDict[order.box_id] += order.qty
            else:
                orderDict[order.box_id] = order.qty
    for legoType in orderDict:
        steps = addLoadActionToAnswer(0, orderDict[legoType], legoType, steps)
    return steps


def day1():
    # Fait a la main
    customers, warehouses, matrix = parse_las_brickas()
    warehouses, customers, trucks, box = parse_day(DAY1_FILENAME, warehouses, customers)
    print(box)


def day3():
    steps = []
    warehouses, customers, trucks, box = parse_day(DAY3_FILENAME, warehouses, customers)


def getDistManhattan(x1, y1, x2, y2):
    xDiff = abs(x2 - x1)
    yDiff = abs(y2 - y1)
    return xDiff + yDiff


def addLoadActionToAnswer(truck, quantity, lego, steps):
    steps.append(
        "load truck=" + str(truck) + " quantity=" + str(quantity) + " lego=" + str(lego)
    )
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
    day2()
    # customers, warehouses, matrix = parse_las_brickas()
    # print(warehouses)
    # build_graph_from_matrix(matrix)
