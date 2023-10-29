import os
import json
import traceback
import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import glob
import opendc_experiment_analyser.scheduler_energy_efficiency_analyser

def analyse_energy_analysis_experiment():
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    base_dir = os.getcwd() + '/../../opendc_experiment_analyser/scheduler_energy_efficiency_analyser/'
    print(base_dir)
    os.chdir(base_dir)
    file_notebooks = glob.glob("*")
    file_notebooks = [f for f in file_notebooks if os.path.isfile(f)]
    # filename = 'energy_analysis.ipynb'
    for file_name in file_notebooks:
        # consider only Python notebooks in case of repeated running
        if file_name.endswith('.ipynb'):
            print("File found = " + file_name)
            with open(file_name) as ff:
                nb_in = nbformat.read(ff, as_version=4)
            # nb_out = ep.preprocess(nb_in)
            ep.preprocess(nb_in) #, {'metadata': {'path': 'notebooks/'}})
            with open(os.getcwd() + '/generated_notebooks/' + file_name, 'w', encoding='utf-8') as f:
                nbformat.write(nb_in, f)


if __name__ == '__main__':
    analyse_energy_analysis_experiment()