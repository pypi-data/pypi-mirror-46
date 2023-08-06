from .docker_compose_config import docker_compose_config

def api_compo_freeze2(files_compose):
  process = docker_compose_config(files_compose)
  print(process.stdout)
  if(process.returncode != 0):
      sys.exit(process.returncode)