# High-Performance Data Processing with Lazy Loading and Multi-Processing

## Project Overview

This project implements an efficient data processing solution that addresses memory constraints and leverages multiprocessing capabilities.

## Key Features

- **Memory-Efficient Data Handling**
  - Utilizes lazy loading techniques to prevent complete dataset loading into memory
  - Splits loaded files into manageable chunks for processing
  - Reduces memory consumption during large dataset operations

- **Multiprocessing Architecture**
  - Implements a producer-consumer design pattern
  - Multiple producers update a shared queue
  - Single consumer fetches and processes queue data
  - Enables parallel processing and improved performance

- **Flexible Processing**
  - Configurable number of threads
  - Custom error code filtering
  - Flexible input and output file handling

## Usage Examples

### Default Run
```bash
python main.py
```
Runs the main with default settings.

### Custom Number of Threads and Threshold
```bash
python main.py --threads 8 --threshold 10
```
- Sets the number of producer threads to 8
- Sets a custom processing threshold

### Custom Error Code Filtering
```bash
python main.py --errorcodes 400 401 500 503
```
Processes only log entries with specified error codes.

### Custom Input and Output Files
```bash
python main.py --input ./logs/my_log.log --output ./results/log_analysis.csv
```
- Specifies a custom input log file
- Defines a custom output CSV file path

## Architecture

### Components
- **Producers**: Multiple processes that load and prepare data chunks
- **Queue**: Shared data structure for inter-process communication
- **Consumer**: Single process that retrieves and processes data from the queue
- **Separate Functions**: 
  - Separate functions for saving results
  - Separate functions for printing output

## Command-Line Arguments
- `--threads`: Number of producer threads (default: 12)
- `--threshold`: Processing threshold value (default: 10)
- `--errorcodes`: List of error codes to filter (default: [[400, 401, 403, 404, 405, 500, 501, 502, 503, 504, 505]])
- `--input`: Path to input log file (default: ./data/sample.log)
- `--output`: Path to output CSV file (default: ./data/output.csv)

## Performance Benefits
- Reduced memory usage
- Parallel processing
- Efficient handling of large datasets
- Flexible error code and thread configuration

## Workflow
1. Load log file in chunks
2. Produce data chunks
3. Consumer processes queue data
4. Separate functions handle:
   - Result saving
   - Result printing

