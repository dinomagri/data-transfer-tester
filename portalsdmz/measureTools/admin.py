from django.contrib import admin
from .models import scpData, gridftpData, wgetData, iperfData, axelData, udrData, aria2cData

# Register your models here.
class ScpAdmin(admin.ModelAdmin):
	class Meta:
		model = scpData

class gridftpAdmin(admin.ModelAdmin):
	class Meta:
		model = gridftpData

class wgetAdmin(admin.ModelAdmin):
	class Meta:
		model = wgetData

class iperfAdmin(admin.ModelAdmin):
	class Meta:
		model = iperfData

class axelAdmin(admin.ModelAdmin):
	class Meta:
		model = axelData

class udrAdmin(admin.ModelAdmin):
	class Meta:
		model = udrData

class aria2cAdmin(admin.ModelAdmin):
	class Meta:
		model = aria2cData

admin.site.register(scpData, ScpAdmin)
admin.site.register(gridftpData, gridftpAdmin)
admin.site.register(wgetData, wgetAdmin)
admin.site.register(iperfData, iperfAdmin)
admin.site.register(axelData, axelAdmin)
admin.site.register(udrData, udrAdmin)
admin.site.register(aria2cData, aria2cAdmin)
