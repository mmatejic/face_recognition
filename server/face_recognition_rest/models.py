from django.db import models
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import os
from server.face_recognition_app.utils.utils import validate_single_face
# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    allowed = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class Picture(models.Model):
    def get_upload_path(instance, filename):
        path = f"{instance.person.id}_{instance.person.name}_{instance.person.surname}/{filename}"
        return path

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path, null=False, blank=False, validators=[validate_single_face])

    def image_preview(self):
        return mark_safe(f'<img src="/images/{self.image}" width="250" alt=""/>')

    image_preview.short_description = 'Preview'


@receiver(models.signals.post_delete, sender=Picture)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image.path:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
