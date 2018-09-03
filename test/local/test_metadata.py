from ob_pipelines.entities.persistence import get_sample_by_key, get_experiments, get_samples, get_tasks, \
    get_experiment_by_name


class TestMetadataIntegrity:
    def test_experiment(self):
        experiment = get_experiment_by_name('EXPT-1')
        assert experiment is not None
        assert experiment.name == 'EXPT-1'

        for sample_id in experiment.Samples:
            sample = get_sample_by_key(sample_id)
            assert sample.sample['Name'] is not None
            assert sample.sample['FastQ 1'] is not None
            assert sample.sample['FastQ 2'] is not None

    def test_experiments(self):
        experiments = get_experiments()
        assert experiments is not None
        for experiment in experiments:
            assert experiment.name is not None

    def test_samples(self):
        samples = get_samples()
        assert samples is not None
        for sample in samples:
            assert sample.sample['Name'] is not None
            assert sample.sample['FastQ 1'] is not None
            assert sample.sample['FastQ 2'] is not None

    def test_tasks(self):
        tasks = get_tasks()
        assert tasks is not None
