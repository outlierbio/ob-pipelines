from datetime import datetime

from ob_pipelines.entities import Task, Job, Experiment


class TestEntities:
    def test_it(self):
        exp = Experiment(user_id="test")
        exp.save()
        job = Job(experiment=exp, params={"param1": 1})
        job.save()
        task = Task(job=job, name='test_task', started_at=datetime.now())
        task.save()

        assert Task.objects.count() == 1
        assert Job.objects.count() == 1
        assert Experiment.objects.count() == 1
        assert task.job.experiment.id == exp.id

        completed = datetime.now().replace(microsecond=0)
        task.completed_at = completed
        task.save()
        assert Task.objects.get(id=task.id).completed_at == completed

    def test_empty_db(self):
        assert Task.objects.count() == 0
        assert Job.objects.count() == 0
        assert Experiment.objects.count() == 0