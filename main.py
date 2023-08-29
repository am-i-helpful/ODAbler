import multiprocessing
import subprocess

def get_multiprocessing_info():
    print("Number of cpu : ", multiprocessing.cpu_count())


def launch_odabler_processes():
    process1 = subprocess.Popen(["python", "opendc-metrics/opendc-metrics.py"])  # Create and launch process pop.py using python interpreter
    process2 = subprocess.Popen(["python", "opendc-metrics/random_plot.py"])

# PyCharm hint - press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_multiprocessing_info()