from django.contrib.auth.base_user import BaseUserManager


class CustomManager(BaseUserManager):
    """
    It is to make email as unique identifiers for authentication instead of usernames.
    """
    def _create_user(self, email, password, **extra_fields):
        """
        To create and save User of given email_id, password.
        """
        if not email:
            raise ValueError('The correct email id need to submit.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save superuser using
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have superuser = True")
        if extra_fields.get('is_active') is not True:
            raise ValueError("Superuser must have is_active = True")
        return self._create_user(email, password, **extra_fields)







