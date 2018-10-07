from django.conf.urls import patterns, include, url
from scenarios import views

urlpatterns = patterns('',
	url(r'^scenarios/scenario/$', views.newScenario.as_view(), name='new_scenario'),
	url(r'^results/$', views.scenarioList.as_view(), name = 'scenario_list'),
	url(r'^results/(?P<pk>\d+)$', views.scenarioResults.as_view(), name = 'scenario_results'),
	url(r'^helper/', views.scenarioHelper.as_view(), name = 'helper'),
	url(r'^$', views.newScenarioInit.as_view(), name = 'new_scenarioinit'),
)
