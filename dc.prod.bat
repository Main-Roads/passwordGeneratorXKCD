@REM docker-compose -f docker-compose.prod.yml down --remove-orphans && docker-compose -f docker-compose.prod.yml rm -f && docker image prune -f && docker-compose -f docker-compose.prod.yml build  --force-rm --compress --no-cache && docker-compose -f docker-compose.prod.yml up -d

@REM docker builder prune -f -a
docker-compose -f docker-compose.prod.yml down --rmi all --volumes
docker-compose -f docker-compose.prod.yml build --no-cache --compress
docker-compose -f docker-compose.prod.yml up -d --force-recreate


@REM curl http://localhost:8080/

docker exec -it password-generator find /home/app/web/project/ -type f
docker exec -it password-generator-web find /home/app/web/project/ -type f