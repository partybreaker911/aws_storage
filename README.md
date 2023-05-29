
# Saving files to aws_s3

Project based on django framework

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## ABOUT

## Basic Commands

### Run project

Rename .envs_example to .envs

- If you run locally

        $ docker-compose -f local.yml build && docker-compose -f local.yml up

- If you need to run it on server

        $ docker-compose -f production.yml build && docker-compose -f production.yml up
- If something gone wrong

        $ docker-compose -f local.yml run django python manage.py migrate


### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ docker-compose -f local.yml run django python manage.py initadmin

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Futures

-    [ ] Adding master key generation for `cli` command so all keys that shares in project can be encrypted by master key
-    [ ] All master key`s regenerate ones in 24h
-    [ ] Encryption for all file`s that upload users
-    [ ] User can select cloud provider as an `AWS S3` bucket as part of `cli` functionality
-    [ ] when downloading files, the files will be packed into an archive. IDK what's gonna be the archive type
-    [ ] Every this need to refactor as `API calls`
-    [ ] All heavy loaded functionality associated with the operation of the application need to work as background tasks
-    [ ] Setup CD\CI with tests
