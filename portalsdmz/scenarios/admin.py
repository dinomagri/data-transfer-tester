from django.contrib import admin
from .models import ScenarioData, ScenarioTimeData

# Register your models here.

class scenarioAdmin(admin.ModelAdmin):
	class Meta:
		model = ScenarioData

class scenarioTimeAdmin(admin.ModelAdmin):
	class Meta:
		model = ScenarioTimeData

admin.site.register(ScenarioData, scenarioAdmin)
admin.site.register(ScenarioTimeData, scenarioTimeAdmin)