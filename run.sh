#nohup python  manage.py runserver 0.0.0.0:8600 > 1.log &
# port is any port;
# python  manage.py runserver 0.0.0.0:8600
killall -9 uwsgi
/usr/bin/uwsgi --ini /home/otto/src/github/normaljs/conf/uwsgi.conf 
