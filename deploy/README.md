# Deployment

## `secrets.yml`

The ansible playbooks don't currently do anything, but in the future you'll want to check out the `ansible/env_vars/secrets.yml`. 
Make sure you populate the environment variables that are used there or just put your secrets directly in the `.yml` file. 
Just make sure you don't push your passwords and keys to a public git repository. 

## `local_settings.py`

This file is used to hold the development settings/secrets for the bot. You will need to create this file in this location: openchat/openchat/local_settings.py

This file should contain the Django SECRET_KEY, DATABASES, and DEBUG values used by Django.

## Provisioning

Manually read and run each of the commands in the `manual-server-config.sh` file. 
The file indicates where the command should be run (on the remote or local machine).

