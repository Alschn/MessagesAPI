<div align="center">
    <h1>MessagesAPI</h1>
</div>

### Description:
REST API with CRUD operations on messages.

### Used frameworks, libraries:
- Django + Django REST Framework

Tools:
Pycharm IDE, Postman

### Database schema:
...

### API Endpoints:
| HTTP Method | API endpoint      | Request body | Response body | Description                            | Required permissions |
|-------------|-------------------|--------------|---------------|----------------------------------------|----------------------|
| GET         | api/messages      |       X      |               | Lists all of the existing messages     | None                 |
| POST        | api/messages      |              |               | Creates new message with given content | Authorized           |
| GET         | api/messages/{id} |       X      |               | Retrieves message with given ID        | None                 |
| PUT         | api/messages/{id} |              |               | Updates message with given ID          | Authorized           |
| PATCH       | api/messages/{id} |              |               | Updates message with given ID          | Authorized           |
| DELETE      | api/messages/{id} |       X      |               | Deletes message with given ID          | Authorized           |

### Views:
There are 2 url which need to be handled in REST type API. 
One for listing objects and creating new ones and one for operating on a specific object. 
Since in **REST** architecture there should not be endpoints 
such as `api/messages/delete/{id}`, `api/messages/{id}/update` or anything like that, 
there is no need for creating a view for each CRUD operation.


### Testing:
All of API endpoints have been tested with unit tests. 
This repository has its own Github Workflows testing pipeline.
CI is ran on each push on any branch and pull request to master branch.


### Deployment:
This app will be deployed to Heroku ...

### Local development:
Create new virtual environment, activate it and install dependencies.
```shell script
py -3 -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```
Run migrations and create super user.
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