import socket
import json
import traceback
import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import opendc_experiment_analyser.scheduler_energy_efficiency_analyser

def run_energy_analysis_experiment():
    print("-----------------Running the energy experiment-----------------")
    with open('../../key-configurations/opendc-experiment-config.json') as config_file:
        data = json.load(config_file)
        host = data['opendc-host-server']
        port = data['opendc-host-port']
        energy_message = data['energy-experiment-analysis-signal']
        terminate_message = data['connection-termination-signal']
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.settimeout(10) # timeout - 10 seconds
            print("Connection succeeded!")
            print(energy_message)
            s.sendall(bytes(energy_message+'\n', 'utf-8'))
            data = s.recv(1024)
            print(f"Received reply to energy-experiment-related message = {data!r}")

    except Exception as e:
        print(traceback.format_exc())
    finally:
        print("ODAbler Analysis Program halted!!!")

def analyse_energy_analysis_experiment():
    base_dir = '/opendc_experiment_analyser/scheduler_energy_efficiency_analyser/'
    filename = 'energy_analysis.ipynb'
    with open(sys.path[0] + base_dir + filename) as ff:
        nb_in = nbformat.read(ff, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    # nb_out = ep.preprocess(nb_in)
    ep.preprocess(nb_in) #, {'metadata': {'path': 'notebooks/'}})
    with open(sys.path[0] + base_dir + 'generated_notebooks/executed_notebook_energy.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(nb_in, f)


if __name__ == '__main__':
    run_energy_analysis_experiment()