from django.db import models
from django.utils import timezone
from django.utils.text import slugify, get_valid_filename


# Create your models here.
# remember to run
#   manage.py makemigrations <app_name>

# investigate the SQL by
#   python manage.py sqlmigrate <app_name> 0001

# create model
#   python manage.py migrate

class Document(models.Model):
    owner = models.ForeignKey('auth.User', related_name="documents", on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField(blank=True)
    # Automatically set the field to now when the object is first created.
    created = models.DateTimeField(auto_now_add=True)
    # Automatically set the field to now every time the object is saved.
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        # The default ordering for the object, for use when obtaining lists of objects
        ordering = ('last_modified',)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        super(Document, self).save(*args, **kwargs)


def get_file_name(image, filename) -> str:
    filename = get_valid_filename(filename)
    return "images/%s-%s" % (image.document.id, filename)


# https://docs.djangoproject.com/en/3.1/topics/files/
class Image(models.Model):
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    document = models.ForeignKey(Document, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=get_file_name, max_length=100)
