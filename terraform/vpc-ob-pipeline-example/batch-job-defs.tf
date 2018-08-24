
locals {
  vcpusForCPUAggressiveTasks = 8
  vcpusForCPUNormalTasks     = 4
  vcpusForCPULowTasks        = 2
  docker_registry_prefix = "${var.aws_account_id}.dkr.ecr.us-east-1.amazonaws.com/outlier-bio/" # outlierbio
}

resource "aws_batch_job_definition" "sra" {
  name = "sra"
  type = "container"
  container_properties = <<EOF
{
  "image": "${local.docker_registry_prefix}sra",
  "vcpus": ${local.vcpusForCPUAggressiveTasks},
  "memory": 50000,
  "command": [ "Ref::srr_id", "Ref::layout", "Ref::outpath" ],
  "volumes": [{
    "host": { "sourcePath": "/mnt/scratch" },
    "name": "scratch"
  }],
  "mountPoints": [{
    "containerPath": "/scratch",
    "readOnly": false,
    "sourceVolume": "scratch"
  }]
}
EOF
}

resource "aws_batch_job_definition" "star" {
  name = "star"
  type = "container"
  container_properties = <<EOF
{
  "image": "${local.docker_registry_prefix}star",
  "vcpus": ${local.vcpusForCPUAggressiveTasks},
  "memory": 50000,
  "command": [ "Ref::fq1", "Ref::fq2", "Ref::genome_dir", "Ref::prefix", "Ref::threads" ],
  "volumes": [{
    "host": { "sourcePath": "/mnt/scratch" },
    "name": "scratch"
  }, {
    "host": { "sourcePath": "/mnt/reference" },
    "name": "reference"
  }],
  "environment": [{
    "name": "SCRATCH_DIR",   
    "value": "/scratch"
  }, {
    "name": "REFERENCE_DIR", 
    "value": "/reference"
  }],
  "mountPoints": [{
    "containerPath": "/scratch",
    "readOnly": false,
    "sourceVolume": "scratch"
  }, {
    "containerPath": "/reference",
    "readOnly": true,
    "sourceVolume": "reference"
  }]
}
EOF
}

resource "aws_batch_job_definition" "skewer" {
  name = "skewer"
  type = "container"
  container_properties = <<EOF
{
  "image": "${local.docker_registry_prefix}skewer",
  "vcpus": ${local.vcpusForCPUAggressiveTasks},
  "memory": 8000,
  "command": [ "-z", "-t", "${local.vcpusForCPUAggressiveTasks}", "-o", "Ref::outdir", "Ref::fq1", "Ref::fq2" ],
  "environment": [{
    "name": "SCRATCH_DIR", "value": "/scratch"
  }],  
  "mountPoints": [{
    "containerPath": "/scratch", 
    "readOnly": false,
    "sourceVolume": "scratch"
  }],
  "volumes": [{
    "name": "scratch",
    "host": { "sourcePath": "/mnt/scratch" }
  }]
}
EOF
}

resource "aws_batch_job_definition" "bam2fastq" {
  name = "bam2fastq"
  type = "container"
  container_properties = <<EOF
{
  "image": "${local.docker_registry_prefix}picard",
  "vcpus": ${local.vcpusForCPUNormalTasks},
  "memory": 8000,
  "command": [ "sh", "/bam2fastq.sh", "Ref::input", "Ref::fq1", "Ref::fq2" ],
  "volumes": [{
    "host": { "sourcePath": "/mnt/scratch" },
    "name": "scratch"
  }],
  "environment": [{
    "name": "SCRATCH_DIR", "value": "/scratch"
  }],
  "mountPoints": [{
    "containerPath": "/scratch",
    "readOnly": false,
    "sourceVolume": "scratch"
  }]
}
EOF
}

