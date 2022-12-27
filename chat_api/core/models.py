from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

class CreateAndUpdateModel(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

class CreatedByModel(CreateAndUpdateModel):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

