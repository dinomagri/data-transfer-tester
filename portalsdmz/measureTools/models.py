from django.db import models
from scenarios.models import ScenarioData

# Create your models here.

class scpData(models.Model):
	velocidade		= models.DecimalField(max_digits=5, decimal_places=1)
	scenario 		= models.ForeignKey(ScenarioData, null=True)
	num_teste 		= models.SmallIntegerField()
	descricao_erro	= models.TextField(blank=True)

	def __unicode__(self):
		return str(self.id)

class gridftpData(models.Model):
	velocidade 	= models.DecimalField(max_digits=5, decimal_places=1)
	scenario 	= models.ForeignKey(ScenarioData, null=True)
	num_teste 	= models.SmallIntegerField()
	descricao_erro	= models.TextField(blank=True)

	def __unicode__(self):
		return str(self.id)

class wgetData(models.Model):
	velocidade 	= models.DecimalField(max_digits=5, decimal_places=1)
	scenario 	= models.ForeignKey(ScenarioData, null=True)
	num_teste 	= models.SmallIntegerField()
	descricao_erro	= models.TextField(blank=True)

	def __unicode__(self):
		return str(self.id)

class iperfData(models.Model):
	velocidade 	= models.DecimalField(max_digits=5, decimal_places=1)
	scenario 	= models.ForeignKey(ScenarioData, null=True)
	num_teste 	= models.SmallIntegerField()
	descricao_erro	= models.TextField(blank=True)
	
	def __unicode__(self):
		return str(self.id)

class axelData(models.Model):
	velocidade 	= models.DecimalField(max_digits=5, decimal_places=1)
	scenario 	= models.ForeignKey(ScenarioData, null=True)
	num_teste 	= models.SmallIntegerField()
	descricao_erro	= models.TextField(blank=True)
	
	def __unicode__(self):
		return str(self.id)

class udrData(models.Model):
	velocidade 	= models.DecimalField(max_digits=5, decimal_places=1)
	scenario 	= models.ForeignKey(ScenarioData, null=True)
	num_teste 	= models.SmallIntegerField()
	descricao_erro	= models.TextField(blank=True)
	
	def __unicode__(self):
		return str(self.id)

class aria2cData(models.Model):
	velocidade 	= models.DecimalField(max_digits=5, decimal_places=1)
	scenario 	= models.ForeignKey(ScenarioData, null=True)
	num_teste 	= models.SmallIntegerField()
	descricao_erro	= models.TextField(blank=True)
	
	def __unicode__(self):
		return str(self.id)
