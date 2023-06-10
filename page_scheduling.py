"""
Page Scheduling Demo
"""

import argparse
from utils.split_page import PageScheduling

parser = argparse.ArgumentParser(
    description="Page Scheduling Demo (FIFO, LRU)."
)

parser.add_argument(
    "--scheduling-algorithm", type=str, required=True, help="In ['fifo', 'lru']."
                                                          " FIFO page replacement algorithm or "
                                                          "LRU replacement algorithm."
)

parser.add_argument(
    "--max-num", type=int, default=9, help="Maximum page number"
)

parser.add_argument(
    "--table-len", type=int, default=4, help="The length of the page table."
)

parser.add_argument(
    "--queue-len", type=int, default=12, help="The length of the page queue."
)


if __name__ == '__main__':
    args = parser.parse_args()
    scheduling = args.scheduling_algorithm
    demo = PageScheduling(
        max_num=args.max_num,
        table_len=args.table_len,
        queue_len=args.queue_len,
    )

    if scheduling.lower() == 'fifo':
        demo.FIFO()
    elif scheduling.lower() == 'lru':
        demo.LRU()
    else:
        raise Exception(f"{scheduling} is not an expected argument!")

