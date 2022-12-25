from __future__ import print_function
from flask import Flask,render_template,request,redirect
import requests,json
from flask import Flask, render_template
from PIL import Image
import base64 
import io
import os
import smtplib, ssl
from pywhatkit import sendwhatmsg_instantly
import base64
from email.message import EmailMessage
global whatsapikey,emails
emails=""
whatsapikey=["1a0f4574f7msheb91b4ee0e4aa41p1eaf03jsnd9edd282ec36","85f05638bbmsh499b476a150a468p1b27ccjsna7602a6d42",
"6da8a2c4c2mshedcbe0786cec706p1c6e9djsnd5f7b198057f","6cb72c20d6msh928241c3c28fad0p136dd7jsn4d6fdc8e97ea"]
app=Flask(__name__)
import socket
socket.getaddrinfo('localhost', 8080)
pic=os.path.join('static','pics')
app.config['UPLOAD_FOLDER']=pic
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\user\\Desktop\\dirc.json"
@app.route('/',methods = ['GET','POST'])

def dropdown():
    pic1=os.path.join(app.config['UPLOAD_FOLDER'],'ir.jpg')
    return render_template('dropdown.html',ui=pic1)


@app.route("/pnrnumber",methods = ['GET','POST'])
def function():
    global whatsapikey
    global emails
    pnrnumber = request.form['pnr']
    mobilenumber = request.form['mobilenumber']
    email=request.form['email']
    emails=email
    url = str("https://pnr-status-indian-railway.p.rapidapi.com/pnr-check/"+str(pnrnumber))
    flag=True
    xno=0
    print(whatsapikey[0])

    while flag==True:
        headers = {"X-RapidAPI-Key": whatsapikey[xno],
        "X-RapidAPI-Host": "pnr-status-indian-railway.p.rapidapi.com"}
        try:
            response=requests.request("GET", url, headers=headers)
            flag=False
        except:
            print("invalid")    
        xno=xno+1
        if xno>=len(whatsapikey):
            flag=False

    pic1=os.path.join(app.config['UPLOAD_FOLDER'],'ir.jpg')
    response_json=response.json()
    x=dict(response_json)
    message="Your booking details are as follows : \n"+str(pnrnumber)+"  "
    message+=str(x["data"]["trainInfo"]["trainNo"])+"\n"
    message+=str(x["data"]["trainInfo"]["name"])+"\n"
    message+=str(x["data"]["boardingInfo"]["stationName"])+"\n"
    message+=str(x["data"]["destinationInfo"]["stationName"])+"\n"
    message+="Arrival & Departure Time " + str(x["data"]["boardingInfo"]["arrivalTime"])+":"+str(x["data"]["boardingInfo"]["departureTime"])+"\n"
    message+="Destination arrival time " + str(x["data"]["destinationInfo"]["arrivalTime"])+"\n"
    message+="Platform Number " + str(x["data"]["boardingInfo"]["platform"])+"\n"
    message+=" No Of Seats and Seat Info : " + str(x["data"]["seatInfo"]["noOfSeats"]) +" & " + str(x["data"]["seatInfo"]["coach"])+" "+str(x["data"]["seatInfo"]["berth"])+"\n"
    sendwhatmsg_instantly("+91"+str(mobilenumber),message,20,60)
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
    
    payload = {"personalizations": [{"to": [{"email": emails }],"subject": "Ticket Confirmation"}
        ],
        "from": {"email": "ashutosh17141@iiitd.ac.in"},
        "content": [
            {
                "type": "text/plain",
                "value": message
            }
        ]
    }
    headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "1a0f4574f7msheb91b4ee0e4aa41p1eaf03jsnd9edd282ec36",
    "X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return render_template('temp.html',response_json=response_json,pnrnumber=pnrnumber,ui=pic1,mn=mobilenumber)

if __name__ == "__main__":
    app.run(debug=True ,port=8080,use_reloader=False)
