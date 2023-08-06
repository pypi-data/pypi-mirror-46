import subprocess
from .flatten import flatten
from .style import style

def docker_compose_config(files):
  process = subprocess.run(
    flatten([
      'docker-compose',
      list(map(lambda f: ['-f', f], files)),
      'config'
    ]),
    universal_newlines=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
  )
  stderr = ''
  for line in process.stderr.split('\n') :
     if 'Compose does not support' not in line:
       stderr += line + '\n'
  stderr = stderr.strip()
  if(stderr != ''):
    if(process.returncode != 0):
      error_label = style.RED('ERROR')
    else:
      error_label = style.YELLOW('WARNING')
    sys.stderr.write(error_label+': '+stderr+'\n\n')
    sys.stderr.flush()
  return process