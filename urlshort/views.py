import random
import string
from random import randint


from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.core.mail import send_mail
from django.shortcuts import render

# Create your views her
def home(request):
    return render(request, "Home.html")

#API
def generateshorturlapi(request):
    letter = string.ascii_letters + string.digits
    shorturl = ''
    for i in range(6):
        shorturl = shorturl + ''.join(random.choice(letter))
    return JsonResponse({"shorturl": shorturl, "response": "success"})


def generateshorturl():
    letter=string.ascii_letters + string.digits
    shorturl=''
    for i in range(6):
        shorturl=shorturl+''.join(random.choice(letter))
    return shorturl


def urlshortner(request):
    longlink= request.GET['link']
    customurl = request.GET['customurl']
    if customurl is None or customurl=="":
        shorturl=''
    else:
        cursor = connection.cursor()
        query1 = "select * from links where short_link='" + customurl + "'"
        cursor.execute(query1)
        data = cursor.fetchone()
        if data is not None:
            data = {"link": " Already custom Url exist please try some other url"}
            return render(request, "first.html", data)
        else:
            query = "insert into links (long_link, short_link) values (%s,%s)"
            value = (longlink,customurl)
            cursor.execute(query, value)
            data = {"link": "Url shortened with nano.co/"+customurl}
            return render(request, "first.html", data)
    if shorturl is  None or shorturl =='':
      while True:
        shorturl = generateshorturl()
        cursor = connection.cursor()
        query2= "select * from links where short_link='" + shorturl + "'"
        cursor.execute(query2)
        data = cursor.fetchone()
        if data is not None:
            break
        else:
            query = "insert into links (long_link, short_link) values (%s,%s)"
            value = (longlink,shorturl)
            cursor.execute(query, value)
            data = {"link":"Url shortened with nano.co/"+shorturl}
            return render(request, "first.html", data)

def handlingshorturl(request, **kwargs):
    cursor = connection.cursor()
    url= kwargs.get('url')
    query = "select long_link from links where short_link='" + url + "'"
    cursor.execute(query)
    data= cursor.fetchone()
    print(data)
    if data is None:
        return render(request,"Home.html")
    else:
        return redirect(data[0])


