import os
import re
import matplotlib.pyplot as plt
from matplotlib import patches
import matplotlib.colors as colors
import numpy as np


def read_instance(instance_path):
    # read an instance file and
    # return variables plate_width, n_circuits, circuit_widths, circuit_heights
    file = open(instance_path, "r")
    plate_width = int(file.readline())  # line 1 is plate width
    n_circuits = int(file.readline())  # line 2 is nb of circuits
    circuit_widths = []
    circuit_heights = []
    for i in range(n_circuits):  # extract x and y for each circuit
        circuit = file.readline().strip().split(" ")
        circuit_widths.append(int(circuit[0]))
        circuit_heights.append(int(circuit[1]))
    return plate_width, n_circuits, circuit_widths, circuit_heights


def alphanumeric_sort(data):
    # sort instances alphanumerically
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def return_circuits(circuit_widths, circuit_heights, start_x, start_y):
    circuits = []
    for i in range(len(start_x)):
        circuits.append(
            (circuit_widths[i], circuit_heights[i], start_x[i], start_y[i]))
    return circuits


def plot_circuits(circuits, plate_width, plate_height, title, save=0, file=''):
    fig, ax = plt.subplots()
    ax.set_title(title)
    # fig.canvas.set_window_title(title)
    fig.canvas.manager.set_window_title(title)

    for i, (w, h, x, y) in enumerate(circuits):
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='black',
                                 facecolor=colors.hsv_to_rgb((i / len(circuits), 1, 1)))
        ax.add_patch(rect)

    ax.set_xticks(np.arange(plate_width))
    ax.set_yticks(np.arange(plate_height))
    ax.grid(color='black', linewidth=1)
    if save:
        plt.savefig(file)
        plt.close()
    else:
        plt.show(block=False)


def convert_instance_to_dzn(instance_path):
    # this function could be used to feed the solver  data files instead
    # of manually passing the parameter values
    out_path = instance_path.replace(
        '\instances', '\data_files').replace('.txt', '.dzn')
    plate_width, n_circuits, circuit_widths, circuit_heights = read_instance(
        instance_path)
    # lower bound is sum of circuit areas divided by width
    min_height = \
        int(sum(np.multiply(circuit_heights, circuit_widths))/plate_width)
    # upper bound = sum of circuit heights
    max_height = sum(circuit_heights)
    with open(out_path, 'w+') as out:
        out.write(f"circuit_heights={circuit_heights};\n")
        out.write(f"circuit_widths={circuit_widths};\n")
        out.write(f"max_height={max_height};\n")
        out.write(f"min_height={min_height};\n")
        out.write(f"n_circuits={n_circuits};\n")
        out.write(f"plate_width={plate_width};\n")


def print_statistics(result):
    # prints relevant statistics to be chosen in list below
    relevant_statistics = ['failures', 
    'solveTime', 
    #'time'
    ]
    for (key, value) in result.statistics.items():
        if key in relevant_statistics:
            print(f'{key}: {value}')
