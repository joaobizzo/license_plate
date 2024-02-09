import subprocess
import time
from util import choose_folder




# List of python scripts to execute
py_scripts = ["main.py", "visualize.py"]

def execute(command, input_data):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = process.communicate(input_data.encode())
    return out.decode(), err.decode()

# Execute each script and measure execution time
for script in py_scripts:
    start_time = time.time()  # Start timer
    # Pass input data to the script (replace "your_input_data" with your actual input)
    out, err = execute(f"python {script}")
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    print(f"Script {script} executed in {elapsed_time:.2f} seconds.")
    print("\n\n\n")
