# PlotPing
Plot ping response time for a website in a graph for monitoring.

## Features

- Real-time plotting of ping times.
- Saves ping data to a CSV file for persistence.
- Configurable number of records to load and display.
- Automatically installs required packages (`pandas` and `matplotlib`).

## Requirements

- Python 3.x
- Internet connection (for pinging the host and installing packages)

## Installation

The script will automatically install the required packages (`pandas` and `matplotlib`) if they are not already installed.

## Usage

### Command Line Arguments

- `host` (str): The address to ping.
- `--data-file` (str): The file to save and load ping data (default: `ping_data.csv`).
- `--load-all`: Load all records from the data file.
- `--num-records` (int): Number of records to load from the data file.
- `--max-records` (int): Maximum number of records to keep in memory (default: 3600).

### Example

```bash
python3 live_ping_plotter.py google.com --data-file=my_ping_data.csv --num-records=1000 --max-records=5000
```

#### Without Arguments

```sh
python3 live_ping_plotter.py google.com
```

By default, this will load the last 3600 records from ping_data.csv and keep a maximum of 3600 records in memory.

## Script Details

##### Function: install_packages

Ensures that the required packages (pandas and matplotlib) are installed. If they are not installed, the function installs them using pip.

##### Function: collect_ping_data

Pings the specified host and returns the ping time in milliseconds.

##### Argument Parsing

Handles command-line arguments for specifying the host to ping, the data file to use, and other configurations.

##### Data Loading

Loads existing ping data from the specified file. If the file does not exist, it initializes an empty DataFrame.

##### Plot Setup

Initializes the plot for real-time updating.

##### Function: init

Initializes the plot with limits based on existing data if available.

##### Function: update

Updates the plot with new ping data, limits the DataFrame to the specified number of records, and saves the data to a CSV file.

##### FuncAnimation

Animates the plot by repeatedly calling the update function.

## License

This project is licensed under the MIT License.
