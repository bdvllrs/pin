from pin.experiments import control_randomness
from pin.sacred import Experiment
from %PROJECT_NAME%.utils.constants import PROJECT_DIR

ex = Experiment("%SCRIPT_NAME%", PROJECT_DIR,
                configs=["main.yaml"],
                source_dir=["%PROJECT_NAME%"])


@ex.automain
def %SCRIPT_NAME%(_run, _log):
    # TODO
