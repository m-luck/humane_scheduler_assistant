# Author: Michael Lukiman
import csv
import random
import sys
import time
from matplotlib import pyplot as plt
from typing import List

class DailyTaskList:

    # TODO: Add interrupt time checks.

    def print_tasks(self):
        [print(task) for task in self.cumul_queue]

    def start(self):
        for minute in range(self.cumul):
            for task in self.cumul_queue:
                end_time = task[1]
                if minute <= end_time:
                    print(task[0][0]," ~ ",task[1]-minute,"minutes remaining.")
                    break
            time.sleep(60)

    def print_dimensions(self):
        print(self.dim_description)

    def __init__(self, file_string: str, dims: int, dim_description: str = "(PRIO, REWARD, COMPOUND)", bottom=30, upper=60):
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
        self._incorporate_ignored_lines()
        self._generate_closest()
        self._separate_into_two_arrs()
        self._make_total_arr()
        self._oscillate_selection()
        self.cumul = self._convert_to_cumulative()
        self.bottom = bottom
        self.upper = upper
    
    def __call__(self):
        print(self.items)
    
    def _items_to_Nd_space(self):
        item_coords = {(item[1],*item[0].strip().split(",")) for item in self.items}
        return item_coords

    def _incorporate_ignored_lines(self):
        self.item_locations = {}
        self.item_fixed_point_interrupts = []
        for item in self.item_coords:
            item_name, coords = item[0], item[1:]
            if item_name[0] == '*':
                self.item_fixed_point_interrupts.append()
            if item_name[0] == '#':
                continue
            coords = [int(coord) for coord in coords]
            self.item_locations[item_name] = coords

    def _generate_closest(self):
        self.closest = sorted([(key, value) for key, value in self.item_locations.items()], key=lambda tup: sum(tup[1]))

    def _separate_into_two_arrs(self):
        self.arr1, self.arr2 = [], []
        for ind, k in enumerate(self.closest):
            if ind % 2 == 0:
                self.arr1.append((ind, k[0]))
            else:
                self.arr2.append((ind, k[0]))
    
    def _make_total_arr(self):
        self.total_schedule =  self.arr2 + self.arr1 if random.randint(0,5) > 3 else self.arr1 + self.arr2 
        for ind, task in enumerate(self.total_schedule):
            if ind != 0:
                chance = random.randint(0,5)
                if chance > 4:
                    self.total_schedule[ind], self.total_schedule[ind - 1]= self.total_schedule[ind - 1], self.total_schedule[ind]

    def _oscillate_selection(self):
        self.osc = []
        self.tot_time = 0
        i, j = 0, len(self.total_schedule)-1
        while i <= j:
            if i != j:
                to_append = self.total_schedule[i]
                minutes = random.randint(self.bottom,self.upper)
                self.tot_time += minutes
                self.osc.append((to_append, minutes))
                i+=1

            to_append = self.total_schedule[j]
            minutes = random.randint(self.bottom,self.upper)
            self.tot_time += minutes
            self.osc.append((to_append, minutes))
            j-=1
        print(len(self.osc))

    def _convert_to_cumulative(self):
        print(self.tot_time)
        cumul = 0
        self.cumul_queue = []
        for task in self.osc:
            task_length = task[1]
            cumul += task_length
            self.cumul_queue.append((task,cumul))
        return cumul
            
    
if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        file_string = f.read()
    tasks = DailyTaskList(file_string, 3)
    # tasks.print_tasks() # Uncomment if we want to spoil the fun.
    tasks.start()

    
