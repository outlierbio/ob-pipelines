import luigi
from luigi.worker import Worker

from ob_pipelines.batch import JobTask
from ob_pipelines.entities import Experiment, Job, Task


class SuccessTask(JobTask):
    def run(self):
        pass


class FailureTask(JobTask):
    def run(self):
        raise Exception('This is test exception')


class SimpleTask(luigi.Task):
    def run(self):
        pass


class TestTasks:
    def test_task_success(self):
        exp = Experiment(user_id="test")
        exp.save()
        job = Job(experiment=exp, params={"param1": 1})
        job.save()
        with Worker() as worker:
            worker.add(SuccessTask(job_id=str(job.id)))
            worker.run()
        assert Task.objects.count() == 1
        assert Task.objects.get().exception is None

    def test_task_failure(self):
        exp = Experiment(user_id="test")
        exp.save()
        job = Job(experiment=exp, params={"param1": 1})
        job.save()
        with Worker() as worker:
            worker.add(FailureTask(job_id=str(job.id)))
            worker.run()
        assert Task.objects.count() == 1
        assert Task.objects.get().exception is not None

    def test_task_simple(self):
        with Worker() as worker:
            worker.add(SimpleTask())
            worker.run()
        assert Task.objects.count() == 0