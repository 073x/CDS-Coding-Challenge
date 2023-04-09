import secrets
import threading
import time
import random
import re
import os
import logging
import string
from typing import Callable
from datetime import datetime

file_time = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')

KEYWORD = "CDS"
PROBABILITY = 0.5  # 50%
BASE_DATA_PATH = './data'
BASE_FILE_PATH1 = f'{BASE_DATA_PATH}/file1_{file_time}'
BASE_FILE_PATH2 = f'{BASE_DATA_PATH}/file2_{file_time}'
SEARCH_RESULTS_LOG_FILE_PATH = './search_logs'
CLEAR_FILES_AFTER_EVERY_SEARCH = False
RANDOM_STRING_LENGTH = 100

# In Seconds. Recommandation: Keep the generator interval period smaller than monitor interval.
PSEUDO_GENERATOR_INTERVAL = 5
# In Seconds. Recommandation: Keep the monitor interval period greater than generator interval.
MONITOR_INTERVAL = 10


def path_exists(path: str) -> bool:
    return os.path.exists(path)


def file_exists(file_path: str) -> bool:
    return path_exists(file_path) and os.path.isfile(file_path)


def write_file(file_path: str, write_data: str, mode: str = "w", force: bool = False) -> bool:
    write_success = False
    if force or file_exists(file_path):
        try:
            with open(file_path, mode) as outfile:
                outfile.write(write_data)
                write_success = True
        except IOError:
            print('IO exception while writing the file.')
        except Exception as e:
            print('Exception while writing a file. details', e)
    return write_success


def read_file(file_path: str, process_data: Callable[[str], int], mode: str = "r") -> int:
    if file_exists(file_path):
        try:
            with open(file_path, mode) as infile:
                count = 0
                for line in infile:
                    count += process_data(line)

        except IOError:
            print('IO exception while reading the file.')
        except Exception as e:
            print('Exception while reading a file. details', e)

        return count
    return 0


# Specific helper functions


def write_file1(write_data: str, mode: str = "a", force: bool = False) -> bool:
    return write_file(BASE_FILE_PATH1, write_data, mode, force)


def write_file2(write_data: str, mode: str = "a", force: bool = False) -> bool:
    return write_file(BASE_FILE_PATH2, write_data, mode, force)


def write_log(write_data: str, mode: str = "a", force: bool = False) -> bool:
    return write_file(SEARCH_RESULTS_LOG_FILE_PATH, write_data, mode, force)


def read_file1(process_data: Callable[[str], int], mode: str = "r") -> str:
    return read_file(BASE_FILE_PATH1, process_data, mode)


def read_file2(process_data: Callable[[str], int], mode: str = "r") -> str:
    return read_file(BASE_FILE_PATH2, process_data, mode)


def ensure_file() -> None:
    if not path_exists(BASE_DATA_PATH):
        print(
            f'Base Data Directory: {BASE_DATA_PATH} does not exists. Creating data directory: {BASE_DATA_PATH}')
        os.mkdir(BASE_DATA_PATH)
        print(f'Created data directory: {BASE_DATA_PATH}')

    if not file_exists(BASE_FILE_PATH1):
        print(
            f'File 1: {BASE_FILE_PATH1} does not exists. Creating base file 1: {BASE_FILE_PATH1}')
        write_file1("File Initialized: {file_name} \n\n".format(
            file_name=BASE_FILE_PATH1), "w", True)
        print(f'Created base file 1: {BASE_FILE_PATH1}')

    if not file_exists(BASE_FILE_PATH2):
        print(
            f'File 2: {BASE_FILE_PATH2} does not exists. Creating base file 2: {BASE_FILE_PATH2}')
        write_file2("File Initialized: {file_name} \n\n".format(
            file_name=BASE_FILE_PATH2), "w", True)
        print(f'Created base file 2: {BASE_FILE_PATH2}')

    if not file_exists(SEARCH_RESULTS_LOG_FILE_PATH):
        print(
            f'Log file: {SEARCH_RESULTS_LOG_FILE_PATH} does not exists. Creating search log file: {SEARCH_RESULTS_LOG_FILE_PATH}')
        write_log("File Initialized: {file_name} \n\n".format(
            file_name=SEARCH_RESULTS_LOG_FILE_PATH), "w", True)
        print(f'Created search log file: {SEARCH_RESULTS_LOG_FILE_PATH}')


def pseudo_random_string() -> str:
    return KEYWORD + " " + "".join(random.choices(KEYWORD + string.ascii_uppercase + string.ascii_lowercase + string.digits + " ", k=RANDOM_STRING_LENGTH-len(KEYWORD))) + " \n" if random.random() < PROBABILITY else "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + " ", k=RANDOM_STRING_LENGTH)) + "\n"


def find_keyword(data: str) -> int:
    return len(re.findall(r"\b{keyword}\b".format(keyword=KEYWORD), data))


# Random data generator
def generate_random_strings() -> None:
    while True:

        write_file1(pseudo_random_string())
        write_file2(pseudo_random_string())

        time.sleep(PSEUDO_GENERATOR_INTERVAL)

# File monitoring system


def monitor_files() -> None:
    while True:
        kw_cnt_file1 = read_file1(find_keyword)
        kw_cnt_file2 = read_file2(find_keyword)
        time_now = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')

        if kw_cnt_file1 > 0 and kw_cnt_file2 > 0:
            write_log(
                f"file1.txt : {time_now} - Count: {kw_cnt_file1}\nfile2.txt : {time_now} - Count: {kw_cnt_file2}\n")
        elif kw_cnt_file1 > 0:
            write_log(
                f"file1.txt : {time_now} - Count {kw_cnt_file1}\n")
        elif kw_cnt_file2 > 0:
            write_log(
                f"file2.txt : {time_now} - Count {kw_cnt_file2}\n")

        time.sleep(MONITOR_INTERVAL)


def main() -> None:
    ensure_file()

    generator_thread = threading.Thread(target=generate_random_strings)
    monitor_thread = threading.Thread(target=monitor_files)

    print("Processing...")

    generator_thread.start()
    monitor_thread.start()


if __name__ == '__main__':
    main()
