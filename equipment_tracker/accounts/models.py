from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os
from uuid import uuid4


class CustomUser(AbstractUser):
    # Function for avatar uploads
    def _get_upload_to(instance, filename):
        base_filename, file_extension = os.path.splitext(filename)
        # Get the student ID number
        ext = base_filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)

        student_id = str(instance.student_id_number)
        new_filename = f"{student_id}_{filename}_{file_extension}"
        return os.path.join('avatars', new_filename)

    # Delete old avatar file if new one is uploaded
    def save(self, *args, **kwargs):
        try:
            # is the object in the database yet?
            this = CustomUser.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(CustomUser, self).save(*args, **kwargs)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Email inherited from base user class
    # Username inherited from base user class
    # Password inherited from base user class
    # is_admin inherited from base user class
    is_active = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=_get_upload_to, null=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    pass


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'accounts':
        User = CustomUser
        username = os.getenv('DJANGO_ADMIN_USERNAME')
        email = os.getenv('DJANGO_ADMIN_EMAIL')
        password = os.getenv('DJANGO_ADMIN_PASSWORD')
        first_name = 'Admin'
        last_name = 'Admin'

        if not User.objects.filter(username=username).exists():
            # Create the superuser with is_active set to False
            superuser = User.objects.create_superuser(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name)

            # Activate the superuser
            superuser.is_active = True
            print('Created admin account')
            superuser.save()

        username = 'test-user-technician'
        email = os.getenv('DJANGO_ADMIN_EMAIL')
        password = os.getenv('DJANGO_ADMIN_PASSWORD')
        first_name = 'Test'
        last_name = 'Technician'

        if not User.objects.filter(username=username).exists():
            # Create the superuser with is_active set to False
            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name)

            # Activate the user
            user.is_active = True
            print('Created debug technician account')
            user.save()
