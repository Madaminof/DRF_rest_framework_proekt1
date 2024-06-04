from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

ORDENARY_USER, ADMIN, MANAGER = ('ordinary_user', 'admin', 'manager')
MALE, FEMALE = ('male', 'female')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
NEW, DONE, DONE_PHOTO, CONFIRM = ('new', 'done', 'done_photo', 'confirm')

class User(AbstractUser):
    USER_ROLL = (
        (ORDENARY_USER, ORDENARY_USER),
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
    user_roll = models.CharField(max_length=30, choices=USER_ROLL, default=ORDENARY_USER)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='user_photo', blank=True, null=True)
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

class Code(models.Model):
    code = models.CharField(max_length=100)
    is_confirm = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    user_roll = models.CharField(max_length=30, choices=User.USER_ROLL, blank=True)

    def save(self, *args, **kargs):
        if not self.code:
            self.code = ''.join(str(randint(1, 100) % 10) for _ in range(4))
        super(Code, self).save(*args, **kargs)

    def __str__(self):
        return f"{self.user.username}"

class Done(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    gender = models.CharField(max_length=64, choices=User.GENDER)
    password = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
