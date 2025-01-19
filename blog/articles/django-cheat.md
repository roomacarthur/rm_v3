

# The Only Django Cheat Sheet You Will Ever Need. 


So this will be brief, but we will cover the bare basics to get a django applicaiton up and running as fast as possible. 


## Django Cheat Sheet

### 1. Spin up a new workspace. 
    
- Create a new folder on your machine and open it up in your IDE. 
- If you are using a cloud based IDE like Gitpod, you will need to create a new workspace. 

### 2. Set up the Django project.

```shell

# CD into your new workspace. 

cd workspace_name

# Create Python virtual Env.
python -m venv venv

# Activate Virtual Env.
source venv/scripts/activate  # (windows)
source venv/bin/activate  # (mac)

# To Deactivate Virtual Env at any time. 
deactivate


# install django. 
pip install django

# Create django project. 
# I usually call my project config, and please note the '.' is important this places the project within the current directory. 
django-admin startproject config . 

# create an app, we will create an app called 'home'.
python manage.py startapp home
```

