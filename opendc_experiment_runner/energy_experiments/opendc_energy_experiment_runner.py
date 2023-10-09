import socket
import json
import traceback
import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import opendc_experiment_analyser.scheduler_energy_efficiency_analyser

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
    analyse_energy_analysis_experiment()