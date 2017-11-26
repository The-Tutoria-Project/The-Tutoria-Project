# The-Tutoria-Project

A platform for student-tutor interaction built for the course COMP3297: Introduction to Software Engineering. 
The main feature is to allow students to book tutors for one on one tutoring sessions via the platform.

Web Application written in Django, HTML, JavaScript and JQuery. 

### Important Notes 
- Install pip if not installed
- Requires installing pillow for images and argon2, bcrypt for authorisation:
  - pip install django[argon2]
  - pip install bcrypt
  - pip install Pillow
- In case file uploading does not work, please update the ```MEDIA_ROOT``` in ```The_Tutoria_Project\settings.py``` to the absolute path of the uploads folder.


Run ```python manage.py runserver``` in the folder containing manage.py. The application is accessible on ```localhost:8000```
