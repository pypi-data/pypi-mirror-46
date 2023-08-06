def api_help():
  print('''
Usage: stackd [OPTIONS] COMMAND

STACKD - A docker swarm deploy helper according to environment 🦊
see https://gitlab.com/youtopia.earth/bin/stackd/

Commands:
  deploy                        docker stack deploy (alias: up)
  rm                            docker stack rm (alias: remove)
  getname
  shellenv                      to load env vars in current bash: eval $(stackd shellenv)
  ls                            docker stack ls
  ps                            docker stack ps
  infos                         display env files, compose files and vars
  compo                         display yaml compose result (stackd merging)
  compo-freeze                  display yaml compose result (stackd merging substituting env vars)
  compo-freeze2                 display yaml compose result (using docker-compose config)
  getimagelist                  list all images required by services
  pull                          pull images required by services
  deploy-with-portainer         docker stack deploy using portainer api
  rm-with-portainer             docker stack rm using portainer api
  config-prune                  remove specified config unused versions
  help                          show this page (alias: h)

  ''')