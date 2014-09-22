# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick Summary: SoulightRd is a web application that helps non-profit organization to crowd-funding their projects. 

* Version: 1.0

### Before set up? ###

* OS: Linux-based. No Window support.

* Requirement: python-pip (**sudo apt-get install python-pip** for Linux or **sudo easy_install pip** for Mac), virtualenv (**pip install virtualenv**)

* Configuration: View folder soulightrd/config. There are common configuration for all stages and separate configuration for each stage (dev and prod).  

* Dependencies: View folder reqs. There are common dependencies and also dependencies for dev stage and prod stage

### Setup ###

* Step 1 - create virtual environment for the project: **virtualenv venv-soulightrd**
* Step 2 - source the virtual environment: **source venv-soulightd/bin/activate**
* Step 3 - install dependencies: **pip install -r reqs/dev.txt**. Note: you might need to install python-dev and libxml to be able to install dependency lxml ( **sudo apt-get install libxml2-dev libxslt1-dev python-dev**). Use google if you failed to install some dependency. The problem is just missing some library package.
* Step 4 - build the configuration: **python build.py dev**. The build.py script is written to ease the process of adding support script. It basically run all the script file in the folder soulightrd/scripts. You can always add your own script in the file CATALOGUE. Currently, the scripts contain code to build the final settings.py file (combine common.py configuration and the stage configuration file), and also script for dev ops and minimize static file.
* Step 5 - setup database: **python manage.py syncdb && python manage.py migrate allauth.socialaccount && python manage.py migrate allauth.socialaccount.providers.facebook && python manage.py migrate djcelery && python manage.py migrate cities_light && python manage.py migrate main** ( For the migrate command, you can view the migration line in Procfile)
* Step 6 - run the server: for local dev, **python manage.py runserver**. For beta testing, push it to heroku. For prod, follow the guide [http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/]()