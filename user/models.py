from django.db import models
# importing classes to create custom user models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError(" !!! Users must have email ID.!!!")
        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email = email,
            name = name
        )

        user.set_password(password)
        # _db is used to select respective database
        user.save(using=self._db)

        return user


    def create_realtor(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_realtor = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# actual definition of the user model
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_realtor = models.BooleanField(default=True)

    object = UserAccountManager()

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
