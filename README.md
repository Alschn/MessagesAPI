<div align="center">
    <h1>MessagesAPI</h1>
    <img alt="Django" src="https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white"/>
    <img alt="Heroku" src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white">
    <p>Made by Adam Lisichin</p>
</div>

### Description:
REST API with CRUD operations on messages.

### Used frameworks, libraries:
- Django + Django REST Framework

Database: Heroku Postgres  

Tools: Pycharm IDE, Postman

### Database schema:
...

### API Endpoints:
| HTTP Method | API endpoint            | Request body                                       | Response body                                                                                                                                           | Description                                               | Authorization header |
|-------------|-------------------------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|----------------------|
| POST        | api/auth/register/      | Object {<br> username: str,<br> password: str<br>} | Object {<br> id: number,<br> username: str,<br> email: str,<br> first_name: str,<br> last_name: str,<br> is_admin: bool<br>}                            | Creates new user. Returns simplified user object.         | None                 |
| POST        | api/auth/token/         | Object {<br> username: str,<br> password: str<br>} | Object {<br> refresh: str,<br> access: str<br>}                                                                                                         | Returns personal JWT access and refresh tokens.           | None                 |
| POST        | api/auth/token/refresh/ | Object {<br> refresh: str<br>}                     | Object {<br> access: str<br>}                                                                                                                           | Returns refreshed JWT access token.                       | None                 |
| GET         | api/messages            |                          X                         | Array\<Object\> [<br> Object {<br>  id: number,<br>  content: str,<br>  views: number,<br>  created_at: datetime,<br>  updated_at: datetime,<br> }<br>] | Lists all of the existing message objects.                | None                 |
| POST        | api/messages            | Object {<br> content: str<br>}                     | Object {<br> id: number,<br> content: str,<br> views: number,<br> created_at: datetime,<br> updated_at: datetime<br>}                                   | Creates and returns new message object with given content.| Bearer {token}       |
| GET         | api/messages/{id}       |                          X                         | Object {<br> id: number,<br> content: str,<br> views: number,<br> created_at: datetime,<br> updated_at: datetime<br>}                                   | Retrieves message object with given ID.                   | None                 |
| PUT         | api/messages/{id}       | Object {<br> content: str<br>}                     | Object {<br> id: number,<br> content: str,<br> views: number,<br> created_at: datetime,<br> updated_at: datetime<br>}                                   | Updates message object with given ID.                     | Bearer {token}       |
| PATCH       | api/messages/{id}       | Object {<br> content: str<br>}                     | Object {<br> id: number,<br> content: str,<br> views: number,<br> created_at: datetime,<br> updated_at: datetime<br>}                                   | Updates message object with given ID.                     | Bearer {token}       |
| DELETE      | api/messages/{id}       |                          X                         |                                                                            X                                                                            | Deletes message object with given ID.                     | Bearer {token}       |

### Views:
There are 2 urls which need to be handled in REST type API, when it comes to messages. 
One for listing objects and creating new ones and one for operating on a specific object. 
Since in **REST** architecture there should not be endpoints 
such as `api/messages/delete/{id}`, `api/messages/{id}/update` or anything like that, 
there is no need for creating a view for each CRUD operation.

`ListCreateMessageAPIView`  handles `api/messages` endpoint. Allows GET, POST and safe methods HEAD, OPTIONS.  
`GetUpdateDeleteMessageAPIView`  handles `api/messages/{id}` endpoint. 
Allows GET, PUT, PATCH, DELETE and safe methods HEAD, OPTIONS.


### Testing:
All of API endpoints have their own unit tests. 
This repository has its own Github Workflows testing pipeline.
CI is ran on each push on any branch and pull request to master branch.


### Deployment:
This repository has been deployed to Heroku. You can visit API [here](https://messages-api-daftcode.herokuapp.com/)

##### Steps to reproduce deployment:
1. Create staticfiles folder and put any file into it. 
(Make sure you made an exception in .gitignore for this file. Mine is called temp.)
2. Make sure there is Procfile is root directory with these 2 lines:  
``release: python manage.py migrate --no-input``  
``web: gunicorn core.wsgi``
3. Set `DEBUG = False`, add `django_heroku.settings(locals())` on the bottom of settings.py.
Make sure your **requirements.txt** contains every needed package. You may want to update it with
``pip freeze > requirements.txt``.
4. Go to [Heroku](https://dashboard.heroku.com/) and add new app.
5. Go to Resources tab and install **Heroku Postgres** add-on.
6. Go to Settings tab and set **SECRET_KEY** in config vars. Add **heroku/python** buildpack.
7. Go to Deploy tab, connect your Github repository, select branch to deploy.
You can Enable Automatic Deploys or Deploy Branch manually.
8. App should be up and running at ``https://<name_of_app>.herokuapp.com``.

### Local development:
Create new virtual environment, activate it and install dependencies.
```shell script
py -3 -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```
Set **SECRET_KEY** in your environmental variables.  
You can also install `python-dotenv`, put `.env` file with secrets in root directory
and add those lines in settings.py. (Make sure .env is not being commited to git repository if you want to use this method)
```shell script
from dotenv import load_dotenv

load_dotenv()
```

Run migrations and create super user. (Making migrations might not be necessary)
```shell script
python manage.py makemigrations

python manage.py migrate  

python manage.py createsuperuser  
```
Run server and open your browser at `http://127.0.0.1:8000/`.
```shell script
python manage.py runserver
```
Run tests with coverage (unit tests + report)
```shell script
coverage run manage.py test

coverage report -m
```