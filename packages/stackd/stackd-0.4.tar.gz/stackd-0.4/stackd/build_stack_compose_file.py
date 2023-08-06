from .merge_docker_yaml_files_dump import merge_docker_yaml_files_dump
from .paths import ensure_build_dir_exists, get_build_stack_compose_file_path

def build_stack_compose_file(files_compose, env_vars):
  yaml_dump = merge_docker_yaml_files_dump(files_compose)
  BUILD_STACK_COMPOSE_FILE = get_build_stack_compose_file_path(env_vars)
  ensure_build_dir_exists()
  f = open(BUILD_STACK_COMPOSE_FILE, 'w+')
  f.write(yaml_dump)
  f.close()