import subprocess

# List of python scripts to execute
py_scripts = ["main.py", "visualize.py"]

def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode(), err.decode()


# Execute each script
for script in py_scripts:
    out, err = execute(f"python {script}")
    print(out)
    print(err)
    print("\n\n\n")
