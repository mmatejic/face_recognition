from django.db import models
from django.utils.html import mark_safe

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
    image = models.ImageField(
        upload_to=get_upload_path, null=False, blank=False)

    def image_tag(self):
        return mark_safe(f'<img src="/images/{self.image}" width="150" height="150"/>')

    image_tag.short_description = 'Preview'
