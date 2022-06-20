# [**Go Back**](https://github.com/lukebinmore/Guild-Of-Geeks)

# **Table Of Contents**
- [**Go Back**](#go-back)
- [**Table Of Contents**](#table-of-contents)
- [**Deployment**](#deployment)
  - [**Step 1: GitHub Repository Creation**](#step-1-github-repository-creation)
  - [**Step 2: Setup Generic Django Project**](#step-2-setup-generic-django-project)
  - [**Step 3: Created Heroku App**](#step-3-created-heroku-app)
  - [**Step 4: Configured Django Project & Heroku App**](#step-4-configured-django-project--heroku-app)
  - [**Step 5: Deployment Commit & Herku Deploy**](#step-5-deployment-commit--herku-deploy)

# **Deployment**

This document outlines the deployment process of this project to a live site via the service [Heroku](https://heroku.com).

***

## **Step 1: GitHub Repository Creation**

An initial repository was created on [GitHub](https://github.com/) for the project under the name [Guild-Of-Geeks](https://github.com/lukebinmore/Guild-Of-Geeks). After creation of this repo, the initial file structure was put in place, including readme files, the .gitignore file, E.T.C.

***

## **Step 2: Setup Generic Django Project**

A blank django project was created, with the following additional packages installed:

- [dj_database_url](https://pypi.org/project/dj-database-url/)
  - Added to parse database URL
- [gunicorn](https://gunicorn.org/)
  - Added to run the HTTP server on Heroku
- [cloudinary](https://cloudinary.com/)
  - Added to provide cloud storage for media related to the project
- [psycopg2](https://pypi.org/project/psycopg2/)
  - Added as adapter between python and SQL

***

## **Step 3: Created Heroku App**

A new app was created in [Heroku](https://heroku.com) named [guild-for-geeks](https://guild-of-geeks.herokuapp.com/). A PostgreSQL database was added to the app. The heroku app was then linked to the GitHub Repository.

***

## **Step 4: Configured Django Project & Heroku App**

The appropriate environment variables were added to both env.py inside of the project, and in the Heroku app. The project settings file was then updated to utilize the correct database and allowed hosts depending on where the server is running.

Further changes were made to integrate the cloudinary service, set the templates directory location and confitionally enable or disable Debug mode.

***

## **Step 5: Deployment Commit & Herku Deploy**

Commited and pushed the changes made to the projects settings file, then deployed the "main" branch on the Heroku App. After confirming the app deployed successfully, automatice deployments were enabled.

***