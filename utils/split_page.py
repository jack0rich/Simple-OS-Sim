"""
sim
"""

import os
import time
import secrets
from rich.console import Console
from rich.table import Table


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class LRUWeight:
    def __init__(self, page_num: int, weight=0):
        self.page_num = page_num
        self.weight = weight

    def used(self):
        self.weight += 1


def sort_dict_by_values(dictionary):
    sorted_dict = sorted(dictionary.items(), key=lambda x: x[1])
    sorted_keys = [item[0] for item in sorted_dict]
    print(sorted_dict)
    return sorted_keys


def print_list_with_highlight(lst, index):
    console = Console()
    for i, item in enumerate(lst):
        if i == index:
            console.print(f"{item}", style="blink bold red underline on white", end="\t")
        else:
            console.print(f"{item}", end="\t")


class PageTable:
    def __init__(self, block_len: int = 2048, table_len=5):
        self.page_table = {
            'page_num': [],
            'is_in_memory': [],
            'block_num': [],
            'Location_on_disk': []
        }
        self.keys = tuple(self.page_table.keys())
        self.block_len = block_len
        self.table_len = table_len

    def append(self, element: (tuple, list)):
        if len(self)+1 > self.table_len:
            return False
        self.examine_element(element)
        for i, key in enumerate(self.keys):
            self.page_table[key].append(element[i])
        self.examine()
        return True

    def pop(self, page_num: int):
        if not self.is_page_in(page_num):
            raise IndexError(f"Page_num [{page_num} is not in the page table]")
        index = self.page_table[self.keys[0]].index(page_num)
        for key in self.keys:
            self.page_table[key].pop(index)
        self.examine()

    def is_page_in(self, page_num: int):
        if page_num in self.page_table[self.keys[0]]:
            return True
        else:
            return False

    def examine(self):
        for key in self.keys[1:]:
            if len(self.page_table[key]) != len(self.page_table[self.keys[0]]):
                raise Exception(f'The page table is not aligned with it \n{self.page_table}')
        return True

    def examine_element(self, element: (tuple, list)):
        if len(element) != 4:
            raise Exception(f"Iterative value of incorrect length({len(element)})")
        temp = (int, bool, int, int)
        for i, expected_type in enumerate(temp):
            if not isinstance(element[i], expected_type):
                raise Exception("Element type wrong")

    def __len__(self):
        self.examine()
        return len(self.page_table[self.keys[0]])

    def display(self):
        self.examine()
        table = Table()
        table.add_column("PAGE_NUM", justify="center", style="cyan", no_wrap=True)
        table.add_column("SIGN", style="magenta", justify="center")
        table.add_column("BLOCK_NUM", justify="center", style="cyan", no_wrap=True)
        table.add_column("LOCATION_ON_DISK", justify="center", style="cyan", no_wrap=True)
        length = len(self)
        for index in range(length):
            table.add_row(
                str(self.page_table[self.keys[0]][index]),
                str(self.page_table[self.keys[1]][index]),
                str(self.page_table[self.keys[2]][index]),
                str(self.page_table[self.keys[3]][index]),
            )

        Console().print(table)

    def __str__(self):
        return None


def creat_page_queue(queue_len: int, max_page_num=7):
    queue = []
    for i in range(queue_len):
        random_page_num = secrets.randbelow(max_page_num)
        queue.append(random_page_num)

    return queue


class PageScheduling:
    def __init__(self, block_len: int = 512, queue_len: int = 12, table_len: int = 5, max_num: int = 16):
        self.page_table = PageTable(block_len=block_len, table_len=table_len)
        self.page_queue = creat_page_queue(queue_len, max_page_num=max_num)
        self.__block_len = self.page_table.block_len

    def FIFO(self):
        ph_table = []
        for i, page in enumerate(self.page_queue):
            clear_console()
            self.page_table.display()
            print_list_with_highlight(self.page_queue, i)
            time.sleep(1)
            if not self.page_table.is_page_in(page):
                page_info = (page, True, page, page * self.__block_len)
                if self.page_table.append(page_info):
                    ph_table.append(page)
                else:
                    self.page_table.pop(ph_table.pop(0))
                    if self.page_table.append(page_info):
                        ph_table.append(page)
                    else:
                        raise Exception("Somthing error when page table is full!")

            clear_console()
            self.page_table.display()
            print_list_with_highlight(self.page_queue, i)
            time.sleep(1)

    def LRU(self):
        ph_table = {}
        for i, page in enumerate(self.page_queue):
            clear_console()
            self.page_table.display()
            print_list_with_highlight(self.page_queue, i)
            time.sleep(1)
            if not self.page_table.is_page_in(page):
                page_info = (page, True, page, page * self.__block_len)
                if self.page_table.append(page_info):
                    ph_table[page] = 0
                else:
                    sorted_dict = sort_dict_by_values(ph_table)
                    del ph_table[sorted_dict[0]]
                    self.page_table.pop(sorted_dict[0])
                    if self.page_table.append(page_info):
                        ph_table[page] = 0
                    else:
                        raise Exception("Somthing error when page table is full!")
            else:
                ph_table[page] += 1

            clear_console()
            self.page_table.display()
            print_list_with_highlight(self.page_queue, i)
            time.sleep(1)


if __name__ == '__main__':
    demo = PageScheduling(table_len=4, max_num=9)
    demo.LRU()



