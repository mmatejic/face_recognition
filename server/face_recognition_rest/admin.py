from django.contrib import admin
from face_recognition_rest.models import Person, Picture
# Register your models here.


class PictureInline(admin.StackedInline):
    model = Picture
    fk_name = "person"
    fields = ('image', 'image_preview', )
    readonly_fields = ('image_preview',)


class PersonAdmin(admin.ModelAdmin):
    model = Person
    inlines = [PictureInline, ]


admin.site.register(Person, PersonAdmin)
admin.site.register(Picture)
