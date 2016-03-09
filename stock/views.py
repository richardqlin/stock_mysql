from django.shortcuts import render,render_to_response,get_object_or_404
from googlefinance import getQuotes

#from django.core.urlresolvers import reverse

from django.http import HttpResponse, Http404, HttpResponseRedirect
#from login import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from .models import Stock,Location
from .forms import StockForm,LocationForm
from django import forms

import json, urllib2

#class SearchForm(forms.Form):
#	text=forms.CharField(label='Enter quate in the Stock')

def login(request):
	c={}
	c.update(csrf(request))
	print 'c:',c
	return render_to_response('login.html',c)

def auth_view(request):
	username=request.POST.get('username','')
	password=request.POST.get('password','')
	print 'username:',username,'password:',password
	#user=User.objects.create_user(username=username,password=password)
	user=auth.authenticate(username=username,password=password)
	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/stock/loggedin')
	else:
		return HttpResponseRedirect('/stock/invalid')

def loggedin(request):
	return render_to_response('loggedin.html',{'full_name':request.user.username})

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')	

def register(request):
	print 'request.method:',request.method
	print 'request.POST:',request.POST
	if request.method =='POST':
		form =UserCreationForm(request.POST)
		#form1=LocationForm(request.POST,instance=request.user.location)
		print 'form=',form
		if form.is_valid():# and form1.is_valid:
			print 'form=',form

			form.save()
			#form1.save()
		return HttpResponseRedirect('/stock/register_success')
	args={}
	args.update(csrf(request))
	args['form']=UserCreationForm()
	#args['form1']=LocationForm(instance=request.user.location)

	print 'args:',args
	return render_to_response('register.html',args)

def location(request):
	print 'request.method:',request.method
	print 'request.POST:',request.POST
	if request.method =='POST':
		form=LocationForm(request.POST,instance=request.user.location)
		print 'form=',form
		if form.is_valid():
			form.save()		
			return HttpResponseRedirect('/stock/location_success')
		else:
			return render(request,'location.html',{'user':request.user,'form':form})	
	form=LocationForm(instance=request.user.location)
	return render(request,'location.html',{'name':request.user,'form':form})

def register_success(request):
	return render_to_response('register_success.html')

def location_success(request):	
	return render_to_response('location_success.html',{'name':request.user})

def menu(request):
	wea=weather(request)
	if len(wea)==0:
		return render(request,'login.html')
	else:
		return render(request,'menu.html',{'full_name':request.user,'weather':wea})

def update(request):
	#wea=weather(request)
	print 'request.user:',request.user
	print 'request.method',request.method
	print 'request.POST',request.POST
	name=request.user
	#name=str(name)
	print 'type:',type(name)
	if request.method=='POST':
		form=StockForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/stock/stock_success/')
		else:
			return render(request,'update.html',{'user':request.user,'stock':form})	
	form=StockForm()
	return render(request,'update.html',{'user':request.user,'stock':form})

def list(request):
	wea=weather(request)
	context=[]
	stock=Stock.objects.filter(username=request.user)
	for stk in stock:
		stk_username=str(stk.username)
		request_user=str(request.user)
		context_str=[]
		stk_quote=str(stk.quote)
		context_str.append(stk_quote)
		tick=getQuotes(str(stk_quote))[0]
		ticker=tick["LastTradeWithCurrency"]
		ticker=str(ticker)
		context_str.append(ticker)	
		ticker=float(ticker)
		price=ticker*stk.qty
		price=round(price,2)			
		context_str.append(stk.qty)
		context_str.append(price)
		context.append(context_str)
	return render(request,'list.html',{'full_name':request.user,'context':context,'weather':wea})

def stock_success(request):
	stock=Stock.objects.filter(username=request.user)
	print 'stock',stock
	return render_to_response('stock_success.html',{'user':request.user,'stock':stock})

def delete(request):
	#wea= weather(request)
	stock=Stock.objects.filter(username=request.user)
	page=Stock.objects.filter(username=request.user)
	query=request.GET.get('q')
	if query:
		page=page.get(pk=query)
		page.delete()	
	return render(request,'delete.html',{'full_name':request.user,'stock':stock,'q':page})

def weather(request):
	location=Location.objects.filter(username=request.user)
	if location.count()==0:
		return location
	list_loc=[]
	city=location[0].city
	state=location[0].state
	list_loc.append(city)
	list_loc.append(state)
	f=urllib2.urlopen('http://api.wunderground.com/api/f3c442098e60ca9c/conditions/q/'+state+'/'+city+'.json')
	json_string=f.read()
	parsed_json=json.loads(json_string)
	#print parsed_json
	weather=parsed_json['current_observation']['weather']
	temp=parsed_json['current_observation']['temperature_string']
	humid=parsed_json['current_observation']["relative_humidity"]
	wind=parsed_json['current_observation']["wind_string"]
	wind_mph=parsed_json['current_observation']["wind_mph"]
	image=parsed_json['current_observation']['icon_url']
	image=str(image)
	list_loc.append(image)
	list_loc.append(temp)
	list_loc.append(humid)
	list_loc.append(wind)
	list_loc.append(wind_mph)
	return list_loc
	#return image