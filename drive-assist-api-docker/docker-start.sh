while getopts ":hdpt" opt; do
  case ${opt} in
    h )
      printf "USAGE: ./docker_start.sh [OPTION]... \n\n"
      printf "-h for HELP, -d for DEV, -p for dev, or -t for TEARDOWN \n\n"
      exit 1
      ;;
    d )
      # Rebuild image itcard_flask
      docker-compose-dev build --no-cache

      # Create hquinn-net bridge network for container(s) to communicate
      docker network create --driver bridge hquinn-net

      # Spin up hquinn-app container
      docker run -d --name itcard_flask --restart always -p 5432:5432
      # -v itcard_flask_home:/var/www/html --network hquinn-net itcard_flask:latest

      exit 1
      ;;
    p )
      # Rebuild image
      docker-compose-dev build

      # Spin up container
      docker-compose-dev up -d

      exit 1
      ;;
    t )
      # If itcard_flask container is running, turn it off.
      running_app_container=`docker ps | grep itcard_flask | wc -l`
      if [ $running_app_container -gt "0" ]
      then
        docker kill itcard_flask
      fi

      # If turned off itcard_flask container exists, remove it.
      existing_app_container=`docker ps -a | grep hquinn-app | grep Exit | wc -l`
      if [ $existing_app_container -gt "0" ]
      then
        docker rm hquinn-app
      fi

      # If image for itcard_flask exists, remove it.
      existing_app_image=`docker images | grep itcard_flask | wc -l`
      if [ $existing_app_image -gt "0" ]
      then
        docker rmi itcard_flask
      fi

    #   # If itcard_flask_home volume exists, remove it.
    #   existing_app_volume=`docker volume ls | grep itcard_flask_home | wc -l`
    #   if [ $existing_app_volume -gt "0" ]
    #   then
    #     docker volume rm itcard_flask_home
    #   fi

    #   # If itcard_flask_net network exists, remove it.
    #   existing_itcardnet_network=`docker network ls | grep itcard_flask_net | wc -l`
    #   if [ $existing_itcardnet_network -gt "0" ]
    #   then
    #     docker network rm itcard_flask_net
    #   fi

      exit 1
      ;;
    \? )
      printf "Invalid option: %s" "$OPTARG" 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

printf "USAGE: ./docker_start.sh [OPTION]... \n\n"
printf "-h for HELP, -d for DEV, -p for dev, or -t for TEARDOWN \n\n"
exit 1
;;