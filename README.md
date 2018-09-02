# ob-pipelines

Luigi pipelines and Dockerized apps for bioinformatics and data science

Use with Python 3.* only.

The pipelines are based on [Luigi](https://github.com/spotify/luigi) framework from Spotify which helps to build complex pipelines of batch jobs and simplifies dependency resolution and workflow management.
Dockerized applications for the pipelines can use files from AWS S3 and from local file system. You can find more containers in [BioContainer](https://github.com/BioContainers/containers) repository.

This repository requires [Airtable library](https://github.com/outlierbio/ob-airtable/) to be copied into python libraries.
You can install it and other dependencies by running ```make dev_install```

###Abstract

ob-pipelines project already contains several pipelines which are ready to use:
 * ChipSeq
 * RnaSeq
 * SRADownload
 * Xenograft
 
###Project overview

#### Makefile

Provides commands to start/stop scheduler, install project, etc.
* `test` _run tests_
* `dev_install` _install project and dependencies_
* `scheduler_start` _start scheduler in background_
* `scheduler_stop` _stop scheduler_
* `scheduler_nodetach` _run scheduler in foreground_

For more details please check each command in Makefile.

#### Metadata

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


#### Setup

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

#### Creating own pipelines

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

#### Tasks
* `LoggingTaskWrapper` - basic task for the pipeline, it is used for managing of priorities and logging activities
* `BatchTask` - basic task for the pipeline, a wrapper for Luigi's Task class and it is used to start task in AWS Batch

##### Download tasks
* `SRADownload` - downloads SRA files from NCBI (https://www.ncbi.nlm.nih.gov/)
* `GDCDownload` - downloads BAM and FASTQ files from https://gdc.cancer.gov. A client supports validation of downloaded data with using MD5 from annotations for files from the site. Annotations are optional and the tool does not guarantee that all files will be verified
* `S3Sync` - synchronizes a storage with AWS S3, it can download from S3 and upload to S3.

##### Scaling tasks

* `ScaleCluster` - allows to do up scale and down scale of AWS cluster via "desired count" parameter in AutoScaling group.  Scaling tasks work only when configuration parameter `AUTOSCALING_GROUP` was specified in `config.yaml`. You don't need to specify the full name of the group, the tasks find a group with name which starts with the same string. Scaling up task has the highest priority (100), Scaling down task has the lowest priority (0). All LoggingTaskWrapper has priority 50 by default. Luigi uses acyclic direction graph structure for tasks and priorities of its work only for tasks on the same level (the same distance from a root task).

### Testing 
If you have issues running test please try following `python3 -m pytest -sv test/local/`

###Getting started

1. `make dev_install`
2. Configure AWS CLI - `aws configure`
3. Create a base in Airtable with Experiment, Samples, Tasks. More information is in **Metadata** paragraph
4. Create `config.yaml`, template of it is `config-template.yaml` and specify all needed configuration parameters.
     Mandatory parameters:
     * All `AIRTABLE_*` parameters
     * `RAW_BUCKET` - a bucket with source data
     * `S3_BUCKET` - a bucket with intermediate and resulted data
     * `COMPUTE_ENV`
     * `QUEUE_NAME`
     * `IMAGE_ID`
     * `INSANCE_TYPE`
     * `SPOT_PRICE`
     * `TARGET_CAPACITY`
     * `AUTOSCALING_GROUP`
5. Install [Terraform](https://www.terraform.io/downloads.html)
6. Update TF variables in  `./terraform/vpc-ob-pipeline-example/variables.tf` file
7. Execute:
    ```
   terraform plan
   terraform apply 
    ```
8. Copy source files to `RAW_BUCKET` on S3, for examples: `s3://bucket/raw/SRR821356_1.fastq.gz and add a link to it in FastQ cell in airtable.
9. Run luigi Task for a pipeline, for example:  `python3 -m luigi --module ob_pipelines.pipelines.rnaseq.rnaseq RnaSeq --local-scheduler --expt-id EXPT-1`
    

### Contributing

If you would like to contribute please check our [Contribution guide](CONTRIBUTING.md)