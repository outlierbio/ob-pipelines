import os
import sys
from os import path, system

import yaml

vars_map = {'COMPUTE_ENV': 'batch_compute_env_name'
            , 'QUEUE_NAME': 'batch_queue_name'
            , 'SOURCE_BUCKET': 'source_bucket_name'
            , 'TARGET_BUCKET': 'target_bucket_name'
            , 'KEY_NAME': 'ssh_key_name'
            , 'AUTOSCALING_GROUP': 'batch_resources_name'
            }


def load_config():
    cfg_file = path.join(path.dirname(__file__), 'config.yaml')
    if path.exists(cfg_file):
        with open(cfg_file) as f:
            cfg = yaml.load(f)
        return cfg
    else:
        raise Exception("Config file wasn't found")


def get_target_path(args):
    file_name = 'variables.auto.tfvars'
    target_path = path.join(path.abspath(path.dirname(__file__)), 'terraform/vpc-ob-pipeline/', file_name)
    if len(args) == 1:
        return target_path, 0
    if len(args) >= 2:
        p = args[1]
        if os.path.isdir(p):
            return path.join(p, file_name), 0
        else:
            return "", 1


def create_tfvars_file(target_path, cfg):
    result_list = []
    d = cfg['default']
#     for k in vars_map.keys():
#         result_list.append(
# """variable \"%s\" {
#     default = \"%s\"
# }""" % (vars_map[k], d[k]))
    for k in vars_map.keys():
        result_list.append("%s = \"%s\"\n" % (vars_map[k], d[k]))
    result = "\n\n".join(result_list)
    f = open(target_path, "w")
    f.write(result)
    f.close()
    print("File '%s' was created or updated." % target_path)


def main(args):
    if not os.path.isfile("./config.yaml"):
        print("File `config.yaml` doesn't exist, please create it from a template")
        system.exit(1)

    target_path, code = get_target_path(args)
    if code > 0:
        print("Directory doesn't exist")
        system.exit(code)
    else:
        try:
            create_tfvars_file(target_path, load_config())
        except Exception as e:
            print("Couldn't create tfvars file due to the following error: %s" % e)
            system.exit(1)


if __name__ == "__main__":
    main(sys.argv)