resource "aws_batch_job_definition" "multiqc" {
  name = "multiqc"
  type = "container"
  container_properties = <<EOF
{
  "image": "${local.docker_registry_prefix}multiqc",
  "vcpus": ${local.vcpusForCPULowTasks},
  "memory": 8000,
  "command": [ "Ref::analysis_dir" ],
  "environment": [{
    "name": "SCRATCH_DIR",
    "value": "/scratch"
  }],
  "volumes": [{
    "host": { "sourcePath": "/mnt/scratch" },
    "name": "scratch"
  }],
  "mountPoints": [{
    "containerPath": "/scratch",
    "readOnly": false,
    "sourceVolume": "scratch"
  }]
}
EOF
}

resource "aws_batch_job_definition" "kallisto" {
  name = "kallisto"
  type = "container"
  container_properties = <<EOF
{
  "image": "${local.docker_registry_prefix}kallisto",
  "vcpus": ${local.vcpusForCPUAggressiveTasks},
  "memory": 50000,
  "command": [ "quant", "-i", "Ref::index", "-o", "Ref::output", "-t", "${local.vcpusForCPUAggressiveTasks}", "-b", "100", "Ref::reads1", "Ref::reads2" ],
  "volumes": [{
    "host": { "sourcePath": "/mnt/scratch" },
    "name": "scratch"
  }, {
    "host": { "sourcePath": "/mnt/reference" },
    "name": "reference"
  }],
  "environment": [{
    "name": "SCRATCH_DIR",
    "value": "/scratch"
  },{
    "name": "REFERENCE_DIR",
    "value": "/reference"
  }],
  "mountPoints": [{
    "containerPath": "/scratch",
    "readOnly": false,
    "sourceVolume": "scratch"
  }, {
    "containerPath": "/reference",
    "readOnly": true,
    "sourceVolume": "reference"
  }]
}
EOF
}

resource "aws_batch_job_definition" "fastqc" {
  name = "fastqc"
  type = "container"
  container_properties = <<EOF
{
  "image": "${local.docker_registry_prefix}fastqc",
  "vcpus": ${local.vcpusForCPULowTasks},
  "memory": 8000,
  "command": [ "Ref::fq1", "Ref::fq2", "Ref::out_dir", "Ref::name" ],
  "environment": [{
    "name": "SCRATCH_DIR",
    "value": "/scratch"
  }],
  "volumes": [{
    "host": { "sourcePath": "/mnt/scratch" },
    "name": "scratch"
  }],
  "mountPoints": [{
    "containerPath": "/scratch",
    "readOnly": false,
    "sourceVolume": "scratch"
  }]
}
EOF
}

resource "aws_batch_job_definition" "disambiguate" {
  name = "disambiguate"
  type = "container"
  container_properties = <<EOF
{
  "image": "${local.docker_registry_prefix}disambiguate",
  "vcpus": ${local.vcpusForCPUAggressiveTasks},
  "memory": 16000,
  "command": [ "-s", "Ref::sample", "-o", "Ref::outdir", "-a", "Ref::aligner", "Ref::A", "Ref::B" ],
  "volumes": [{
    "host": { "sourcePath": "/mnt/scratch" },
    "name": "scratch"
  }],
  "environment": [{
    "name": "SCRATCH_DIR",
    "value": "/scratch"
  }],
  "mountPoints": [{
    "containerPath": "/scratch",
    "readOnly": false,
    "sourceVolume": "scratch"
  }]
}
EOF
}

resource "aws_batch_job_definition" "samtools-sort-by-coord" {
  name = "samtools-sort-by-coord"
  type = "container"
  container_properties = <<EOF
{
  "image": "outlierbio/samtools",
  "vcpus": ${local.vcpusForCPUAggressiveTasks},
  "memory": 50000,
  "command": [ "samtools", "sort", "-m", "8G", "-o", "Ref::output", "-T", "Ref::tmp_prefix", "-@", "4", "Ref::input" ],
  "environment": [{
    "name": "SCRATCH_DIR",
    "value": "/scratch"
  }],
  "mountPoints": [{
    "containerPath": "/scratch",
    "readOnly": false,
    "sourceVolume": "scratch"
  }],
  "volumes": [{
    "name": "scratch",
    "host": { "sourcePath": "/mnt/scratch" }
  }]
}
EOF
}