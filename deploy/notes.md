## hist

## Processes running

```bash
$ ps aux | grep -E 'python|beam|mq|celery|supervisor|service'
root       824  0.0  0.4 171220 16980 ?        Ssl  Apr29   0:00 /usr/bin/python3 /usr/bin/networkd-dispatcher
root       851  0.0  0.1 288376  6868 ?        Ssl  Apr29   0:07 /usr/lib/accountsservice/accounts-daemon
root      5077  0.0  0.5  65448 21176 ?        Ss   Apr30   0:47 /usr/bin/python /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
root      5111  0.0  1.6 149484 66200 ?        S    Apr30   3:38 /srv/virtualenvs/openchat_venv/bin/python3 /webapps/virtualenvs/openchat_venv/bin/celery -A openchat worker -B -l info
root      5116  0.0  1.5 159088 62212 ?        S    Apr30   0:19 /srv/virtualenvs/openchat_venv/bin/python3 /webapps/virtualenvs/openchat_venv/bin/celery -A openchat worker -B -l info
root      5117  0.0  1.4 147808 58644 ?        S    Apr30   0:00 /srv/virtualenvs/openchat_venv/bin/python3 /webapps/virtualenvs/openchat_venv/bin/celery -A openchat worker -B -l info
root      5118  0.0  1.5 148728 61084 ?        S    Apr30   0:44 /srv/virtualenvs/openchat_venv/bin/python3 /webapps/virtualenvs/openchat_venv/bin/celery -A openchat worker -B -l info
ubuntu   21560  0.0  0.5  62260 22684 ?        S    Apr29   0:46 /srv/virtualenvs/openchat_venv/bin/python3 /srv/virtualenvs/openchat_venv/bin/gunicorn --reload --log-level=debug --name openchat --bind 127.0.0.1:8001 --workers 2 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application
ubuntu   21563  0.6  1.4 204084 57540 ?        Sl   Apr29  41:58 /srv/virtualenvs/openchat_venv/bin/python3 /srv/virtualenvs/openchat_venv/bin/gunicorn --reload --log-level=debug --name openchat --bind 127.0.0.1:8001 --workers 2 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application
ubuntu   21565  0.6  1.4 203828 57160 ?        Sl   Apr29  41:59 /srv/virtualenvs/openchat_venv/bin/python3 /srv/virtualenvs/openchat_venv/bin/gunicorn --reload --log-level=debug --name openchat --bind 127.0.0.1:8001 --workers 2 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application
ubuntu   28016  0.0  0.0  15292  2644 pts/0    S+   17:40   0:00 grep --color=auto -E python|beam|mq|celery|supervisor|service
rabbitmq 31395  0.0  0.0   4628   808 ?        Ss   Apr29   0:00 /bin/sh /usr/sbin/rabbitmq-server
rabbitmq 31412  0.0  0.0   4628  1916 ?        S    Apr29   0:00 /bin/sh /usr/lib/rabbitmq/bin/rabbitmq-server
rabbitmq 31578  0.0  0.0  26852   204 ?        S    Apr29   0:03 /usr/lib/erlang/erts-9.2/bin/epmd -daemon
rabbitmq 31683  0.2  1.5 2180324 61492 ?       Sl   Apr29  18:03 /usr/lib/erlang/erts-9.2/bin/beam.smp -W w -A 64 -P 1048576 -t 5000000 -stbt db -zdbbl 32000 -K true -B i -- -root /usr/lib/erlang -progname erl -- -home /var/lib/rabbitmq -- -pa /usr/lib/rabbitmq/lib/rabbitmq_server-3.6.10/ebin -noshell -noinput -s rabbit boot -sname rabbit@big-openchat -boot start_sasl -kernel inet_default_connect_options [{nodelay,true}] -sasl errlog_type error -sasl sasl_error_logger false -rabbit error_logger {file,"/var/log/rabbitmq/rabbit@big-openchat.log"} -rabbit sasl_error_logger {file,"/var/log/rabbitmq/rabbit@big-openchat-sasl.log"} -rabbit enabled_plugins_file "/etc/rabbitmq/enabled_plugins" -rabbit plugins_dir "/usr/lib/rabbitmq/plugins:/usr/lib/rabbitmq/lib/rabbitmq_server-3.6.10/plugins" -rabbit plugins_expand_dir "/var/lib/rabbitmq/mnesia/rabbit@big-openchat-plugins-expand" -os_mon start_cpu_sup false -os_mon start_disksup false -os_mon start_memsup false -mnesia dir "/var/lib/rabbitmq/mnesia/rabbit@big-openchat" -kernel inet_dist_listen_min 25672 -kernel inet_dist_listen_max 25672
rabbitmq 31797  0.0  0.0   4520  1652 ?        Ss   Apr29   0:07 erl_child_setup 65536
rabbitmq 31860  0.0  0.0   8264  1084 ?        Ss   Apr29   0:00 inet_gethost 4
rabbitmq 31861  0.0  0.0  14616  1848 ?        S    Apr29   0:01 inet_gethost 4
```

## hist

