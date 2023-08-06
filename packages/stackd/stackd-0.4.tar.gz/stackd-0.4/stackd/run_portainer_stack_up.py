import os
from .build_stack_compose_file import build_stack_compose_file
from .build_stack_env_file import build_stack_env_file
from .paths import get_build_stack_compose_file_path, get_build_stack_env_file_path
from .run_shell import run_shell

def run_portainer_stack_up(files_compose, env_vars, args):
  env = os.environ.copy()

  build_stack_compose_file(files_compose, env_vars)
  build_stack_env_file(env_vars)

  env['PORTAINER_STACK_NAME'] = env_vars['STACKD_STACK_NAME']
  env['DOCKER_COMPOSE_FILE'] = get_build_stack_compose_file_path(env_vars)
  env['ENVIRONMENT_VARIABLES_FILE'] = get_build_stack_env_file_path(env_vars)
  env['HTTPIE_VERIFY_SSL'] = 'no'
  env['VERBOSE_MODE'] = 'true'
  env['PORTAINER_USER'] = 'admin'
  env['PORTAINER_PASSWORD'] = 'admin'
  env['PORTAINER_URL'] = 'http://localhost'
  # process = run_shell(['portainer-stack-up', args], env=env)
  process = run_shell(['/home/jo/Devlab/gitlab.com/youtopia.earth/bin/stackd/portainer-stack-up', args], env=env)
  return process
