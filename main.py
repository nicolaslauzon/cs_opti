from parsers import parse_las_brickas, parse_day
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
    with open("out2.txt", "w") as f:
        for point in cycle:
            f.write(f"{point[0]},{point[1]}\n")  # Save as x,y coordinates

    print("TSP solution saved")


def day2():
    day2fromCycleFile()
    # print("started parsing")
    # customers, warehouses, matrix = parse_las_brickas()
    # print("parsed las brickas")
    # warehouses, customers, trucks, box = parse_day(DAY2_FILENAME, warehouses, customers)
    # print("parsed day 2")
    # # build_graph_from_matrix(matrix)


def day2fromCycleFile():
    filename = "./out2.txt"

    data = np.loadtxt(filename, delimiter=",", dtype=int)

    cycle = [tuple(point) for point in data]

    x = 3525
    y = 4458
    if (x, y) not in cycle:
        print("Starting point not found in the file.")
        return None

    start_index = cycle.index((x, y))

    # Reorder the cycle starting from the found index
    ordered_cycle = cycle[start_index:] + cycle[: start_index + 1]
    print(ordered_cycle)
    return ordered_cycle


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
    day2()
