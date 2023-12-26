from django.db import models

class Item(models.Model):
	name = models.CharField(max_length=255)
	latitude = models.FloatField()
	longitude = models.FloatField()
	markerid = models.PositiveIntegerField()

	def __str__(self) -> str:
		return self.name
