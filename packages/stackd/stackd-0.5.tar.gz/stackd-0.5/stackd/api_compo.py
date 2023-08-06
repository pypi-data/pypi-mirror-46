from .merge_docker_yaml_files_dump import merge_docker_yaml_files_dump

def api_compo(files_compose):
  yaml_dump = merge_docker_yaml_files_dump(files_compose)
  print(yaml_dump)
