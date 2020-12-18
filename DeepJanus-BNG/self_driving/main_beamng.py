
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path

#sys.path.insert(0, r'C:\DeepHyperion-BNG')
#sys.path.append(os.path.dirname(os.path.dirname(os.path.join(__file__))))
path = Path(os.path.abspath(__file__))
# This corresponds to DeepHyperion-BNG
sys.path.append(str(path.parent))
sys.path.append(str(path.parent.parent))

from self_driving.beamng_problem import BeamNGProblem
from core import nsga2
from core.archive_impl import SmartArchive
from self_driving.beamng_config import BeamNGConfig


config = BeamNGConfig()

problem = BeamNGProblem(config, SmartArchive(config.ARCHIVE_THRESHOLD))

if __name__ == '__main__':
    nsga2.main(problem)
    print('done')

    plt.ioff()
    plt.show()
