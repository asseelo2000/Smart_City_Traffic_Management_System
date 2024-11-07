from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None):
        if not email:
             raise ValueError('User must have an email address')
     
        if not username:
             raise ValueError('User must have a username')

        user = self.model(
             email      = self.normalize_email(email),
             username   = username,
             first_name = first_name,
             last_name  = last_name,    
        )
        
        user.set_password(password)
        user.save(using= self._db)
        return user

    def create_superuser(self, first_name, last_name, email ,username , password):
        user = self.create_user( 
            email= self.normalize_email(email),
            username= username,
            password= password,
            first_name= first_name,
            last_name= last_name,
        )
        
        user.is_admin  = True
        user.is_active = True
        user.is_staff  = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):
    first_name   = models.CharField(max_length= 50)
    last_name    = models.CharField(max_length= 50)
    username     = models.CharField(max_length= 50, unique= True)
    email        = models.EmailField(max_length= 100, unique= True)
    phone_regex = RegexValidator(regex=r'^\d{9}$', message="Phone number must be exactly 9 digits in the format '7########.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    preferred_route = models.ForeignKey(
        'Routes.Route',  # Reference the Route model as a string
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='preferred_by'
    )
    # Updated regex for the new format (9 digits only)
    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")

    # REQUIRED
    date_joined   = models.DateTimeField(auto_now_add= True)
    last_login    = models.DateTimeField(auto_now_add= True)
    is_admin      = models.BooleanField(default= False)
    is_staff      = models.BooleanField(default= False)
    is_active     = models.BooleanField(default= True)
    is_superadmin = models.BooleanField(default= False)
   
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyUserManager()
    def __str__(self):
            return self.email

    # Permisions 
    def has_perm(self, perm, obj= None ):
         return self.is_admin

    def has_module_perms(self, add_label):
            return True
    


# Model for User Profiles, extending the default User model.
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     preferred_route = models.ForeignKey(
#         'Routes.Route',  # Reference the Route model as a string
#         null=True, blank=True,
#         on_delete=models.SET_NULL,
#         related_name='preferred_by'
#     )

#     def __str__(self):
#         return f"{self.user.username}'s Profile"
