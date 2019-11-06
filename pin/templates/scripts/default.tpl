from pin.experiments import control_randomness
from pin.sacred import init_and_get_experiment
from %PROJECT_NAME%.utils.constants import PROJECT_DIR

ex = init_and_get_experiment(exp_name="%SCRIPT_NAME%",
                             project_directory=PROJECT_DIR,
                             configs=["main.yaml"])


@ex.automain
def %SCRIPT_NAME%(_run, _seed, _log):
    # Set randomness
    control_randomness(_seed)

    # TODO
