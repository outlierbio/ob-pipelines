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

### Metadata

We are using [Airtable](https://airtable.com/) as main metadata storage.
Please create your own database based on our [sample](https://airtable.com/tblyy5D1XdeMG7hok/viwOOno27qvaYhpDt)

For *Experiments* required columns are:
* `Name` - text name of experiment. Should be unique. Could be auto generated based on formula, like in sample  
* `Samples` - link to *Samples* table 

For *Samples* required columns are:
* `Name` - text name of sample. Should be unique. Could be auto generated based on formula, like in sample
* `FastQ 1` - FastQ file URI
* `FastQ 2` - FastQ file URI  
* `Experiment` - link to *Experiments* table 

You can add any metadata fields you'd like.

Please note that pipeline will be looking for raw data in `<Experiment Name>/<Sample Name>`/ folder, eg `EXPT-1/SAMPLE-1/`


### Setup

Create `config.yaml` based on [config template](config-template.yaml)

* Install pre required dependencies using `make dev_install`
* Run [build.sh](scripts/build.sh) when you want to build new docker images and update docker registry
* Run [config.py](ob_pipelines/config.py) to configure AWS CLI
* Run [cluster.py](ob_pipelines/cluster.py) to spin up 1 EC2 instance in ECS
* Run [register_job_defs.py](scripts/register_job_defs.py) to register AWS Batch job definitions

You can now run sample pipelines, eg [rnaseq.py](ob_pipelines/pipelines/rnaseq/rnaseq.py) or [xenograft.py](ob_pipelines/pipelines/xenograft/xenograft.py), or create your own. Please refer to [Creating own pipelines](#creating-own-pipelines)  
To start pipeline run
`luigi --module <namespace> <entrypoint> --expt-id="<experiment ID>"`
eg
 `luigi --module ob_pipelines.pipelines.rnaseq.rnaseq RnaSeq --expt-id="EXPT-1"`

!Please Note! Installation via `configure_bas.sh` is deprecated, please use `ob_pipelines/cluster.py` instead

### Creating own pipelines

When creating your own pipelines please follow:

* Create folder for your pipeline under `ob_pipelines/pipelines/` and put pipeline entry point file there
* Reuse common tasks from `ob_pipelines/tasks/` when possible
* When creating custom pipeline specific tasks put them under `ob_pipelines/pipelines/<your pipeline>/tasks/`

Your folder structure should look like following:
```
.
├── ...
├── ob_pipelines
│   ├── ...
│   ├── pipelines
│   │   ├── ...
│   │   ├── <your pipeline>                 # your pipeline folder
│   │   │   ├── ...
│   │   │   ├── tasks                       # your custom tasks folder
│   │   │   │   └── *.py                    # your custom tasks
│   │   │   └── <your pipeline>.py          # your custom pipeline entrypoint
│   │   └── ...
│   ├── tasks
│   │   └── *.py
│   └── ...
└── ...
```

### Tasks

* `BatchTask` - basic task for the pipeline, a wrapper for Luigi's Task class

#### Download tasks
* `SRADownload` - downloads data from NCBI
* `GDCDownload` - downloads BAM and FASTQ files from https://gdc.cancer.gov. A client supports validation of downloaded data with using MD5 from files' annotation from the site. Annotations are optional and the toold doesn't guarantee that all files will be verified

#### Testing 
If you have issues running test please try following `python3 -m pytest -sv test/local/`

### Contributing

If you would like to contribute please check our [Contribution guide](CONTRIBUTING.md)