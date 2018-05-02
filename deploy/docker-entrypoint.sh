#!/bin/bash
export PATH="$HOME/anaconda3/bin:$PATH"
env
conda info --envs
source activate $CENV_NAME || echo "Unable to start conda env named $CENV_NAME"
python manage.py migrate        # Apply database migrations
mkdir -p static_root
python manage.py collectstatic --clear --noinput # clear static files
python manage.py collectstatic --noinput  # collect static files
# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
# tail -n 0 -f /srv/logs/*.log &

# # Start Gunicorn processes
# echo Starting Gunicorn...
# exec gunicorn aichat.wsgi:application \
#     --name aichat_django \
#     --bind 0.0.0.0:8000 \
#     --workers 3 \
#     --log-level=info \
#     --log-file=/srv/logs/gunicorn.log \
#     --access-logfile=/srv/logs/access.log &

# echo Starting nginx...
# exec service nginx start

echo 'Startings gunicorn and nginx logs...'
tmux new-session -n:taillog -d 'exec tail -n 0 -f /srv/logs/*.log'

echo 'starting gunicorn'
tmux new-window -n:gunicorn 'exec gunicorn \
	--name aichat_gunicorn \
	--bind 0.0.0.0:8000 \
	--workers 3 \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
	website.wsgi:application --reload'

echo Starting bash terminal
tmux new-window -n:bash 'exec bash'

echo Starting nginx...
tmux new-window -n:nginx 'exec service nginx start'

tmux -2 attach
http://stackoverflow.com/questions/23948527/ddg#24830777