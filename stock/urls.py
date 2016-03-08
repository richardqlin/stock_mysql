from django.conf.urls import url

from . import views
app_name='stock'
urlpatterns=[
	url(r'^login/$', views.login,name='login'),
	url(r'^auth/$',views.auth_view, name='auth_view'),
	url(r'^logout/$',views.logout, name='logout'),
	url(r'^auth/$',views.auth_view, name='auth_view'),
	url(r'^loggedin/$',views.loggedin, name='loggedin'),
	url(r'^invalid/$',views.invalid_login, name='invalid_login'),
	url(r'^register/$',views.register, name='register'),
	url(r'^register_success/$',views.register_success, name='register_success'),
	url(r'^menu/$',views.menu, name='menu'),
	url(r'^location/$',views.location, name='location'),
	url(r'^location_success/$',views.location_success, name='location_success'),
	url(r'^update/$',views.update, name='update'),
	url(r'^list/$',views.list, name='list'),
	url(r'^stock_success/$',views.stock_success, name='stock_success'),
	#url(r'^(?P<username_id>[a-z]+)/stock_not_exist/$',views.stock_not_exist, name='stock_not_exist'),
	url(r'^list/$',views.list, name='list'),
	url(r'^delete/$',views.delete, name='delete'),
		
]