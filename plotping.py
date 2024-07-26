import os
import subprocess
import sys

# Function to install required packages
def install_packages():
    required_packages = ["pandas", "matplotlib"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required packages
install_packages()

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse

# Function to collect ping data
def collect_ping_data(host):
    """
    Ping the specified host and return the ping time.
    
    Parameters:
    host (str): The address to ping.

    Returns:
    float: The ping time in milliseconds, or None if the ping failed.
    """
    response = os.popen(f"ping -c 1 {host}").read()
    if "time=" in response:
        ping_time = float(response.split("time=")[-1].split(" ms")[0])
        return ping_time
    else:
        return None

# Parse command line arguments
parser = argparse.ArgumentParser(description='Live ping plotter.')
parser.add_argument('host', type=str, help='The address to ping')
parser.add_argument('--data-file', type=str, default='ping_data.csv', help='File to save and load ping data')
parser.add_argument('--load-all', action='store_true', help='Load all records from the data file')
parser.add_argument('--num-records', type=int, help='Number of records to load from the data file')
parser.add_argument('--max-records', type=int, default=3600, help='Maximum number of records to keep in memory')
args = parser.parse_args()

# Load the data file if it exists
data_file = args.data_file

if os.path.exists(data_file):
    if args.load_all:
        df = pd.read_csv(data_file, parse_dates=['timestamp'])
    elif args.num_records:
        df = pd.read_csv(data_file, parse_dates=['timestamp']).tail(args.num_records)
    else:
        df = pd.read_csv(data_file, parse_dates=['timestamp']).tail(args.max_records)
else:
    df = pd.DataFrame(columns=['timestamp', 'ping_time'])

# Set up the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], '-')

def init():
    """
    Initialize the plot with limits based on existing data if available.
    
    Returns:
    line: The line object to be updated.
    """
    if not df.empty:
        ax.set_xlim(df['timestamp'].min(), df['timestamp'].max() + pd.Timedelta(seconds=10))
        ax.set_ylim(0, df['ping_time'].max() + 10)
    else:
        ax.set_xlim(pd.Timestamp.now(), pd.Timestamp.now() + pd.Timedelta(seconds=120))
        ax.set_ylim(0, 100)
    return line,

def update(frame):
    """
    Update the plot with new ping data.
    
    Parameters:
    frame: The current frame number (ignored).

    Returns:
    line: The updated line object.
    """
    global df
    timestamp = pd.Timestamp.now()
    ping_time = collect_ping_data(args.host)
    
    if ping_time is not None:
        new_data = pd.DataFrame({'timestamp': [timestamp], 'ping_time': [ping_time]})
        df = pd.concat([df, new_data], ignore_index=True)
        
        # Limit the number of records to max_records
        if len(df) > args.max_records:
            df = df.tail(args.max_records)
        
        # Save data to CSV file
        df.to_csv(data_file, index=False)
        
        line.set_data(df['timestamp'], df['ping_time'])
        ax.set_xlim(df['timestamp'].min(), df['timestamp'].max() + pd.Timedelta(seconds=10))
        ax.set_ylim(0, df['ping_time'].max() + 10)
    
    return line,

ani = FuncAnimation(fig, update, init_func=init, interval=1000, cache_frame_data=False, save_count=args.max_records)

plt.xlabel('Timestamp')
plt.ylabel('Ping Time (ms)')
plt.title(f'Live Ping Time Graph for {args.host}')
plt.show()
