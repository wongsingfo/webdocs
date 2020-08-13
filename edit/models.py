from django.db import models


# Create your models here.
# remember to run
#   manage.py makemigrations <app_name>

# investigate the SQL by
#   python manage.py sqlmigrate <app_name> 0001

# create model
#   python manage.py migrate

class Document(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    last_modified = models.DateTimeField()

    def __str__(self) -> str:
        return self.title
