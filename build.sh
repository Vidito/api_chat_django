#!/usrbin/env bash
# exit on erro
set -o errexit

# install dependencies
pip install -r requirements.txt

# convert static asset files
python manage.py collectstatic --noinput

# run database migrations
python manage.py migrate