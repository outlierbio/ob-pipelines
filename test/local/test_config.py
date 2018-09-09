from ob_pipelines.config import cfg


class TestConfigIntegrity:
    def check_airtable_cfg(self):
        assert cfg['AIRTABLE_API_ENDPOINT'] is not None
        assert cfg['AIRTABLE_API_KEY'] is not None
        assert cfg['AIRTABLE_EXPT_TABLE'] is not None
        assert cfg['AIRTABLE_SAMPLE_TABLE'] is not None
        assert cfg['AIRTABLE_TASK_TABLE'] is not None

    def check_s3_cfg(self):
        assert cfg['SOURCE_BUCKET'] is not None
        assert cfg['TARGET_BUCKET'] is not None
