from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import pickle
from . get_df import get_aspect_df 
from textblob import TextBlob
import os
import json 
import glob
from .get_graph import get_plotly_plot

# from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ind(request):
    return render(request,"home.html")

def all(request):
	df=pd.read_csv('src/data_frame.csv')
	labels = ['Positive',"Negative","Neutral"]
	color=['green','red','yellow']
	sizes = [df.Positive.values.sum()/(len(df)*100),df.Negative.values.sum()/(len(df)*100),df.Neutral.values.sum()/(len(df)*100)]
	fig = go.Figure(data=[go.Pie(labels=labels, values=sizes ,marker={"colors":color},pull=[0.02, 0.05])])
	fig.update_layout(title =  dict(text ='Over All Sentiments',
	                           font =dict(family='Sherif',
	                           size=25,
	                           color = 'blue'),
	                           y=0.9,
        					   x=0.5,
        					   xanchor= 'center',
        					   yanchor= 'top'))
	div = opy.plot(fig, auto_open=False, output_type='div')
	param={'graph':div}
	return render(request,"all.html",param)


def simple_upload(request):

	
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		# print("url is ",BASE_DIR+uploaded_file_url)
		file_url=BASE_DIR+uploaded_file_url
		feature_count,absa_list,df,male_lis,female_lis,male_count,female_count,emotions_values,emotions_name=get_aspect_df(file_url)
		# print(emotions_name)
		# print('emotion_values',emotions_values)
		aspect_data=pd.read_csv("src/data_frame.csv")
		Positive_data=aspect_data.sort_values(by=['Positive'],ascending=False)["Aspect"].values
		Negative_data=aspect_data.sort_values(by=['Negative'],ascending=False)["Aspect"].values
		Neutral_data=aspect_data.sort_values(by=['Neutral'],ascending=False)["Aspect"].values
		context={}
		color=['green','red','yellow']
		labels = ['Positive',"Negative","Neutral"]
		sizes = [df.Positive.values.sum()/(len(df)*100),df.Negative.values.sum()/(len(df)*100),df.Neutral.values.sum()/(len(df)*100)]
		fig = go.Figure(data=[go.Pie(labels=labels, values=sizes,marker={"colors":color}, pull=[0.02, 0.05])])
		fig.update_layout(title =  dict(text ='Over All Sentiments',
		                           font =dict(family='Sherif',
		                           size=25,
		                           color = 'blue'),
		                           y=0.9,
	        					   x=0.5,
	        					   xanchor= 'center',
	        					   yanchor= 'top'),
									paper_bgcolor = 'rgba(0,0,0,0)',
									plot_bgcolor = 'rgba(0,0,0,0)')
		div = opy.plot(fig, auto_open=False, output_type='div')
		os.remove(file_url)
		param={'graph':div,"Positive_data":Positive_data,"Negative_data":Negative_data,"Neutral_data":Neutral_data,"male_lis":male_lis,"female_lis":female_lis,"male_count":male_count,"female_count":female_count,"emotions_values":emotions_values,"emotions_name":emotions_name}
		
        
	return render(request, 'sentiment.html',param)



def positive(request):
	absa_df=pd.read_csv("src/absa_df.csv")
	aspect_data=pd.read_csv("src/data_frame.csv")
	df1=aspect_data[(aspect_data.Positive>0) & (aspect_data.Positive>0.5)]
	Positive_data=df1.sort_values(by=['Positive'],ascending=False)["Aspect"].values

	length=len(Positive_data)
	if length==1:
		varr=int(1)
	elif length==2:
		varr=int(2)
	elif length==3:
		varr=int(3)
	elif length==4:
		varr=int(4)
	else:
		varr=int(5)

	absa_list = dict()
	for i in list(set(absa_df.name.values)):
	    absa_list[i] = list()
	    for j in list(absa_df.score[absa_df.name==i].values):
	        absa_list[i].append(j)
	sentences_top=[]
	for i in Positive_data[0:varr]:
	    aspect_sentence=" ".join([str(x) for x in absa_list[i]])
	    sentences_top.append(str(aspect_sentence))
	
	final = []
	for n,s in zip(Positive_data[0:varr],sentences_top):
		r = (n,s)
		final.append(r)

	# print(Positive_data)
	param={"final":final,"Positive":Positive_data}
	poas=request.GET.get('poas')
	if poas:
		# print("posa",poas)
		sentences_top1=absa_list[str(poas)]
		param1={"Positive_data":poas,"sentences":sentences_top1,"Positive":Positive_data}
		return render(request, 'positive1.html',param1)
	else:
		return render(request, 'positive.html',param)

