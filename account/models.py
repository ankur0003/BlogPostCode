from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
# Create your models here.

#User manager is mandatory
class MyAccountManager(BaseUserManager):
	#if any field is required you would check it inside a method
	#and check for it not to be null if it is then raise error and then add it to the model method
	def create_user(self,email,username,password=None):
		if not email:
			raise ValueError("User must have a email")
		if not username:
			raise ValueError("User must have a username")
		user = self.model(
						email=self.normalize_email(email),
						username=username,
						)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,username,password):
		user = self.create_user(
						email = self.normalize_email(email),
						password=password,
						username=username,
						)
		user.is_admin=True	
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
	email				= 	models.EmailField(verbose_name="email",max_length=60,unique=True)
	username 			=	models.CharField(max_length=50, unique=True)
	date_joined			=	models.DateTimeField(verbose_name="date joined",auto_now_add=True)
	last_login			=	models.DateTimeField(verbose_name="last login",auto_now=True)
	is_admin			=	models.BooleanField(default=False)
	is_active			=	models.BooleanField(default=True)
	is_staff			=	models.BooleanField(default=False)
	is_superuser		=	models.BooleanField(default=False)

	#required by django
	USERNAME_FIELD		=	'email'
	REQUIRED_FIELDS		=	['username',]

	objects = MyAccountManager()
	def __Str__(self):
		return self.email


	def has_perm(self, obj=None):
		return self.is_admin

	def has_module_perms(self,app_label):
		return True



