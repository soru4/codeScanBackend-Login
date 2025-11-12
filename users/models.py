from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class AuthenticationCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=False)

    code = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)