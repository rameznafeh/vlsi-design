# Import the necessary libraries
from utils import *
import time
import datetime
import matplotlib.pyplot as plt
from minizinc import Instance, Model, Solver
import numpy as np

gecode = Solver.lookup("gecode")
model_path = 'solver.mzn'
print(os.getcwd())
# path to instances

# instances_path = os.path.join(os.getcwd(), '')

instances_path = '..//..//..//instances'
sorted_instances = alphanumeric_sort(os.listdir(instances_path))

# if debug, choose which instances to run on
debug = False
range_instances = range(3) if debug else range(len(sorted_instances))
n_solved = len(range_instances) # nb of instances successfully solved

timeout = 5  # in minutes
total_solveTime = 0

for i in range_instances: # loop over each instance
    # initialize model
    model = Model(model_path)  
    instance = Instance(gecode, model)

    # get parameters from instance file
    instance_name = sorted_instances[i]
    instance_path = os.path.join(instances_path, instance_name)
    plate_width, n_circuits, circuit_widths, circuit_heights = \
        read_instance(instance_path)     

    # lower bound is sum of circuit areas divided by width
    min_height = \
        int(sum(np.multiply(circuit_heights, circuit_widths))/plate_width)
    # upper bound = sum of circuit heights
    max_height = sum(circuit_heights)

    # display instance data
    print(f"solving {instance_name.replace('.txt', '')}")

    # initialize variables in MZ solver
    instance['plate_width'] = plate_width
    instance['n_circuits'] = n_circuits
    instance['circuit_widths'] = circuit_widths
    instance['circuit_heights'] = circuit_heights
    instance['min_height'] = min_height
    instance['max_height'] = max_height

    # time execution
    start_time = time.time()
    result = instance.solve(timeout=datetime.timedelta(minutes=timeout))
    end_time = time.time()
    elapsed_time = (end_time - start_time)
    
    # get solve time from the solver
    total_solveTime += result.statistics['solveTime'].total_seconds()

    if elapsed_time > timeout*60:  # failure
        print(f"Failure! Exceeded timeout of {timeout} min...")
        print('--------------------------')
        n_solved -= 1
    else:  # success
        print_statistics(result)  

        # get output and plot result
        x = result['x']
        y = result['y']
        plate_height = result['plate_height']
        circuits = return_circuits(circuit_widths, circuit_heights, x, y)
        save = 1
        file = f'..//out//out-{i+1}.png'
        plot_circuits(circuits, plate_width,
                      plate_height, f'{instance_name[:-4]}', save, file)
        print('--------------------------')

plt.pause(0.001)
print(f'solved instances: {n_solved}/{len(range_instances)}')
print(f'total solveTime: {total_solveTime:.3f} s')
input("Done! Press [enter] to continue.")

# challenging instances: 11, 16, 18, 19 20, 22F, 26, 30F, 31, 32, 34, 36, 37, 38
#                                                                         39, 40