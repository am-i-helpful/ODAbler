import multiprocessing
import subprocess
import time
import json
import socket
import traceback
from opendc_experiment_runner.energy_experiments import opendc_energy_experiment_runner
from opendc_experiment_runner.anomaly_experiments import opendc_anomaly_experiment_runner

def get_multiprocessing_info():
    print("Number of CPUs available in this system: ", multiprocessing.cpu_count())


def launch_odabler_experiments():
    # Could also create and launch multiple processes using python interpreter as commented below:
    # process1 = subprocess.Popen(["python", "opendc_experiment_runner/energy_experiments/opendc_experiment_runner.py"])
    launch_opendc_energy_experiment()
    launch_opendc_anomaly_experiment()

def launch_opendc_energy_experiment():
    print("-----------------Sending a signal to initiate the energy experiment to the OpenDC listening socket instance-----------------")
    with open('key-configurations/opendc-experiment-config.json') as config_file:
        data = json.load(config_file)
        energy_message = data['energy-experiment-analysis-signal']
        data = send_message_to_opendc_listener_server(energy_message)
        if data is not None:
            print(f"Received reply against energy-experiment-related message = {data!r}")
            time.sleep(30) # for allowing the Telegraf agent to flush data to InfluxDB in sufficient time
            # analyse_opendc_energy_experiment()
        else:
            print(f"No reply received against energy-experiment-related message!")

def launch_opendc_anomaly_experiment():
    print("-----------------Sending a signal to initiate the anomaly experiment to the OpenDC listening socket instance-----------------")
    with open('key-configurations/opendc-experiment-config.json') as config_file:
        data = json.load(config_file)
        anomaly_message = data['anomaly-experiment-analysis-signal']
        data = send_message_to_opendc_listener_server(anomaly_message)
        if data is not None or data == '':
            print(f"Received reply against anomaly-experiment-related message = {data!r}")
            time.sleep(30)  # for allowing the Telegraf agent to flush data to InfluxDB in sufficient time
            # analyse_opendc_anomaly_experiment()
        else:
            print(f"No reply received against anomaly-experiment-related message!")

def terminate_opendc_listener_connection():
    print("-----------------Sending a signal to initiate the termination of the OpenDC listening socket instance-----------------")
    with open('key-configurations/opendc-experiment-config.json') as config_file:
        data = json.load(config_file)
        terminate_message = data['connection-termination-signal']
        data = send_message_to_opendc_listener_server(terminate_message)
        # send one more client socket message to halt OpenDC socket server
        data = send_message_to_opendc_listener_server(terminate_message)
        if data is not None:
            print(f"Received reply against termination-related message = {data!r}")
        else:
            print(f"No reply received against termination-related message!")

def send_message_to_opendc_listener_server(message):
    data = None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            with open('key-configurations/opendc-experiment-config.json') as config_file:
                data = json.load(config_file)
                host = data['opendc-host-server']
                port = data['opendc-host-port']
                s.connect((host, port))
                # s.settimeout(10) # timeout - 10 seconds
                print("Sending message to OpenDC...")
                # print(terminate_message)
                s.sendall(bytes(message+'\n', 'utf-8'))
                data = s.recv(1024)
                return data
    except Exception as e:
        print(traceback.format_exc())
    finally:
        print("---------------------ODAbler communication completed with OpenDC---------------------!!!")

def analyse_opendc_energy_experiment():
    opendc_energy_experiment_runner.analyse_energy_analysis_experiment()

def analyse_opendc_anomaly_experiment():
    opendc_anomaly_experiment_runner.analyse_anomaly_analysis_experiment()


# PyCharm hint - press the green button in the gutter to run the script.
if __name__ == '__main__':
    # get_multiprocessing_info()
    # launch_odabler_experiments - launch both experiments sequentially
    launch_opendc_energy_experiment()
    # launch_opendc_anomaly_experiment()
    terminate_opendc_listener_connection()