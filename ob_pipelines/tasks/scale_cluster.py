import logging
from enum import Enum, unique

import boto3
import luigi

from ob_pipelines.config import cfg
from ob_pipelines import LoggingTaskWrapper

logger = logging.getLogger('ob-pipelines')


@unique
class ScalingAction(Enum):
    NONE = 0
    UP = 1
    DOWN = 2


class ScaleCluster(LoggingTaskWrapper):
    desired_capacity_target = luigi.Parameter(default=1)
    scaling_action = luigi.Parameter(default=ScalingAction.NONE)
    task_priority = luigi.Parameter(default=0)

    done = False

    @property
    def priority(self):
        if self.scaling_action == ScalingAction.UP:
            return 100
        if self.scaling_action == ScalingAction.DOWN:
            return 0
        return self.task_priority

    def run(self):
        if self.done:
            return

        ag_name = cfg['AUTOSCALING_GROUP']
        client = boto3.client('autoscaling')
        response = client.describe_auto_scaling_groups()
        groups = response['AutoScalingGroups']
        target_groups = list(filter(lambda g: g['AutoScalingGroupName'].startswith(ag_name), groups))
        if len(target_groups) > 1:
            raise Exception("AWS contains %d groups with name '%s', please specify other name." % (len(target_groups),
                                                                                                   ag_name))
        group = target_groups[0]
        desired_capacity = group["DesiredCapacity"]
        if desired_capacity != self.desired_capacity_target:
            logger.info("Applying desired capacity: group - %s, desired capacity - %d, action - %s" % (
                group['AutoScalingGroupName'], self.desired_capacity_target, self.scaling_action
            ))
            response = client.update_auto_scaling_group(
                AutoScalingGroupName=group['AutoScalingGroupName'],
                DesiredCapacity=self.desired_capacity_target
            )
        else:
            logger.info("Don't need to scale up or down: group - %s, desired capacity - %d, action - %s" % (
                group['AutoScalingGroupName'], self.desired_capacity_target, self.scaling_action
            ))

        self.done = True

    def complete(self):
        return self.done
