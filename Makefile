.PHONY: scheduler_start scheduler_stop scheduler_nodetach dev_install test
SHELL = /bin/bash

test:
	pytest -v test/local/

dev_install: ../ob-airtable  # install project as library into current python and dependency if needed
	pip install -e .[test]
	pip install awscli

scheduler_start: scheduler_stop  # start scheduler in background
	mkdir -p var/logs
	luigid --background --pidfile var/luigid.pid --logdir var/logs/ --state-path var/luigid.state

scheduler_stop:  # stop scheduler
	- killall luigid

scheduler_nodetach:  # run scheduler in foreground
	luigid --state-path var/luigid.state

../ob-airtable:  # Dependency which is not listened in setup.py
	git clone git@github.com:outlierbio/ob-airtable.git ../ob-airtable
	pip install -e ../ob-airtable
