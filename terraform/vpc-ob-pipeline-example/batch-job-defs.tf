
locals {
  vcpusForCPUAggressiveTasks = 8
  vcpusForCPUNormalTasks     = 4
  vcpusForCPULowTasks        = 2
}

resource "aws_batch_job_definition" "sra" {
  name = "sra"
  type = "container"
  container_properties = <<EOF
{
  "image": "outlierbio/sra",
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
  "image": "outlierbio/star",
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
  "image": "outlierbio/skewer",
  "vcpus": ${local.vcpusForCPUAggressiveTasks},
  "memory": 8000,
  "command": [ "-z", "-t", "20", "-o", "Ref::outdir", "Ref::fq1", "Ref::fq2" ],
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
  "image": "outlierbio/picard",
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
  "image": "outlierbio/multiqc",
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
  "image": "outlierbio/kallisto",
  "vcpus": ${local.vcpusForCPUAggressiveTasks},
  "memory": 50000,
  "command": [ "quant", "-i", "Ref::index", "-o", "Ref::output", "-t", "20", "-b", "100", "Ref::reads1", "Ref::reads2" ],
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
  "image": "outlierbio/fastqc",
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
  "image": "outlierbio/disambiguate",
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
