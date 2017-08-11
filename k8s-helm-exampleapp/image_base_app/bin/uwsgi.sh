#! /bin/bash -e
echo "=======Run $0 for exampleapp `pwd`========"

echo "--- Start uwsgi service exampleapp ---"
su -l httpd -c '/usr/sbin/uwsgi --ini /home/httpd/conf/uwsgi/uwsgi.conf  --logto /home/httpd/logs/httpd_uwsgi_access_service.log'
