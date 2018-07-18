import pytest
from mongoengine.connection import register_connection, get_connection
from mongoengine.context_managers import switch_db

from ob_pipelines import Task
from ob_pipelines.entities import Experiment, Job


@pytest.yield_fixture(scope="function", autouse=True)
def another_resource_setup_with_autouse():
    register_connection('testdb', host='mongomock://localhost/test')
    with switch_db(Experiment, "testdb"), switch_db(Job, "testdb"), switch_db(Task, "testdb"):
        yield
        conn = get_connection("testdb")
        # should use database_names because mongomock does not support new method
        for db_name in conn.database_names():
            conn.drop_database(db_name)
