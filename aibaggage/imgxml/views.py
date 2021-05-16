from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
from django.core.files.storage import FileSystemStorage
import requests
import urllib.request
import cv2
import csv  
import numpy as np
from . models import NewBaggages
from datetime import datetime
from datetime import date
# Create your views here.
def home(request):
    return render(request,"home.html")
def files(request):
    urli = ""
    urlx = ""
    if request.method=='POST':
        upfilei = request.FILES['file1']
        upfilex = request.FILES['file2']
        fs = FileSystemStorage()
        fs1 = FileSystemStorage()
        name1 = fs.save(upfilei.name,upfilei)
        name2 = fs.save(upfilex.name,upfilex)
        urli = fs.url(name1)
        urlx = fs.url(name2)
        xmlfilex = requests.get("http://127.0.0.1:8000"+urlx)
        xmlfilei = requests.get("http://127.0.0.1:8000"+urli)
        tree = et.parse(urlx[1:])
        root = tree.getroot()
        names=[]
        for i in root.findall('object'):
            item = i.find('name').text
            names.append(item)
        xmin=[]
        ymin=[]
        xmax=[]
        ymax=[]
        for i in root.iter('bndbox'):
            item1 = i.find('xmin').text
            item2 = i.find('ymin').text
            item3 = i.find('xmax').text
            item4 = i.find('ymax').text
            xmin.append(int(item1))
            ymin.append(int(item2))
            xmax.append(int(item3))
            ymax.append(int(item4))
        print(xmin,"ok")
        print(ymin)
        print(xmax)
        print(ymax)
        img = cv2.imread(urli[1:])
        for i in range(len(xmax)):
            img = cv2.rectangle(img, (xmin[i], ymin[i]), (xmax[i], ymax[i]), (0, 255, 0),4)
        for i in range(len(names)):
            cv2.putText(img,names[i],(xmin[i],ymin[i]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),4, cv2.LINE_AA)
        cv2.imwrite("media/superhappy.jpg",img)
        now = datetime.now()
        
        today = date.today()
        for i in range(len(names)):
            b = NewBaggages(time=now,startdate=today,enddate=today,imgname=urli,objname=names[i],xmaxi=xmax[i],ymaxi=ymax[i],xmini=xmin[i],ymini=ymin[i])
            b.save()
    details = NewBaggages.objects.all()
    return render(request,"out.html",{"details":details})
def dates(request):
    return render(request,"dates.html")
def report(request):
    start = request.POST.get('start')
    end = request.POST.get('end')
    # ctd = datetime.strptime(start, '%Y-%m-%d')
    # ctd = ctd.date()
    searchresult = NewBaggages.objects.raw('select * from public.imgxml_newbaggages where startdate in (%s,%s)',[start,end])
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="media/file.csv"'  
    writer = csv.writer(response)  
    for i in searchresult:
        writer.writerow([i.objname,i.imgname, i.xmini,i.ymini,i.xmaxi,i.ymaxi,i.time])
    return response
    