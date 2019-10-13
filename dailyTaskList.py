import csv
import random
import sys
import time
from matplotlib import pyplot as plt
from typing import List

class DailyTaskList:

    def __init__(self, file_string: str, dims: int):
        item_delimiter = "\n"
        nice_delimiter = ":"
        if len(file_string) > 32_767:
            print("This list is too long for my preference. To fix, have a less ambitious to-do list, you dunce.")
            exit()
        
        items = file_string.split(item_delimiter)
        items = [tuple(item.split(nice_delimiter)[::-1]) for item in items]
        self.items = items
        self.dims = dims
        self.item_coords = self._items_to_Nd_space()
    
    def __call__(self):
        print(self.items)
    
    def _items_to_Nd_space(self):
        item_coords = {(item[1],*item[0].strip().split(",")) for item in self.items}
        return item_coords

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        file_string = f.read()
    tasks = DailyTaskList(file_string, 3)
    item_locations = {}
    for item in tasks.item_coords:
        item_name, coords = item[0], item[1:]
        coords = [int(coord) for coord in coords]
        item_locations[item_name] = coords
    closest = sorted([(key, value) for key, value in item_locations.items()], key=lambda tup: sum(tup[1]))
    arr1, arr2 = [], []
    for ind, k in enumerate(closest):
        if ind % 2 == 0:
            arr1.append((ind, k[0]))
        else:
            arr2.append((ind, k[0]))
    total_schedule =  arr2 + arr1 if random.randint(0,5) > 3 else arr1 + arr2 
    for ind, task in enumerate(total_schedule):
        if ind != 0:
            chance = random.randint(0,5)
            if chance > 3:
                total_schedule[ind], total_schedule[ind - 1]= total_schedule[ind - 1], total_schedule[ind]
    osc = []
    tot_time = 0
    for i in range(len(total_schedule)):
        to_append = total_schedule[-i] if i % 2 == 1 else total_schedule[i]
        minutes = random.randint(30,60)
        tot_time += minutes
        osc.append((to_append, minutes))

    # [print(task) for task in osc]
    print(tot_time)
    cumul = 0
    cumul_queue = []
    for task in osc:
        task_length = task[1]
        cumul += task_length
        cumul_queue.append((task,cumul))
    # [print(task) for task in cumul_queue]
    for minute in range(cumul):
        for task in cumul_queue:
            end_time = task[1]
            if minute <= end_time:
                print(task[0][0]," ~ ",task[1]-minute,"minutes remaining.")
                break
        time.sleep(60)
