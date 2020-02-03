
docker-compose down

set backup_dir="%cd%\backup"

docker volume rm wordpress_db_data
docker run --rm -v wordpress_db_data:/wordpress_db_data -v %backup_dir%:/wordpress_backup ubuntu bash -c "mkdir /untar && tar xzf /wordpress_backup/db.tar.gz -C /untar && mv /untar/db_data/* /wordpress_db_data"

docker volume rm wordpress_wordpress_data
docker run --rm -v wordpress_wordpress_data:/wordpress_wordpress_data -v %backup_dir%:/wordpress_backup ubuntu bash -c "mkdir /untar && tar xzf /wordpress_backup/wordpress.tar.gz -C /untar && mv /untar/wordpress_data/* /wordpress_wordpress_data"

docker-compose up -d
