import socket
import json
import traceback
import nbformat
import sys
from nbconvert.preprocessors import ExecutePreprocessor
import opendc_experiment_analyser.node_performance_anomaly_analyser


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
    analyse_anomaly_analysis_experiment()