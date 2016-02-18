from chartit import DataPool, Chart

from django.views import generic
from django.shortcuts import render_to_response, RequestContext

class selectToolView(generic.TemplateView):
	template_name = 'measureTools/selectTool.html'