```
sudo apt remove postgresql-10
sudo apt remove postgresql-9.6
sudo apt-get install -y postgresql-9.6 postgresql-contrib python3-psycopg2 ntp wget git nano 
sudo nano /etc/apt/sources.list
sudo apt remove postgresql-10
sudo apt remove postgresql-9.6
sudo apt install postgresql-9.6
sudo nano /etc/apt/sources.list
sudo apt install postgresql-9.6
sudo apt update
sudo apt install postgresql-9*
sudo apt autoremove
sudo apt remove postgresql
sudo apt remove postgresql-contrib
sudo apt remove python3-psycopg2
sudo apt autoremove
sudo apt autoclean
sudo apt install postgresql
sudo apt install postgresql-contrib
pip install --upgrade psycopg2-binary --no-cache-dir
pip unininstall psycopg2-binary
pip uninstall psycopg2-binary
pip uninstall psycopg2
pip install --upgrade psycopg2 --no-cache-dir
nano openchat/local_settings.py 
python3 manage.py validate
python3 manage.py migrate
sudo -u postgres createdb --encoding='UTF-8' --lc-collate='en_US.UTF-8' --lc-ctype='en_US.UTF-8' --template='template0' $DBNAME "For openchat hackor and other totalgood.org projects"
sudo -u postgres echo "ALTER USER $DBUN WITH PASSWORD '$DBPW';" | sudo -u postgres psql $DBNAME
ls /etc/postgresql/
sudo apt remove python3-psycopg2
sudo apt remove python-psycopg2
sudo apt remove postgresql
sudo apt remove postgresql-contrib
ls /etc/postgresql/
sudo rm -rf /etc/postgresql/*
sudo shutdown -r now
cd /srv/openchat
git pull
ls /etc/postgresql
ls /etc/postgresql/
sudo apt install postgresql
ls /etc/postgresql
sudo apt install postgresql-contrib
ls /etc/postgresql
ls -al /etc/postgresql
sudo service postgresql restart
ls -al /etc/postgresql
psql
python manage.py migrate
GH_ORG='totalgood'
GH_PRJ='openchat'
DBNAME='hackor'
DBUN=postgres
DOMAIN_NAME='totalgood.org'
SUBDOMAIN_NAME="GH_PRJ"
BASHRC_PATH="$HOME/.bashrc"
PUBLIC_IP='34.211.189.63'  # from AWS EC2 Dashboard
SRV='/srv'
VIRTUALENVS="$SRV/virtualenvs"
export DOCKER_DEV=true  # DOCKER_DEV=false uses postgis instead of postgresql backend in settings.py
source "$VIRTUALENVS/${GH_PRJ}_venv/bin/activate"
pip install --upgrade -r requirements.txt 
python manage.py migrate
more settingspy
more settings.py
more openchat/settings.py
git pull
y
git pull
nano openchat/local_settings.py 
git status
git pull
nano openchat/local_settings.py 
python manage.py migrate
pip uninstall psycopg2
pip freeze | grep pg
pip freeze | grep post
pip freeze | grep -i post
pip freeze | grep -i pg
python manage.py migrate
grep -i post openchat/settings.py
grep -i post openchat/local_settings.py
nano openchat/local_settings.py 
git pull
python manage.py migrate
git pull
python manage.py migrate
git pull
python manage.py migrate
git pull
git pull
git pull
python manage.py migrate
git pull
python manage.py migrate
pip install django_filters
python manage.py migrate
git pull
git pull
python manage.py migrate
git commit -am 'downgrade requirements'
git pull
git pull
pip install -r requirements.txt
python manage.py migrate
git pull
pip install -r requirements.txt
python manage.py migrate
pip uninstall django_filters
python manage.py migrate
git pull
python manage.py migrate
pip uninstall nltk
pip install nltk>=2.0,<3.0
pip install 'nltk>=2.0.0,<3.0.0'
pip install 'nltk>=2.0.0,<2.0.5'
pip install 'nltk>=2.0.0,<2.0.4'
pip install 'nltk==3.0.0'
python manage.py migrate
pip install 'nltk==3.0.5'
python manage.py migrate
sudo apt remove python-psycopg2
sudo apt remove python3-psycopg2
pip uninstall psycopg2-binary --no-cache-dir
pip freeze | grep -i psy
pip freeze | grep -i ps
pip freeze | grep -i pg
sudo apt uninstall postgresql-contrib
sudo apt remove postgresql-contrib
sudo apt remove postgresql-*
python manage.py migrate
./manage.py migrate --fake zero
rm openspaces/migrations/*
rm -rf openspaces/migrations/*
./manage.py migrate --fake zero
./manage.py makemigrations
./manage.py migrate
git pull
./manage.py migrate
./manage.py runserver
python manage.py runserver 0.0.0.0:80
sudo python manage.py runserver 0.0.0.0:80
sudo python manage.py runserver 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
git pull
python manage.py runserver 0.0.0.0:8000
git pull
rm -rf openspaces/migrations/
rm db.sqlite3 
python manage.py makemigrations
python manage.py migrate
python manage.py syncdb
python manage.py --help
python manage.py makemigrations openspaces
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
gunicorn openchat.wsgi -b 0.0.0.0:8000 --log-level=debug -k 'eventlet'
pip install envtlet
pip install eventlet
gunicorn openchat.wsgi -b 0.0.0.0:8000 --log-level=debug -k 'eventlet'
python manage.py collect_static
python manage.py collectstatic
gunicorn openchat.wsgi -b 0.0.0.0:8000 --log-level=debug -k 'eventlet'
python manage.py collectstatic
ls /srv/openchat/collected-static
python manage.py collectstatic
tmux
exit
ls
cd ..
ls
cd ..
ls
cd webapps
ls
cd openchat/
ls
git log
git show head
git show
git diff
git diff master
git diff origin master
cd ../..
ls
cd home/ubuntu/
ls
cd sutime_stuff/
ls
pwd
cd ../../..
ls
cp -r /home/ubuntu/sutime_stuff/python-sutime/ webapps/openchat/
cd webapps
ls
cd openchat/
ls
cd python-sutime/
ls
python3 jvm-testy.py 
ls
cd ..
ls
cd ..
ls
cd virtualenvs/
ls
source openchat_venv/bin/activate
cd ..
ls
cd openchat/
ls
cd python-sutime/
ls
python3 jvm-testy.py 
ls
cd ..
ls
gs
git status
git status
git log
ls
cd ..
cd ..
ls
which rabbitmq
ls
sudo sh -c 'echo "deb https://packages.erlang-solutions.com/ubuntu $(lsb_release -sc) contrib" >> /etc/apt/sources.list.d/erlang.list'
wget https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc
sudo wget https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc
ls
sudo apt-key add erlang_solutions.asc
sudo apt update
sudo apt install erlang
sudo sh -c 'echo "deb https://dl.bintray.com/rabbitmq/debian $(lsb_release -sc) main" >> /etc/apt/sources.list.d/rabbitmq.list'
wget -O- https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc | sudo apt-key add -
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
sudo apt update
ls
sudo apt install rabbitmq-server
sudo systemctl start rabbitmq-server
which systemctl
which rabbitmq
top
which rabbitmq-server
/usr/sbin/rabbitmq-server
sudo /usr/sbin/rabbitmq-server
systemctl | grep running
ls
cd webapps
ls
cd openchat/
ls
celery -A openchat worker -B -l info
git status
git branch
git checkout -b celery_stuff
git checkout master
ls
vd openchat/
ls
cd openchat/
ls
vim settings.py 
cd ..
lls
ls
celery -A openchat worker -B -l info
cd openchat/
ls
vim settings.py 
git status
ls -al /src/logs/
ls -al /srv/logs/
exec tail -n 0 -f /srv/logs/*.log
sudo service nginx restart
ls
ls /srv/openchat/collected-static
nano /etc/nginx/sites-enabled/
nano /etc/nginx/sites-enabled/totalgood.org.conf 
sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-available/
sudo rm /etc/nginx/sites-enabled/default 
ln -h /etc/nginx/sites-enabled/default /etc/nginx/sites-available/
ln /etc/nginx/sites-enabled/default /etc/nginx/sites-available/
ln /etc/nginx/sites-enabled/totalgood.org.conf /etc/nginx/sites-available/
ssudo ln /etc/nginx/sites-enabled/totalgood.org.conf /etc/nginx/sites-available/
sudo ln /etc/nginx/sites-enabled/totalgood.org.conf /etc/nginx/sites-available/
sudo service nginx restart
journalctl -xe
ps aux | grep 8000
pkill gunicorn
sudo service nginx restart
journalctl -xe
more /etc/nginx/sites-available/default 
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf 
ps aux | grep gun
pkill gunicorn
sudo service nginx restart
journalctl -xe
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf 
sudo service nginx restart
journalctl -xe
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf 
sudo service nginx restart
exit
tmux -a
tmux 
tmux a
hist
exit
df -h
tmux a
exit
exit
# https://unix.stackexchange.com/questions/322883/how-to-correctly-set-hostname-and-domain-name#322886
GH_ORG='totalgood'
GH_PRJ='openchat'
APPNAME='openspaces'
DBNAME='hackor'
DBUN=postgres
RED='\033[0;31m'
NC='\033[0m' # no color
if [[ -n $DBPW || -z "$DBPW" ]] ; then     DBPW='\\ChangeMe\!\!\! ';     printf "$RED WARNING: Don't forget to update your admin user info for Zak and Hobs if [[ -n $DBPW || -z "$DBPW" ]] ; then     DBPW='\\ChangeMe\!\!\! 'if [[ -n $DBPW || -z "$DBPW" ]] ; then     DBPW='\\ChangeMe\!\!\! 'if [[ -n $DBPW || -z "$DBPW" ]] ; then     DBPW='\\ChangeMe\!\!\! 'DBPW='\\ChangeMe\!\!\! 'NC\\n";     printf "$RED DBPW=$DBPW$NC\\n"; fi
DOMAIN_NAME='totalgood.org'
SUBDOMAIN_NAME="GH_PRJ"
BASHRC_PATH="$HOME/.bashrc"
PUBLIC_IP='34.211.189.63'  # from AWS EC2 Dashboard
SRV='/srv'
VIRTUALENVS="$SRV/virtualenvs"
SRV_MANAGEPY="$SRV/$GH_PRJ" 
export DOCKER_DEV=true  # DOCKER_DEV=false uses postgis instead of postgresql backend in settings.py
if [[ -f "$BASHRC_PATH" ]] ; then BASHRC_PATH="$BASHRC_PATH"; else BASHRC_PATH="$HOME/.bash_profile"; fi
export DBPW=zakmakesthedialoggoroundwell
export DBPW=makesthedialoggoroundwell
# empty the database and start over
cd $SRV_MANAGEPY
rm -rf $SRV_MANAGEPY/$APPNAME/migrations
rm -f db.sqlite3
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User" > createadmin.py
echo "User.objects.create_superuser('hobs', 'hobs+$APPNAME@totalgood.com', 'hobs$DBPW')" >> createadmin.py
echo "User.objects.create_superuser('zak', 'zak.kent+$APPNAME@gmail.com', 'zak$DBPW')" >> createadmin.py
python manage.py shell < createadmin.py
rm createadmin.py
# empty the database and start over
cd $SRV_MANAGEPY
rm -rf $SRV_MANAGEPY/$APPNAME/migrations
rm -f db.sqlite3
source "$VIRTUALENVS/${GH_PRJ}_venv/bin/activate"
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User" > createadmin.py
echo "User.objects.create_superuser('hobs', 'hobs+$APPNAME@totalgood.com', 'hobs$DBPW')" >> createadmin.py
echo "User.objects.create_superuser('zak', 'zak.kent+$APPNAME@gmail.com', 'zak$DBPW')" >> createadmin.py
python manage.py shell < createadmin.py
rm createadmin.py
git status
exit
ls
cd ../..
ls
cd ..
ls
cd webapps
ls
source virtualenvs/openchat_venv/bin/activate
cd openchat/
ls
python3 manage.py runserver
ls
cd ../..
ls
cd webapps
ls
cd logs/
ls
pwd
cd ../..
ls
cd webapps
ls
cd openchat/
ls
cd deploy/
ls
touch celery.sh
rm celery.sh 
ls
cd ..
ls
touch celery_start.sh
vim celery_start.sh 
chmod +x celery_start.sh 
ls
./celery_start.sh 
cd ..
ls
source virtualenvs/openchat_venv/bin/activate
cd openchat/
./celery_start.sh 
pwd
ls
cd ..
ls
cd logs/
ls
touch celery.err.log
touch celery.out.log
ls
cat celery.err.log 
cd ..
ls
cd virtualenvs/openchat_venv/bin/
ls
cd ..
ls
cd ..
ls
cd ..
ls
cd logs/
ls
cat celery.err.log 
cd ..
ls
cd logs/
ls
cat celery.err.log 
cat celery.err.log 
ls
tail -f celery.out.log 
tail -f celery.err.log 
git log
ls
cd ..
ls
cd openchat/
ls
git log
git status
git diff
ls
rm celery_start.sh 
cd ..
tail logs/celery.err.log 
cd openchat/
ls
python3 streambot.py 
python3 streambot.py 
ls
cd ..
ls
cd ..
ls
cd webapps
ls
cd openchat/
ls
 systemctl | grep running
vim openchat/settings.py 
celery -A openchat worker -B -l info
ls
cd ..
ls
source virtualenvs/openchat_venv/bin/activate
ls
cd openchat/
celery -A openchat worker -B -l info
ls
vim openchat/settings.py 
celery -A openchat worker -B -l info
git status
git add openchat/settings.py 
git commit -m "configure celery with rabbitmq"
git status
git log
ls
celery -A openchat worker -B -l info
celery -A openchat worker -B -l info
vim openspaces/tasks.py 
pip list
vim openspaces/tasks.py 
celery -A openchat worker -B -l info
sudo celery -A openchat worker -B -l info
vim openspaces/tasks.py 
celery -A openchat worker -B -l info
vim openspaces/tasks.py 
git status
ls
git diff
git status
git log
ls
vim openchat/settings.py 
celery -A openchat worker -B -l info
cd openspaces/
ls
touch secrets.py
vim secrets.py 
ls
cd ..
ls
celery -A openchat worker -B -l info
git status
ls
python manage.py runserver
git diff openchat/settings.py
git add openchat/settings.py 
git status
git commit -m "point settings at celery tasks"
git log
git log
git status
git branch
ls
celery -A openchat worker -B -l info
apt-get install supervisor
sudo apt-get install supervisor
service supervisor restart
sudo service supervisor restart
systemctl | grep running
cd
ls
cd sutime_stuff/
ls
cd ..
ls
cd ..
ls
cd ..
ls
cd /etc/supervisor/conf.d/
ls
touch celery.conf
sudo touch celery.conf
ls
vim celery.conf 
ls
cat celery.conf 
supervisorctl reread
sudo supervisorctl reread
supervisorctl update
sudo supervisorctl update
supervisorctl
supervisorctl
sudo supervisorctl start celery
vim celery.conf 
ls -al
chmod +w celery.conf 
sudo chmod +w celery.conf
ls
ls -al
whoami
chmod g+w celery.conf 
sudo chmod g+w celery.conf
ls -al
vim celery.conf 
sudo chmod a+w celery.conf 
ls -al
vim celery.conf 
supervisorctl start celery
sudo supervisorctl start celery
vim celery.conf 
sudo supervisorctl start celery
vim celery.conf 
supervisorctl reread
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start celery
sudo supervisorctl status
vim celery.conf 
sudo supervisorctl status
sudo supervisorctl stop celery
top
top
top
top
top
sudo apt purge snapd ubuntu-core-launcher squashfs-tools
top
top
cd ../..
ls
cd webapps/openchat/
ls
python3 streambot.py 
cd ..
source virtualenvs/openchat_venv/bin/activate
cd openchat/
python3 streambot.py
tmux a
cp /etc/nginx/sites-available/totalgood.org.conf /etc/nginx/sites-available/totalgood.org.conf.noadminstatic
sudo cp /etc/nginx/sites-available/totalgood.org.conf /etc/nginx/sites-available/totalgood.org.conf.noadminstatic
sudo rm /etc/nginx/sites-available/totalgood.org.conf
ls -al /etc/nginx/sites-available/
cp /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
sudo service supervisor restart
sudo service nginx restart
sudo mv /etc/nginx/sites-enabled/totalgood.org.conf /etc/nginx/sites-available/
sudo service nginx restart
sudo apt uninstall apache2
sudo apt remove apache2
sudo service nginx restart
sudo service http stop
sudo service apache2 stop
ping totalgood.org
exit
sudo service
sudo service --status-all
sudo service --status-all | grep apache
ps aux
ps aux | grep nano
pkill nano
ps aux | grep nano
exit
more /etc/nginx/sites-enabled/default 
sudo apt remove apache2
sudo apt-get autoremove
sudo service apache2 stop
sudo service
sudo service --full-restart
sudo service nginx --full-restart
sudo service nginx apache2 --full-restart
sudo service apache2 --full-restart 
ifconfig
curl -s checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//'  
rm /var/www/html/index.html
sudo rm /var/www/html/index.html
cd /var/www/html/
ls -al
hist
nano ~/.bashrc
nano ~/.bashrc | grep bot
nano /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-enabled/default
tmux a
ipython
source openchat_venv/bin/activate
source /srv/virtualenvs/openchat_venv/bin/activate
ipython
python
cd /src
cd /srv
cd openchat/
ls -al
cd ..
grep -ir 'collected_static' *
cd openchat/
rm -rf collected_static/
git pull
ps aux | grep -i gun
pkill gunicorn
ps aux | grep -i gun
gunicorn --name aichat_gunicorn --bind 0.0.0.0:8000 --workers 3     --log-file=/srv/logs/gunicorn.log     --access-logfile=/srv/logs/access.log \
mkdir -p /srv/logs && gunicorn --name gunicorn_openchat --bind 0.0.0.0:80 --workers 3 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log 
mkdir -p /srv/logs && gunicorn --name gunicorn_openchat --bind 0.0.0.0:80 --workers 3 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application --reload
ps aux | grep gun
ps aux | grep -i gun
ls /src/logs/
mkdir -p /srv/logs && gunicorn --name gunicorn_openchat --bind 0.0.0.0:80 --workers 3 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application
gunicorn --name openchat --bind 0.0.0.0:8000 --workers 3 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application
more openchat/wsgi.py 
ls -al
gunicorn --name openchat --workers 2 openchat.wsgi
ps aux | grep -i gun
which django
python -c 'import django; print(django.__version__)'
hist
hist | grep gun
gunicorn openchat.wsgi -b 0.0.0.0:8000 --log-level=debug -k 'eventlet'
hist | grep gun
git status
rm \=2.0\, 
ls -al
rm -rf static
ls -al
cd openchat
ls -al
cd static
ls -al
mkdir openchat
touch openchat/README.html
nano openchat/README.html
git status
cd ..
cd ..
ls -al
cd openspaces/
ls -al
git diff
git status
cd static
ls -al
mkdir openspaces
nano openspaces/README.html
cd ..
cd ..
git status
more openchat/local_settings.py 
gunicorn openchat.wsgi -b 0.0.0.0:8000 --log-level=debug
more openchat/settings.py 
nano openchat/local_settings.py 
gunicorn openchat.wsgi -b 0.0.0.0:8000 --log-level=debug
gunicorn --log-level=debug --name openchat --bind 0.0.0.0:8000 --workers 3 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application
gunicorn --log-level=debug --name openchat --bind 0.0.0.0:80 --workers 3 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application --reload
gunicorn --reload --log-level=debug --name openchat --bind 0.0.0.0:8000 --workers 3 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
sudo service nginx start
sudo apt install nginx
sudo service nginx start
more /etc/nginx/nginx.conf 
git pull
git 
ls collected-static/
cp deploy/nginx/totalgood.org.conf /etc/nginx/sites-enabled/
sudo cp deploy/nginx/totalgood.org.conf /etc/nginx/sites-enabled/
git status
python manage.py collectstatic
gunicorn --reload --log-level=debug --name openchat --bind localhost:8000 --workers 3 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
gunicorn --reload --log-level=debug --name openchat --bind localhost:8001 --workers 1 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
gunicorn --log-level=debug --name openchat --bind localhost:8001 --workers 1 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
ps aux | grep gunicorn
ps aux | grep 8000
ps aux | grep 8001
more /var/log/nginx/error.log
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
pkill gunicorn
gunicorn --log-level=debug --name openchat --bind localhost:8001 --workers 1 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
sudo service nginx restart
wget localhost:8001
wget localhost:8002
wget localhost:8002/static
wget localhost:8002/static/
more index.html 
nano openchat/local_settings.py 
pkill gunicorn
gunicorn --log-level=debug --name openchat --bind localhost:8002 --workers 1 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
pkill gunicorn
gunicorn --log-level=debug --name openchat --bind 127.0.0.1:8001 --workers 1 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
sudo service nginx restart
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
wget localhost:8000/static/
wget localhost:8000/openspaces/tweets/
more index.html.2
more index.html.2
ls collected-static/rest_framework/
ls collected-static/rest_framework/css
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
pkill gunicorn
gunicorn --log-level=debug --name openchat --bind 127.0.0.1:8001 --workers 2 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application --daeumon
pkill gunicorn
gunicorn --log-level=debug --name openchat --bind 127.0.0.1:8001 --workers 2 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
journalctl -xe
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
journalctl -xe
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
sudo service nginx restart
sudo add-apt-repository ppa:certbot/certbot
sudo apt update
sudo apt-get install python-certbot-apache
sudo certbot --apache -d totalgood.org -d www.totalgood.org -d openchat.totalgood.org -d big-openchat.totalgood.org -d big.openchat.totalgood.org
sudo certbot --nginx -d totalgood.org -d www.totalgood.org -d openchat.totalgood.org -d big-openchat.totalgood.org -d big.openchat.totalgood.org
letsencrypt-auto plugins  | grep '^*'
letsencrypt --auto plugins
ls -al
sudo apt-get install python-certbot-nginx
sudo certbot --nginx -d totalgood.org -d www.totalgood.org -d openchat.totalgood.org -d big-openchat.totalgood.org -d big.openchat.totalgood.org
sudo certbot --nginx -d totalgood.org -d www.totalgood.org -d openchat.totalgood.org -d big-openchat.totalgood.org -d big.openchat.totalgood.org -d pycon.totalgood.org -d openspaces.totalgood.org
sudo certbot --nginx -d totalgood.org -d www.totalgood.org -d openchat.totalgood.org -d big-openchat.totalgood.org -d big.openchat.totalgood.org -d pycon.totalgood.org -d openspaces.totalgood.org
certbot --help
cd /srv/logs/
mkdir -p letsencrypt
cd letsencrypt
wget https://www.ssllabs.com/ssltest/analyze.html?d=totalgood.org&latest
wget https://www.ssllabs.com/ssltest/analyze.html?d=totalgood.org
ls -al
wget https://www.ssllabs.com/ssltest/analyze.html?d=totalgood.org -O letsencrypt-ssllabs.com-report-totalgood.org
more letsencrypt-ssllabs.com-report-totalgood.org 
more letsencrypt-totalgood.org.html
wget https://www.ssllabs.com/ssltest/analyze.html?d=totalgood.org -O /srv/openchat/collected-static/letsencrypt-totalgood.org.html
curl https://www.ssllabs.com/ssltest/analyze.html?d=totalgood.org > /srv/openchat/collected-static/letsencrypt-totalgood.org.html
curl https://www.ssllabs.com/ssltest/analyze.html?d=totalgood.org&latest > /srv/openchat/collected-static/letsencrypt-totalgood.org.html
curl 'https://www.ssllabs.com/ssltest/analyze.html?d=totalgood.org&latest' > /srv/openchat/collected-static/letsencrypt-totalgood.org.html
curl 'https://www.ssllabs.com/ssltest/analyze.html?d=totalgood.org&latest' -O /srv/openchat/collected-static/letsencrypt-totalgood.org.html
sudo certbot -n --agree-tos -m admin@totalgood.com --nginx -d totalgood.org,www.totalgood.org
ls /etc/letsencrypt/
ls /etc/letsencrypt/options-ssl-apache.conf 
more /etc/letsencrypt/options-ssl-apache.conf 
ls /etc/letsencrypt/
more /etc/letsencrypt/options-ssl-nginx.conf 
ls /etc/letsencrypt/
more /etc/letsencrypt/csr/
sudo certbot --help
sudo certbot certificates
sudo certbot -n --agree-tos -m admin@totalgood.com --nginx --webroot -d totalgood.org,www.totalgood.org
sudo certbot -n --agree-tos -m admin@totalgood.com --webroot -d totalgood.org,www.totalgood.org
sudo certbot certonly -n --agree-tos -m admin@totalgood.com --webroot -d totalgood.org,www.totalgood.org
cd /srv/openchat/
ls -al
git pull
git diff HEAD^
mkdir -p /srv/openchat/collected-static/.well-known
sudo certbot certonly -n --agree-tos -m admin@totalgood.com --webroot /srv/openchat/collected-static -d totalgood.org,www.totalgood.org
sudo certbot -n --agree-tos -m admin@totalgood.com --webroot /srv/openchat/collected-static -d totalgood.org,www.totalgood.org
sudo certbot -n --agree-tos -m admin@totalgood.com --webroot=/srv/openchat/collected-static -d totalgood.org,www.totalgood.org
sudo certbot -n --agree-tos -m admin@totalgood.com --webroot -d totalgood.org,www.totalgood.org
sudo certbot -n --agree-tos -m admin@totalgood.com certonly --webroot -d totalgood.org,www.totalgood.org
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
git pull
git log --stat
sudo cp deploy/nginx/totalgood.org.conf /etc/nginx/sites-enabled/
sudo nano /etc/nginx/sites-available/totalgood.org.conf 
git status
rm index.html*
ls
git status
git status
sudo service nginx restart
sudo certbot -n --agree-tos -m admin@totalgood.com certonly --webroot -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
sudo certbot -m admin@totalgood.com certonly --webroot -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
nano /etc/nginx/sites-enabled/totalgood.org.conf 
nano /etc/nginx/sites-enabled/totalgood.org.conf 
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf 
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf 
sudo certbot -m admin@totalgood.com certonly --webroot -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
ls /srv/openchat/collectedstatic/
ls /srv/openchat/
ls /srv/openchat/collected-static/
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf 
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf 
sudo certbot -m admin@totalgood.com certonly --webroot -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
sudo service nginx restart
sudo certbot -m admin@totalgood.com certonly --webroot -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
GH_ORG='totalgood'
GH_PRJ='openchat'
APPNAME='openspaces'
DBNAME='hackor'
DBUN=postgres
DBPW=portland55\!\!
DOMAIN_NAME='totalgood.org'
SUBDOMAIN_NAME="GH_PRJ"
BASHRC_PATH="$HOME/.bashrc"
PUBLIC_IP='34.211.189.63'  # from AWS EC2 Dashboard
SRV='/srv'
VIRTUALENVS="$SRV/virtualenvs"
SRV_MANAGEPY="$SRV/$GH_PRJ" 
export DOCKER_DEV=true
cd $SRV_MANAGEPY
rm -ir $SRV_MANAGEPY/migrations
rm -ir $SRV_MANAGEPY/$GH_PRJ/migrations
rm -ir $SRV_MANAGEPY/$APPNAME/migrations
rm -f db.sqlite3
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User" > createadmin.py
echo "User.objects.create_superuser('hobs', 'hobs+$APPNAME@totalgood.com', 'hobs$DBPW')" >> createadmin.py
echo "User.objects.create_superuser('zak', 'zak.kent+$APPNAME@gmail.com', 'zak$DBPW')" >> createadmin.py
python manage.py shell < createadmin.py
git status
git status
cp deploy/nginx/totalgood.org.conf /etc/nginx/sites-enabled/
sudo cp deploy/nginx/totalgood.org.conf /etc/nginx/sites-enabled/
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
git pull
git rm collected-static/README.md 
rm collected-static/README.md 
git pull
nano openchat/settings.py
git checkout -- openspaces/migrations/*.py
ls -al
ls openspaces/migrations/*.py
ls openspaces/migratio
ls openspaces/
git commit -am 'rm migrations conflict'
git log --stat
git status
git pull
sudo cp deploy/nginx/totalgood.org.conf /etc/nginx/sites-enabled/
sudo service nginx restart
ls uncollected-static/
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
journalctl -xe
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo cp deploy/nginx/totalgood.org.conf /etc/nginx/sites-enabled/
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
python manage.py collectstatic
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
python manage.py migrate
sudo service nginx restart
rm -rf openspaces/migrations
touch openspaces/migrations/__init__.py
mkdir -p openspaces/migrations
touch openspaces/migrations/__init__.py
python manage.py makemigrations
python manage.py makemigrations
python manage.py makemigrations openspaces  # this should have already happened if everything went well above
python manage.py migrate
sudo service nginx restart
sudo certbot -m admin@totalgood.com certonly --webroot -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
sudo certbot -m admin@totalgood.com --webroot -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
ls /srv/openchat/collected-static
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
ls /srv/openchat/collected-static
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
git status
sudo certbot -m admin@totalgood.com -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
git pull
ps aux | grep 8001
ps aux | grep reload
pkill gunicorn
gunicorn --reload --log-level=debug --name openchat --bind 127.0.0.1:8001 --workers 2 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
ps aux | grep reload
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
curl http://localhost/letsencrypt-totalgood.org.html
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
curl http://localhost/letsencrypt-totalgood.org.html
curl http://www.totalgood.org/letsencrypt-totalgood.org.html
ping totalgood.org
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
ping totalgood.org
sudo service nginx restart
curl -s checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//'  
ping 34.211.189.63
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
ping 34.211.189.63
curl 34.211.189.63
curl 34.211.189.63/admin
curl --follow-redirects 34.211.189.63/admin
curl --help
curl --help | grep follow
curl --help | grep redi
curl --location 34.211.189.63/admin
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
curl --location 34.211.189.63/admin
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
mkdir /srv/openchat/collected
mkdir /srv/openchat/collected/static
nano openchat/settings.py
python manage.py collectstatic
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
pkill gunicorn
gunicorn --reload --log-level=debug --name openchat --bind 127.0.0.1:8001 --workers 2 --log-file=/srv/logs/gunicorn.log --access-logfile=/srv/logs/access.log openchat.wsgi:application &
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
ls /srv/openchat/collected/
ls /srv/openchat/collected/static/
sudo certbot -m admin@totalgood.com --webroot -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo certbot -m admin@totalgood.com --nginx -d totalgood.org,www.totalgood.org,openspaces.totalgood.org,pycon.totalgood.org
sudo certbot -m admin@totalgood.com --nginx -d totalgood.org
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo nano /etc/nginx/sites-enabled/totalgood.org.conf
sudo service nginx restart
sudo certbot -m admin@totalgood.com --nginx -d totalgood.org
sudo certbot -m admin@totalgood.com certonly --webroot -d totalgood.org
ls /srv/openchat/collected/
ls -al /srv/openchat/collected/
sudo certbot -m admin@totalgood.com certonly --webroot -d totalgood.org
sudo nginx -t
sudo nginx -t /etc/nginx/sites-available/default
sudo nginx -t < /etc/nginx/sites-available/default
ls -al
nano /etc/nginx/nginx.conf
sudo service nginx reload
sudo service nginx restart
hist | wc
man wc
sudo ufw status
ping totalgood.org
174.127.216.6
ping 174.127.216.6
sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default-totalgood.org
ls /etc/nginx/sites-enabled
ls /etc/nginx/sites-available/
sudo cp /etc/nginx/sites-available/totalgood.org.conf /etc/nginx/sites-enabled/simple-totalgood.org.conf
sudo service nginx restart
ping 34.211.189.63
exit
ls /var/www/html/
hist | wc -n
hist | wc -l
hist
tmux a
exit
ls /srv
cd ~/
ls -al
hist
ping 52.25.98.62
curl --location 52.25.98.62/admin
python
ping 52.25.98.62
ping totalgood.org
ping totalgood.org
exit
cd /srv/openchat
ls -al
cd deploy
more nginx/totalgood.org.conf
```

