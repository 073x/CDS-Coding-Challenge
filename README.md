# CDS-Coding-Challenge

## Prerequisites
- Python enviroment version >= 3.7.13

## Run
- Ensure proper user permissions.
- Command: python3 main.py

## Config Params
- KEYWORD = "CDS"
  - Search keyword, for now limited to a single keyword.

- PROBABILITY = 0.5  # 50%
  - Keyword generator probability. Possible values: 0 - 1, [0.1, 0.2 ... 0.9]

- BASE_DATA_PATH = './data'
  - Base data directory path.
  
- BASE_FILE_PATH1 = './data/file1'
  - first file path.
  
- BASE_FILE_PATH2 = './data/file2'
  - second file path.
  
- SEARCH_RESULTS_LOG_FILE_PATH = './search_logs'
  - Search log file count.
 
- CLEAR_FILES_AFTER_EVERY_SEARCH = False
  - Whether to clear the file after every search.
  
- RANDOM_STRING_LENGTH = 100
  - Length of pseudo string to generated.


- PSEUDO_GENERATOR_INTERVAL = 5
  - In Seconds. Recommandation: Keep the generator interval period smaller than monitor interval.

- MONITOR_INTERVAL = 10
  - In Seconds. Recommandation: Keep the monitor interval period greater than generator interval.
  
  
