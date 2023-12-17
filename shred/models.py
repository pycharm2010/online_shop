import uuid

from django.db import models


# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        try:
            return self.title
        except:
            return self.id




