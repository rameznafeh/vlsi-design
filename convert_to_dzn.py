import os
from utils import *

instances_path = os.path.join(os.getcwd(), 'instances')
sorted_instances = alphanumeric_sort(os.listdir(instances_path))

for i in range(len(sorted_instances)):
    inst = sorted_instances[i]
    instance_path = os.path.join(instances_path, inst)
    convert_instance_to_dzn(instance_path)