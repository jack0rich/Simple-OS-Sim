# Simple-OS-Sim
Exercises for simulating basic algorithms of an operating system.
## Page Scheduling Demo (FIFO, LRU)

This is a page scheduling simulation program that demonstrates the FIFO (First-In, First-Out) and LRU (Least Recently Used) page replacement algorithms.

### Usage

1. Download the `page_scheduling.exe` executable from the [releases](https://github.com/jack0rich/Simple-OS-Sim/releases/download/Win/page_scheduling.exe) page.
2. Open a terminal or command prompt.
3. Run the executable with the desired arguments.

```shell
page_scheduling.exe --scheduling-algorithm <algorithm> [--max-num <max_number>] [--table-len <table_length>] [--queue-len <queue_length>]
```

Replace `<algorithm>` with either "fifo" or "lru" to specify the scheduling algorithm. You can also provide optional arguments for the maximum page number, table length, and queue length.

### Arguments

- `--scheduling-algorithm`: The scheduling algorithm to use. Choose either "fifo" or "lru".

- `--max-num`: (Optional) The maximum page number. Default is 9.

- `--table-len`: (Optional) The length of the page table. Default is 4.

- `--queue-len`: (Optional) The length of the page queue. Default is 12.

### Examples

- Run the FIFO algorithm with default parameters: `page_scheduling.exe --scheduling-algorithm fifo`

- Run the LRU algorithm with custom parameters:`page_scheduling.exe --scheduling-algorithm lru --max-num 15 --table-len 5 --queue-len 20`

## License

This project is licensed under the [MIT License](https://github.com/jack0rich/Simple-OS-Sim/blob/main/LICENSE).
