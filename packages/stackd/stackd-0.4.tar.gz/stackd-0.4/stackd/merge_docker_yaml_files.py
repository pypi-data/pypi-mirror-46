from deepmerge import always_merger
from .parse_yaml import parse_yaml

def merge_docker_yaml_files(files):
  config = {}
  for file in files:
    config = always_merger.merge(config, parse_yaml(file))
  return config