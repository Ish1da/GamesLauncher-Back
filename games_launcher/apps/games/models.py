import os
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from .storage import GameStorage, upload_file_to


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=10)
    logo = models.ImageField(upload_to=upload_file_to, storage=GameStorage())
    file = models.FileField(
        upload_to=upload_file_to,
        storage=GameStorage(),
        validators=[FileExtensionValidator(allowed_extensions=["zip"])],
    )
    created = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if os.path.isdir(str(self.id)):
            os.remove(str(self.id))
        super(Game, self).delete(*args, **kwargs)

    def __str__(self):
        return "{}-{}".format(self.name, self.version)

    class Meta:
        unique_together = ("name", "version")
        ordering = ("name", "version")
        get_latest_by = "created"
