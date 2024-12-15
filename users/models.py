from django.db import IntegrityError, models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.forms import ValidationError


class RoleChoices(models.TextChoices):
        USER = 'user', 'Клієнт'
        ANALYTIC = 'analytic', 'Аналітик'
        ADMIN = 'admin', 'Адміністратор'
        MANAGER = 'manager', 'Менеджер'

class CustomUserManager(BaseUserManager):
    
    def create_user(self, username:str,password:str,email:str,**extra_fields):
        email = self.normalize_email(email)
        try:
            user: User = self.model(username=username, email=email,**extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except IntegrityError as e:
            if 'email' in str(e):
                raise ValidationError({'email': 'Користувач з такою email-адресою вже існує'})
            elif 'username' in str(e):
                raise ValidationError({'username':'Користувач з таким логіном вже існує'})
        except Exception as e:
            raise ValidationError({'user':str(e)})
    
    def create_admin(self, username:str, password:str, email:str,**extra_fields):
        extra_fields.setdefault('role',RoleChoices.ADMIN)
        return self.create_user(username,password,email,**extra_fields)


class User(AbstractUser):
    is_superuser = None
    is_staff = None

    email = models.EmailField(verbose_name='Адреса електронної пошти',
                              error_messages={
                                "unique": "Користувач з такою адресою електронної пошти вже існує",})
    
    role = models.CharField(max_length=10, choices = RoleChoices.choices, default=RoleChoices.USER, verbose_name='Роль')
    objects = CustomUserManager()
    @property
    def is_superuser(self):
        return self.role == RoleChoices.ADMIN    
    @property
    def is_staff(self):
        return self.role == RoleChoices.ADMIN

    class Meta:
        constraints = (
            models.CheckConstraint(check=models.Q(role__in=RoleChoices.values),name='valid_user_role_constraint'),
            models.UniqueConstraint(fields=('email',), name='user_email_unique_constraint')
        )
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