def negative(request):
	sentences_top=[]
	absa_df=pd.read_csv("src/absa_df.csv")
	aspect_data=pd.read_csv("src/data_frame.csv")
	df1=aspect_data[(aspect_data.Negative>0) & (aspect_data.Negative>0.5)]
	Negative_data=df1.sort_values(by=['Negative'],ascending=False)["Aspect"].values
	length=len(Negative_data)
	if length==1:
		varr=int(1)
	elif length==2:
		varr=int(2)
	elif length==3:
		varr=int(3)
	elif length==4:
		varr=int(4)
	else:
		varr=int(5)

	absa_list = dict()
	for i in list(set(absa_df.name.values)):
	    absa_list[i] = list()
	    for j in list(absa_df.score[absa_df.name==i].values):
	        absa_list[i].append(j)

	for i in Negative_data[0:varr]:
	    aspect_sentence=" ".join([str(x) for x in absa_list[i]])
	    sentences_top.append(str(aspect_sentence))
	
	final = []
	for n,s in zip(Negative_data[0:varr],sentences_top):
		r = (n,s)
		final.append(r)

	param={"final":final,"Negative":Negative_data}
	neas=request.GET.get('neas')
	if neas:
		sentences_top1=absa_list[str(neas)]
		param1={"Negative_data":neas,"sentences":sentences_top1,"Negative":Negative_data}
		return render(request, 'negative1.html',param1)
	else:
		return render(request, 'negative.html',param)


def neutral(request):
	absa_df=pd.read_csv("src/absa_df.csv")
	aspect_data=pd.read_csv("src/data_frame.csv")
	df1=aspect_data[(aspect_data.Neutral>0) & (aspect_data.Neutral>0.5)]
	Neutral_data=df1.sort_values(by=['Neutral'],ascending=False)["Aspect"].values
	length=len(Neutral_data)
	if length==1:
		varr=int(1)
	elif length==2:
		varr=int(2)
	elif length==3:
		varr=int(3)
	elif length==4:
		varr=int(4)
	else:
		varr=int(5)

	# print(Neutral_data)
	absa_list = dict()
	for i in list(set(absa_df.name.values)):
	    absa_list[i] = list()
	    for j in list(absa_df.score[absa_df.name==i].values):
	        absa_list[i].append(j)
	sentences_top=[]
	for i in Neutral_data[0:varr]:
	    aspect_sentence=" ".join([str(x) for x in absa_list[i]])
	    sentences_top.append(str(aspect_sentence))

	final = []
	for n,s in zip(Neutral_data[0:varr],sentences_top):
		r = (n,s)
		final.append(r)

	# print(final[0])
	param={"final":final,"Neutral":Neutral_data}
	neas=request.GET.get('neas')
	if neas:
		sentences_top1=absa_list[str(neas)]
		param1={"Neutral_data":neas,"sentences":sentences_top1,"Neutral":Neutral_data}
		return render(request,'neutral1.html',param1)
	else:
		return render(request,'neutral.html',param)




def dist(request):

	absa_df=pd.read_csv("src/absa_df.csv")
	aspect_data=pd.read_csv("src/data_frame.csv")
	aspcts=list(aspect_data.Aspect.values)
	aspcts.sort()
	poas1=request.GET.get('poas1')
	poas2=request.GET.get('poas2')
	poas3=request.GET.get('poas3')
	poas4=request.GET.get('poas4')
	poas5=request.GET.get('poas5')
	# print(poas1)

	param={"aspcts":aspcts}
	if poas1:
		name=[poas1,poas2,poas3,poas4,poas5]
		context=get_plotly_plot(aspect_name_list=name)
		context['aspcts']=aspcts
		return render(request,"aspect.html",context)
	else:
		return render(request,"aspect.html",param)
