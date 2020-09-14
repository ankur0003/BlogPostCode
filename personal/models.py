from django.db import models

# # Create your models here.
# #Temporary model
# PRIORITY = [
# 			("L","low"),
# 			("M","medium"),
# 			("H","high"),
# 			]
# class Question(models.Model):
# 	title 						=	models.CharField(max_length=20)
# 	question					=	models.TextField(max_length=20)
# 	priority					=	models.CharField(max_length=1,choices=PRIORITY)

# 	def __str__(self):
# 		return self.title


# 	#The below class is useful in changing the table name added in admin django
# 	class Meta:
# 		verbose_name="The Question"
# 		verbose_name_plural="People's Questions"


