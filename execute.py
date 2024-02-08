import subprocess
import time

# List of python scripts to execute
py_scripts = ["main.py", "visualize.py"]

def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode(), err.decode()

# Execute each script and measure execution time
for script in py_scripts:
    start_time = time.time()  # Start timer
    out, err = execute(f"python {script}")
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    print(f"Script {script} executed in {elapsed_time:.2f} seconds.")
    print(out)
    print(err)
    print("\n\n\n")
