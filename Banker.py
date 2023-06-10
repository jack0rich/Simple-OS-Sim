"""
Sim System Class
"""

import os
import time
import secrets
import numpy as np
from rich.text import Text
from rich.table import Table
from rich.console import Console

MAX_TIME = 5
NUM_RESOURCES = 4
MAX_RESOURCE = 13
MIN_RESOURCE = 6
RESOURCE_NAMES = ('A', 'B', 'C', 'D')


def random_vector_element(vector, max_, min_):
    for i in range(len(vector)):
        vector[i] = secrets.randbelow(max_ - min_ + 1) + min_


def creat_resource_vector(max, min):
    vector = np.zeros(NUM_RESOURCES, dtype=int)
    random_vector_element(vector, max, min)
    return vector


def vector_to_str(vector):
    return ' '.join([str(i) for i in vector])


class Process:
    def __init__(self, system_owned: np.ndarray):
        self.max_vector = np.zeros(NUM_RESOURCES, dtype=int)
        self.allocation = np.zeros(NUM_RESOURCES, dtype=int)
        self.__create_max(self.max_vector, system_owned)
        self.need_time = secrets.randbelow(MAX_TIME) + 1
        self.released = False

    def __create_max(self, target, owned, diff=2):
        for i in range(NUM_RESOURCES):
            target[i] = secrets.randbelow(int(owned[i] - (diff - 1)))

    def create_allocation(self, available):
        suitable = []
        for i in range(len(RESOURCE_NAMES)):
            suitable.append(available[i] if available[i] <= self.max_vector[i]
                            else self.max_vector[i])
        self.__create_max(self.allocation, suitable, diff=0)

    def need(self):
        return self.max_vector - self.allocation

    def is_finish(self):
        if self.need().sum() == 0:
            return True
        else:
            return False

    def release(self):
        if self.released:
            return True
        else:
            self.released = True
            return False

    def __getitem__(self, item: str):
        try:
            return self.max_vector[RESOURCE_NAMES.index(item)]
        except IndexError:
            print(f"{str} NOT IN RESOURCE_NAMES({RESOURCE_NAMES})")


class SystemEnvironment:
    def __init__(self, resources_dict: tuple, num_processes=5):
        self.resources_dict = resources_dict
        self.system_owned_resources = creat_resource_vector(MAX_RESOURCE, MIN_RESOURCE)
        self.__available = self.system_owned_resources.copy()
        self.num_processes = num_processes
        self.processes_list = []
        self.__creat_process()

    def __creat_process(self):
        for i in range(self.num_processes):
            temp_p = Process(self.system_owned_resources)
            temp_p.create_allocation(self.__available)
            self.__available -= temp_p.allocation
            self.processes_list.append(temp_p)

    def available(self):
        return self.__available

    def finished(self):
        finished = 0
        for i in self.processes_list:
            if i.is_finish():
                finished += 1

        if finished == self.num_processes:
            return True
        else:
            return False

    def visualization_banker(self):
        console = Console()
        console.print(self.display())
        while not self.finished():
            time.sleep(0.8)
            safe = False
            for p in self.processes_list:
                if p.is_finish() and p.released:
                    safe = True
                    continue
                elif p.is_finish() and not p.released:
                    safe = True
                    self.__available += p.allocation
                    p.release()
                    continue
                else:
                    is_suitable = self.__available >= p.need()
                    if False not in is_suitable:
                        safe = True
                        self.__available += p.allocation
                        p.release()
                        p.allocation += p.need()
                    else:
                        continue

            if not safe:
                console.print(Text("NOT SAFE!!!", style="bold red"))
                break

        console.print(self.display())
        print()

    def display(self) -> Table:
        table = Table(title=f'SYSTEM_OWNED: {vector_to_str(self.system_owned_resources)}'
                            f'\nAVAILABLE: {vector_to_str(self.__available)}', title_style='blue')
        table.add_column('Processes', justify='left', style='cyan')
        table.add_column('Max', justify='center', style='green')
        table.add_column('Allocation', justify='center', style='green')
        table.add_column('Need', justify='center', style='green')
        table.add_column('Finish', justify='center', style='green')
        table.add_row(' _____', 'A B C D', 'A B C D', 'A B C D', '_____')
        for i in range(self.num_processes):
            table.add_row(f'P{i}',
                          vector_to_str(self.processes_list[i].max_vector),
                          vector_to_str(self.processes_list[i].allocation),
                          vector_to_str(self.processes_list[i].need()),
                          "[blue]SUCCESS" if self.processes_list[i].is_finish() else "[red]False"
                          )
        return table


if __name__ == '__main__':
    sys = SystemEnvironment(RESOURCE_NAMES, num_processes=4)
    sys.visualization_banker()
    input("Press Enter to exit...")
