from pin.experiments import control_randomness, set_cuda_device
from pin.sacred import init_and_get_experiment
from %PROJECT_NAME%.utils.constants import PROJECT_DIR

ex = init_and_get_experiment(exp_name="%SCRIPT_NAME%",
                             project_directory=PROJECT_DIR,
                             configs=["main.yaml"])


@ex.automain
def %SCRIPT_NAME%(_run, _seed, _log, cuda, cuda_device):
    # Set randomness
    control_randomness(_seed)
    # Set available cuda devices to use
    set_cuda_device(cuda_device)

    # TODO
