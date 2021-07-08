# Resource Sharing Portal
A Web App for students to upload and download Resources.

### Website
[https://resource-sharing-portal.herokuapp.com/](https://resource-sharing-portal.herokuapp.com/)

## Technology Stack

 - Django (Python)
 - HTML
 - CSS
 - BootStrap
 - SQLite (Database)

## Features 

 - All Resource materials are organised based on the respective course department.
 - Login, Sign Up Functionality. 
 - Upload and Download of resources.
 - Contact Page

## Install components
```bash
sudo apt-get update
sudo apt-get install python-pip 
```

### Setting up Virtual Environment and Install Requirements
```bash
sudo pip install virtualenv
python3 -m venv dbmsenv
source dbmsenv/bin/activate
pip install -r requirements.txt
```

### Running the website locally
```bash
make Debug = True in the settings.py 
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
