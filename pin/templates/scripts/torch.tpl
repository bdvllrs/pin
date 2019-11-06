import torch
from pin.experiments import control_randomness
from pin.sacred import init_and_get_experiment
from %PROJECT_NAME%.utils.constants import PROJECT_DIR

ex = init_and_get_experiment(exp_name="%SCRIPT_NAME%",
                             project_directory=PROJECT_DIR,
                             configs=["main.yaml"])


@ex.automain
def %SCRIPT_NAME%(_run, _seed, _log, cuda):
    # Set randomness
    control_randomness(_seed)

    device = torch.device('cpu')
    if cuda and torch.cuda.is_available():
        print("Using CUDA.")
        device = torch.device('cuda')

    # TODO
