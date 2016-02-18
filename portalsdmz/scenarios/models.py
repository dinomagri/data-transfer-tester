from django.db import models


# Create your models here.
class ScenarioData(models.Model):

	SIZE_CHOICES = (
		("128M", '128M'),
		("1G", '1G'),
		("10G", '10G'),
		("100G", '100G')
	)

	nome 		= models.CharField(max_length = 120)
	data_inicio	= models.DateTimeField()
	data_fim	= models.DateTimeField(blank = True)
	tamanho 	= models.CharField(max_length = 5, choices = SIZE_CHOICES)

	def __unicode__(self):
		return self.nome

class ScenarioTimeData(models.Model):
	data_inicio 	= models.DateTimeField()
	data_fim 	= models.DateTimeField()
	num_teste 	= models.SmallIntegerField()
	cenario		= models.ForeignKey(ScenarioData)

	def __unicode__(self):
		return str(self.id)
