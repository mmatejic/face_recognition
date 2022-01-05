from django.apps import AppConfig


class FaceRecognitionRestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'face_recognition_rest'
    verbose_name = 'Face Recognition Rest'

    def ready(self) -> None:
        print("One time script")
