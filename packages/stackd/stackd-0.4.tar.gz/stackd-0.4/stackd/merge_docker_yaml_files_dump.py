from .merge_docker_yaml_files import merge_docker_yaml_files
import yaml

def merge_docker_yaml_files_dump(files):
  config = merge_docker_yaml_files(files)
  return yaml.dump(config, default_flow_style=False, indent=2)