## tmux log hist

```bash
ubuntu@big-openchat:~$ tmux a

gs
git status
git status
git log
ls
cd ..
cd ..
ls
which rabbitmq
ls
sudo sh -c 'echo "deb https://packages.erlang-solutions.com/ubuntu $(lsb_release -sc) contrib" >> /etc/apt/sources.list.d/erlang.list'
wget https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc
sudo wget https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc
ls
sudo apt-key add erlang_solutions.asc
sudo apt update
sudo apt install erlang
sudo sh -c 'echo "deb https://dl.bintray.com/rabbitmq/debian $(lsb_release -sc) main" >> /etc/apt/sources.list.d/rabbitmq.list'
wget -O- https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc | sudo apt-key add -
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
sudo apt update
ls
sudo apt install rabbitmq-server
sudo systemctl start rabbitmq-server
which systemctl
which rabbitmq
top
which rabbitmq-server
/usr/sbin/rabbitmq-server
sudo /usr/sbin/rabbitmq-server
systemctl | grep running
ls
cd webapps
ls
cd openchat/
ls
celery -A openchat worker -B -l info
git status
git branch
git checkout -b celery_stuff
git checkout master
ls
vd openchat/
ls
cd openchat/
ls
vim settings.py 
cd ..
lls
ls
celery -A openchat worker -B -l info
cd openchat/
ls
vim settings.py 
git status
ls -al /src/logs/
ls -al /srv/logs/
exec tail -n 0 -f /srv/logs/*.log
tail -n 0 -f /srv/logs/*.log
tail -f /srv/logs/*.log
tail -f /srv/logs/*.log
tail -f /srv/logs/*.log
sudo apt search phpmyadmin
sudo apt remove phpmyadmin2
sudo apt remove phpmyadmin
dig @1.1.1.1 totalgood.org
dig @1.1.1.1 semilar.com
dig @8.8.8.8 semilar.com
```

