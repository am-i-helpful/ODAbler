import multiprocessing
import subprocess
import json
import socket
import traceback
from opendc_experiment_runner.energy_experiments import opendc_energy_experiment_runner
from opendc_experiment_runner.anomaly_experiments import opendc_anomaly_experiment_runner

def get_multiprocessing_info():
    print("Number of cpu : ", multiprocessing.cpu_count())


def launch_odabler_experiments():
    # Create and launch process pop.py using python interpreter
    process1 = subprocess.Popen(["python", "opendc_experiment_runner/energy_experiments/opendc_experiment_runner.py"])
    process2 = subprocess.Popen(["python", "opendc_experiment_runner/random_plot.py"])

def launch_opendc_energy_experiment():
    opendc_energy_experiment_runner.analyse_energy_analysis_experiment()

def launch_opendc_anomaly_experiment():
    opendc_anomaly_experiment_runner.analyse_anomaly_analysis_experiment()

def exit_opendc_listener_server():
    print("-----------------Terminating the OpenDC listening socket instance-----------------")
    with open('key-configurations/opendc-experiment-config.json') as config_file:
        data = json.load(config_file)
        host = data['opendc-host-server']
        port = data['opendc-host-port']
        terminate_message = data['connection-termination-signal']
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.settimeout(10) # timeout - 10 seconds
            print("Sending termination message to OpenDC...")
            # print(terminate_message)
            s.sendall(bytes(terminate_message+'\n', 'utf-8'))
            data = s.recv(1024)
            print(f"Received reply to termination-related message = {data!r}")
    except Exception as e:
        print(traceback.format_exc())
    finally:
        print("---------------------ODAbler Analysis Program halted---------------------!!!")

# PyCharm hint - press the green button in the gutter to run the script.
if __name__ == '__main__':
    # get_multiprocessing_info()
    #launch_opendc_energy_experiment()
    launch_opendc_anomaly_experiment()
    # exit_opendc_listener_server()