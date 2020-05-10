
docker-compose down

set backup_dir="%cd%\backup"

powershell docker run --rm -v wordpress_db_data:/db_data -v %backup_dir%:/backup --rm ubuntu tar czf /backup/db.tar.gz /db_data

powershell docker run --rm -v wordpress_wordpress_data:/wordpress_data -v %backup_dir%:/backup --rm ubuntu tar czf /backup/wordpress.tar.gz /wordpress_data

docker-compose up -d