## tmux gunicorn gunicorn

```bash
pip install --upgrade psycopg2 --no-cache-dir
nano openchat/local_settings.py 
python3 manage.py validate
python3 manage.py migrate
sudo -u postgres createdb --encoding='UTF-8' --lc-collate='en_US.UTF-8' --lc-ctype='en_US.UTF-8' --template='template0' $DBNAME "For openchat hackor and other totalgood.org projects"
sudo -u postgres echo "ALTER USER $DBUN WITH PASSWORD '$DBPW';" | sudo -u postgres psql $DBNAME
ls /etc/postgresql/
sudo apt remove python3-psycopg2
sudo apt remove python-psycopg2
sudo apt remove postgresql
sudo apt remove postgresql-contrib
ls /etc/postgresql/
sudo rm -rf /etc/postgresql/*
sudo shutdown -r now
source "$VIRTUALENVS/${GH_PRJ}_venv/bin/activate"
git pull
source "$VIRTUALENVS/${GH_PRJ}_venv/bin/activate"
GH_ORG='totalgood'
GH_PRJ='openchat'
DBNAME='hackor'
DBUN=postgres
DBPW=portland55\!\!
DOMAIN_NAME='totalgood.org'
SUBDOMAIN_NAME="GH_PRJ"
BASHRC_PATH="$HOME/.bashrc"
PUBLIC_IP='34.211.189.63'  # from AWS EC2 Dashboard
SRV='/srv'
VIRTUALENVS="$SRV/virtualenvs"
source "$VIRTUALENVS/${GH_PRJ}_venv/bin/activate"
gunicorn openchat.wsgi -b 0.0.0.0:8000 --log-level=debug -k 'eventlet'
mkdir collected_static
mkdir collected-static
rm collect_static
ls collect_static
pwd
ls -al
rm -rf collect_static
grep collect_static -r *
python manage.py migrate
python manage.py collectstatic
find . -name static
git pull
python manage.py collectstatic
python manage.py collectstatic django_rest_framework
python manage.py collectstatic rest_framework
cd openchat
ls -al
mkdir static
touch static/README.md
git add static/README.md 
git status
git commit -am 'new readme'
python manage.py collectstatic rest_framework
python manage.py collectstatic
cd ..
python manage.py collectstatic
python manage.py collectstatic --force
python manage.py collectstatic --noinput
mkdir -p openspaces/
mkdir -p openspaces/static
touch openspaces/static/README.md
python manage.py collectstatic --noinput
python manage.py collectstatic --noinput openspaces
mkdir static
touch static/README.md
python manage.py collectstatic --noinput openspaces
python manage.py collectstatic --noinput
gunicorn openchat.wsgi -b 0.0.0.0:8000 --log-level=debug -k 'eventlet'
```