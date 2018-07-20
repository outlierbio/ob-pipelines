# ob-pipelines

Luigi pipelines and Dockerized apps for bioinformatics and data science

Use with Python 3.* only.

This repository requires [Airtable library](https://github.com/outlierbio/ob-airtable/) to be copied into python libraries.
You can install it and other dependencies by running ```make dev_install```

### Makefile

Provides commands to start/stop scheduler, install project, etc.
* `test` _run tests_
* `dev_install` _install project and dependencies_
* `scheduler_start` _start scheduler in background_
* `scheduler_stop` _stop scheduler_
* `scheduler_nodetach` _run scheduler in foreground_

For more details please check each command in Makefile.

### Contributing

If you would like to contribute please check our [Contribution guide](CONTRIBUTING.md)
