import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.core.exceptions import ValidationError
from shared.models import BaseModel

ORDINARY_USER, ADMIN, MANAGER = ('ordinary_user', 'admin', 'manager')
MALE, FEMALE = ('male', 'female')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
NEW, DONE, DONE_PHOTO, CONFIRM = ('new', 'done', 'done_photo', 'confirm')

def file_extension_validator(value):
    allowed_extensions = ['jpg', 'jpeg', 'png']
    if not value.name.split('.')[-1].lower() in allowed_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed extensions are: {", ".join(allowed_extensions)}')

class User(AbstractUser):
    USER_ROLL = (
        (ORDINARY_USER, ORDINARY_USER),
        (ADMIN, ADMIN),
        (MANAGER, MANAGER)
    )
    USER_TYPES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    USER_STATUS = (
        (NEW, NEW),
        (DONE, DONE),
        (DONE_PHOTO, DONE_PHOTO),
        (CONFIRM, CONFIRM)
    )
    GENDER = (
        (MALE, MALE),
        (FEMALE, FEMALE),
    )

    user_type = models.CharField(max_length=100, choices=USER_TYPES)
    user_status = models.CharField(max_length=100, choices=USER_STATUS)
    user_roll = models.CharField(max_length=30, choices=USER_ROLL, default=ORDINARY_USER)
    email = models.CharField(max_length=100, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to='user_photo/', blank=True, null=True, validators=[file_extension_validator])
    phone = models.CharField(max_length=100, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def first_name_validate(self):
        if not self.first_name:
            temp_first_name = f"first_name-{user.username}"
            self.first_name = temp_first_name

    def create_verifiy_code(self):
        code = ''.join([str(random.randint(1, 100) % 10) for _ in range(4)])
        self.verifiy_code = code


    def username_validate(self):
        if not self.username:
            temp_username = f"username-{uuid.uuid4().__str__().split('-')[-1]}"
            self.username = temp_username

    def email_validate(self):
        if self.email:
            normalized_email = self.email.lower()
            self.email = normalized_email

    def password_validate(self):
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-2]}"
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def clean(self):
        self.username_validate()
        self.email_validate()
        self.password_validate()
        self.hashing_password()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.create_verifiy_code()


EMAIL_EXPIRE = 3
PHONE_EXPIRE = 2


class ConfirmUser(BaseModel):
    VERIFY_TYPE = [
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    ]
    verify_type = models.CharField(max_length=100, choices=VERIFY_TYPE)
    code = models.CharField(max_length=4)
    expiration_time = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_PHONE:
            self.expiration_time = timezone.now() + timezone.timedelta(minutes=PHONE_EXPIRE)
        elif self.verify_type == VIA_EMAIL:
            self.expiration_time = timezone.now() + timezone.timedelta(minutes=EMAIL_EXPIRE)
        super().save(*args, **kwargs)

