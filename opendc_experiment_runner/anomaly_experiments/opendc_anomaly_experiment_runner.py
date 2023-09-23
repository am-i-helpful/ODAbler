import socket
import json
import traceback
import nbformat
import sys
from nbconvert.preprocessors import ExecutePreprocessor
import opendc_experiment_analyser.node_performance_anomaly_analyser

def run_anomaly_analysis_experiment():
    print("-----------------Running the performance anomaly experiment-----------------")
    with open('../../key-configurations/opendc-experiment-config.json') as config_file:
        data = json.load(config_file)
        host = data['opendc-host-server']
        port = data['opendc-host-port']
        anomaly_message = data['anomaly-experiment-analysis-signal']
        terminate_message = data['connection-termination-signal']
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.settimeout(10) # timeout - 10 seconds
            print("Connection succeeded!")
            print(anomaly_message)
            s.sendall(bytes(terminate_message+'\n', 'utf-8'))
            data = s.recv(1024)
            print(f"Received reply to anomaly-experiment-related message = {data!r}")

    except Exception as e:
        print(traceback.format_exc())
    finally:
        print("ODAbler Analysis Program halted!!!")


def analyse_anomaly_analysis_experiment():
    # running python notebook from python script - https://stackoverflow.com/a/68720825/3482140,
    # docs - https://nbconvert.readthedocs.io/en/latest/execute_api.html
    base_dir = '/opendc_experiment_analyser/node_performance_anomaly_analyser/'
    filename = 'anomaly_analysis.ipynb'
    with open(sys.path[0] + base_dir + filename) as ff:
        nb_in = nbformat.read(ff, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    # nb_out = ep.preprocess(nb_in)
    ep.preprocess(nb_in) #, {'metadata': {'path': 'notebooks/'}})
    with open(sys.path[0] + base_dir + 'generated_notebooks/executed_notebook_anomaly.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(nb_in, f)

if __name__ == '__main__':
    run_anomaly_analysis_experiment()