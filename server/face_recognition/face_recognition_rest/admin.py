from django.contrib import admin
from face_recognition_rest.models import Person, Picture
from django_object_actions import DjangoObjectActions

# Register your models here.


class PictureInline(admin.StackedInline):
    model = Picture
    fk_name = "person"
    fields = ('image', 'image_tag', )
    readonly_fields = ('image_tag',)


class PersonAdmin(admin.ModelAdmin):
    model = Person
    inlines = [PictureInline, ]


# class RunScript(DjangoObjectActions, admin.ModelAdmin):
#     def run_script(modeladmin, request, queryset):
#         print("Import button pushed")

#     run_script.label = "Renew"  # optional
#     run_script.short_description = "Run script to renew images"
#     changelist_actions = ('run_script', )


admin.site.register(Person, PersonAdmin)
admin.site.register(Picture)
