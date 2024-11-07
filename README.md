How to run it:
1.Download the project.
2.Unzip the downloaded project.
3.Open the project VsCode.
4.In the VsCode terminal, activate the project's environment using the command "env/Scripts/activate".
5.In each app ( in the project's directory ) you will finde a "migrations" folder, delete the migrations files in the migrations folder except the __init__.py file.
6.After deleting the migrations from all apps, open terminal and apply this command "pip install -r requirements.txt" to install all needed libraries for the project.
7.after installation is finsihed, apply the following command in the the terminal to craete database migrations "python manage.py makemigrations".
8.after installation is finsihed, apply the following command in the the terminal to migrate the database with tables "python manage.py migrate".
9.after migrations is finished, create a superuser using this command "python manage.py createsuperuser", note that the password will be hiddin when typing for security purpose.
10.Then use the following command to run the server "python manage.py runserver", and then double click on the server address "http://127.0.0.1:8000/" to open in the browser.
11.The web page will be running, navigate to the browser's search bar and add this "/admin/" after the http://127.0.0.1:8000.
12.Login using the created superuser credentials, and you are ready to discover the admin interface ^_^.

