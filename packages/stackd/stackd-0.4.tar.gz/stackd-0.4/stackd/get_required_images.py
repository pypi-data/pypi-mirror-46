import yaml
from .merge_docker_yaml_files import merge_docker_yaml_files

def get_required_images(files_compose=[],force=False):
  images = set([])
  config = merge_docker_yaml_files(files_compose)
  if(config['services']):
    for service_name,service_def in config['services'].items():
      # image = service_def['image']
      if 'image' in service_def:
        images.add(service_def['image'])
  return images
