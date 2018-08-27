from enum import Enum, unique

import luigi

from ob_pipelines import LoggingTaskWrapper


class ScaleCluster(LoggingTaskWrapper):

    @unique
    class ScalingAction(Enum):
        NONE = 0
        UP = 1
        DOWN = 2

    instances_count = luigi.Parameter(default=1)
    scaling_action = luigi.Parameter(default=ScalingAction.NONE)

    @property
    def priority(self):
        if self.scaling_action == self.ScalingAction.UP:
            return 100
        if self.scaling_action == self.ScalingAction.DOWN:
            return 0

    def run(self):
        pass