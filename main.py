# import os
# import sys


# sys.path.insert(0, os.path.dirname(__file__))


# def app(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'It works!\n'
#     version = 'Python v' + sys.version.split()[0] + '\n'
#     response = '\n'.join([message, version])
#     return [response.encode()]

import pymysql
from flask import Flask,request,jsonify
from werkzeug.utils import secure_filename
import re
import datetime
from datetime import datetime
import mysql.connector
import json
import os , io , sys
import base64
from io import BytesIO
from PIL import Image
from os.path import expanduser
import paramiko

import pytesseract
from sshtunnel import SSHTunnelForwarder
sql_hostname = 'localhost'
sql_username = 'uoka9vojujcjk'
sql_password = 'admin1234!@#$'
sql_main_database = 'dbhqpazymifxx6'
sql_port = 3306
ssh_host = 'monte-bianco.in'
ssh_user = 'u30-3zfmzf4bsowc'
ssh_port = 18765
# sql_ip = '1.1.1.1.1'
# mypkey = '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'
home = expanduser('~')
privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
mypkey = paramiko.RSAKey.from_private_key_file(home + '/Documents/docsender_key.ppk',password=';p@f2&42*^@$')



with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = mysql.connector.connect(host='localhost', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)
    cursor = conn.cursor()

    cursor.execute('set max_allowed_packet=67108864')

# with SSHTunnelForwarder(('dbhqpazymifxx6', 18765),
#                   ssh_password=";p@f2&42*^@$",
#                   ssh_username="u30-3zfmzf4bsowc",
#                   remote_bind_address=('localhost',  18765)) as server:
#                     conn = mysql.connector.connect(
#                             host='monte-bianco.in',
#                             port=' 18765',
#                             user='uoka9vojujcjk',
#                             password='admin1234!@#$',
#                             database='dbhqpazymifxx6')



# import numpy as np
# from numpy import ndarray
# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
# pytesseract.pytesseract.tesseract_cmd = '/home/thebugsb/virtualenv/restapi/3.8/lib/python3.8/site-packages/tesseract'
#!/usr/bin/env python

    # We usually use madvise hugepages support, but on some old kernels it
    # is slow and thus better avoided.
    # Specifically kernel version 4.6 had a bug fix which probably fixed this:
    # https://github.com/torvalds/linux/commit/7cf91a98e607c2f935dbcc177d70011e95b8faff



# try:
#     from PIL import Image
# except ImportError:
#     import Image

# pytesseract.pytesseract.tesseract_cmd= r"home/thebugsb/virtualenv/restapi/3.8/lib/python3.8/site-packages/pytesseract/tesseract.exe"
# Flask constructor takes the name of 
# current module (__name__) as argument.
def date_finder(text_input):
    dates=[]
    reg1=re.compile(r'(?<!\S)[0-3]{1}[0-9]{1}[/][0-9]{2}[/][0-9]{4}')
    res1=reg1.findall(text_input)
    for i in res1:
        d1 = datetime.strptime(i,'%d/%m/%Y').strftime('%Y-%m-%d')
        dates.append(d1)
    reg2=re.compile(r'(?<!\S)[0-3]{1}[0-9]{1}[-][0-9]{2}[-][0-9]{4}')
    res2=reg2.findall(text_input)
    for i in res2:
        d2= datetime.strptime(i,'%d-%m-%Y').strftime('%Y-%m-%d')
        dates.append(d2)
    reg3=re.compile(r'(?<!\S)[0-9]{4}[/][0-9]{2}[/][0-9]{2}')
    res3=reg3.findall(text_input)
    for i in res3:
        d3= datetime.strptime(i,'%Y/%m/%d').strftime('%Y-%m-%d')
        dates.append(d3)
    reg4=re.compile(r'(?<!\S)[0-9]{4}[-][0-9]{2}[-][0-9]{2}')
    res4=reg4.findall(text_input)
    for i in res4:
        d4= datetime.strptime(i,'%Y-%m-%d').strftime('%Y-%m-%d')
        dates.append(d4)
    reg5=re.compile(r'(?<!\S)[0-9]{4}[.][0-9]{2}[.][0-9]{2}')
    res5=reg5.findall(text_input)
    for i in res5:
        d5= datetime.strptime(i,'%Y.%m.%d').strftime('%Y-%m-%d')
        dates.append(d5)
    reg6=re.compile(r'(?<!\S)[0-9]{2}[.][0-9]{2}[.][0-9]{4}')
    res6=reg6.findall(text_input)
    for i in res6:
        d6= datetime.strptime(i,'%d.%m.%Y').strftime('%Y-%m-%d')
        dates.append(d6)
    return dates
    
    
def amount_finder(text_input):
    amounts=[]
    reg1=re.compile('[1-9]{1}[0-9]{1,12}[.][0-9]{1,2}')
    res1=reg1.findall(text_input)
    for i in res1:
        amounts.append(i)
    reg2=re.compile('[1-9][,][0-9]{1,3}')
    res2=reg2.findall(text_input)
    for i in res2:
        num1=re.sub(',','',i)
        amounts.append(num1)
    reg3=re.compile('[1-9][0-9][,][0-9]{2,5}')
    res3=reg3.findall(text_input)
    for i in res3:
        num2=re.sub(',','',i)
        amounts.append(num2)
    reg4=re.compile('[1-9][,][0-9]{2}[,][0-9]{2,5}')
    res4=reg4.findall(text_input)
    for i in res4:
        num3=re.sub(',','',i)
        amounts.append(num3)
    reg5=re.compile('[1-9][0-9][,][0-9]{2}[,][0-9]{2,5}')
    res5=reg5.findall(text_input)
    for i in res5:
        num4=re.sub(',','',i)
        amounts.append(num4)
    reg6=re.compile('[1-9][,][0-9]{2}[,][0-9]{2}[,][0-9]{2,5}')
    res6=reg6.findall(text_input)
    for i in res6:
        num5=re.sub(',','',i)
        amounts.append(num5)
    reg7=re.compile('[1-9][0-9][,][0-9]{2}[,][0-9]{2}[,][0-9]{2,5}')
    res7=reg7.findall(text_input)
    for i in res7:
        num6=re.sub(',','',i)
        amounts.append(num6)
    reg8=re.compile('[1-9][,][0-9]{1,3}[.][0-9]{1,2}')
    res8=reg8.findall(text_input)
    for i in res8:
        num7=re.sub(',','',i)
        amounts.append(num7)
    reg9=re.compile('[1-9][0-9][,][0-9]{2,5}[.][0-9]{1,2}')
    res9=reg9.findall(text_input)
    for i in res9:
        num8=re.sub(',','',i)
        amounts.append(num8)
    reg10=re.compile('[1-9][,][0-9]{2}[,][0-9]{2,5}[.][0-9]{1,2}')
    res10=reg10.findall(text_input)
    for i in res10:
        num9=re.sub(',','',i)
        amounts.append(num9)
    reg11=re.compile('[1-9][0-9][,][0-9]{2}[,][0-9]{2,5}[.][0-9]{1,2}')
    res11=reg11.findall(text_input)
    for i in res11:
        num11=re.sub(',','',i)
        amounts.append(num11)
    reg12=re.compile('[1-9][,][0-9]{2}[,][0-9]{2}[,][0-9]{2,5}[.][0-9]{1,2}')
    res12=reg12.findall(text_input)
    for i in res12:
        num12=re.sub(',','',i)
        amounts.append(num12)
    reg13=re.compile('[1-9][0-9][,][0-9]{2}[,][0-9]{2}[,][0-9]{2,5}[.][0-9]{1,2}')
    res13=reg13.findall(text_input)
    for i in res13:
        num13=re.sub(',','',i)
        amounts.append(num13)
    amounts=[float(i) for i in amounts]
    if len(amounts)>0:
        final_amount=max(amounts)
    else:
        final_amount=None
    return final_amount

def invoice_finder(text_input):
    invoice_num=[]
    reg1=re.compile('(?<!\S)[0-9]{5,6}[-][0-9]{3,5}')
    res1=reg1.findall(text_input)
    for i in res1:
        invoice_num.append(i)
    reg2=re.compile('(?<!\S)[0-9]{4}[/][A-Za-z]{2,3}[/][0-9]{3,5}')
    res2=reg2.findall(text_input)
    for i in res2:
        invoice_num.append(i)
    reg4=re.compile('(?<!\S)[0-9]{4}[/|-][0-9]{4}')
    res4=reg4.findall(text_input)
    for i in res4:
        invoice_num.append(i)
    reg6=re.compile('(?<!\S)[#][A-Za-z]{3,4}[-|/][0-9]{3,4}')
    res6=reg6.findall(text_input)
    for i in res6:
        invoice_num.append(i)
    reg7=re.compile('(?<!\S)[0-9]{2,3}[-][0-9]{5,6}')
    res7=reg7.findall(text_input)
    for i in res7:
        invoice_num.append(i)
    reg8=re.compile('(?<!\S)[#][0-9]{2,5}(?=\s|$)')
    res8=reg8.findall(text_input)
    for i in res8:
        invoice_num.append(i)
    reg11=re.compile('(?<!\S)[A-Za-z]{2,3}[0-9]{12,14}')
    res11=reg11.findall(text_input)
    for i in res11:
        invoice_num.append(i)
    return invoice_num

def contact_finder(text_input):
    contact_no=[]
    reg1=re.compile('[7-9][0-9]{9}')
    res1=reg1.findall(text_input)
    for i in res1:
        contact_no.append(i)
    reg2=re.compile('[+][9][1][6-9][0-9]{9}')
    res2=reg2.findall(text_input)
    for i in res2:
        contact_no.append(i)
    reg3=re.compile('(?<!\S)[0-9]{3,4}[\s][0-9]{3,4}[\s][0-9]{3,4}')
    res3=reg3.findall(text_input)
    for i in res3:
        contact_no.append(i)
    return contact_no

def email_finder(text_input):
    emails=[]
    reg1 = re.compile(r'[a-zA-Z0-9|.|_]{2,20}@[a-zA-Z]{2,20}.[a-zA-Z|.]{2,20}')
    res1 = reg1.findall(text_input)
    for i in res1:
        emails.append(i)
    return emails

def name_finder(text_input):
    name1 = re.compile(r'([A-Z]{3,10}[\s][A-Z]{3,15})+')
    name=name1.findall(text_input)
    if len(name)>0:
        name=name[0]
    else:
        name=None
    return name

def gst_finder(text_input):
    gst_number=[]
    regex=re.compile(r'[0-9A-Z]{10}[0-9A-Za-z]{3}[Z][0-9A-Za-z]{1}')
    gst_no = regex.findall(text_input)
    for i in gst_no:
        gst_number.append(i)
    return gst_number
    
def ocr_core(filename):
        text =pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
        return text

def text_to_info(text):

        gst_no = gst_finder(text)
        if len(gst_no)>0:
            gst_no=gst_no[0]
        else:
            gst_no=None
        final_amount = amount_finder(text)
        contact_no = contact_finder(text)
        if len(contact_no)>0:
            contact_no=contact_no[0]
        else:
            contact_no=None
        email_id = email_finder(text)
        if len(email_id)>0:
            email=email_id[0]
        else:
            email=None
        date=date_finder(text)
        if len(date)>0:
            result=date[0]
        else:
            result=None
        invoice_no=invoice_finder(text)
        if len(invoice_no)>0:
            invoice_no=invoice_no[0]
        else:
            invoice_no=None
        name=name_finder(text)
        info_get = []
        info_get.extend([gst_no,final_amount,contact_no,email,result,invoice_no,name])
        return info_get
        
def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = '/home/python/Downloads/restful_api/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','pdf','txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='/home/python/Downloads/restful_api/uploads'
  
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'
    
@app.route('/upload',methods=['POST'])
def upload():
    document_type=request.form.get('document_type')
    if str(document_type)=='Sales':
        user_id = request.form.get('user_id')
        file1 = request.form.get('file')
        file2 = request.form.get('file')
        file3 = request.form.get('file')
        file4 = request.form.get('file')
        if file2=='':
            pass
        if file3=='':
            pass
        if file4=='':
            pass
        select_date=request.form.get('date')
        Invoice_No=request.form.get('invoice_no')
        Invoice_Value=request.form.get('invoice_value')
        Credit_No=None
        Credit_Value=None
        Debit_No=None
        Debit_Value=None
        Note=request.form.get('notes')
        if Note=='':
            pass
    elif str(document_type)=='Purchase':
        user_id = request.form.get('user_id')
        file1 = request.form.get('file')
        file2 = request.form.get('file')
        file3 = request.form.get('file')
        file4 = request.form.get('file')
        if file2 == '':
            pass
        if file3 == '':
            pass
        if file4 == '':
            pass
        select_date=request.form.get('date')
        Invoice_No=request.form.get('invoice_no')
        Invoice_Value=request.form.get('invoice_value')
        Credit_No=None
        Credit_Value=None
        Debit_No=None
        Debit_Value=None
        Note=request.form.get('notes')
        if Note=='':
            pass
    elif str(document_type)=='Credit':
        user_id = request.form.get('user_id')
        file1 = request.form.get('file')
        file2 = request.form.get('file')
        file3 = request.form.get('file')
        file4 = request.form.get('file')
        if file2 == '':
            pass
        if file3 == '':
            pass
        if file4 == '':
            pass
        select_date=request.form.get('date')
        Credit_No=request.form.get('credit_no')
        Credit_Value=request.form.get('credit_value')
        Invoice_No=None
        Invoice_Value=None
        Debit_No=None
        Debit_Value=None
        Note=request.form.get('notes')
        if Note=='':
            pass
    elif str(document_type)=='Debit':
        user_id = request.form.get('user_id')
        file1 = request.form.get('file')
        file2 = request.form.get('file')
        file3 = request.form.get('file')
        file4 = request.form.get('file')
        if file2 == '':
            pass
        if file3 == '':
            pass
        if file4 == '':
            pass
        select_date=request.form.get('date')
        Debit_No=request.form.get('debit_no')
        Debit_Value=request.form.get('debit_value')
        Invoice_No=None
        Invoice_Value=None
        Credit_No=None
        Credit_Value=None
        Note=request.form.get('notes')
        if Note=='':
            pass
    else:
        user_id = request.form.get('user_id')
        file1 = request.form.get('file')
        file2 = request.form.get('file')
        file3 = request.form.get('file')
        file4 = request.form.get('file')
        if file2 == '':
            pass
        if file3 == '':
            pass
        if file4 == '':
            pass
        select_date=request.form.get('date')
        # select_date=request.form.get('Select Date')
        # Invoice_No=request.form.get('Invoice No')
        # Invoice_Value=request.form.get('Invoice Value')
        Invoice_No=None
        Invoice_Value=None
        Credit_No=None
        Credit_Value=None
        Debit_No=None
        Debit_Value=None
        Note=request.form.get('notes')
        if Note=='':
            pass
    
    file1= BytesIO(base64.b64decode(file))
    now=datetime.now()
    ext='.jpeg'
    filename = secure_filename(str(now)+ext)
    saved_path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_converted=base64.b64decode(file)
    image=Image.open(io.BytesIO(file_converted))
    # image.save(saved_path)


#     # call the OCR function on it
    extracted_text = ocr_core(file1)
    ms=text_to_info(text=extracted_text)
    gst=ms[0]
    amnt=ms[1]
    no=ms[2]
    email=ms[3]
    date=ms[4]
    invoice_no=ms[5]
    name=ms[6]

    dic1={"user_id":user_id,"gst_no":gst,"Total_amnt":amnt,"Contact_no":no,"email_id":email,"date":date,"invoice_number":invoice_no,"name":name,"Status":1}
    json_file=json.dumps(dic1)
    json_file = json.loads(json_file.replace("\'", '"'))
    # from sshtunnel import SSHTunnelForwarder
#     # with SSHTunnelForwarder(
#     #              ('DocSender123.mysql.pythonanywhere-services.com', 3306),
#     #              ssh_password="sshPass",
#     #              ssh_username="sshUser",
#     #              remote_bind_address=('localhost', 3306)) as server:
#     # conn = mysql.connector.connect(
#     #         host='localhost',
#     #         port='3306',
#     #         user='uoka9vojujcjk',
#     #         password='admin1234!@#$',
#     #         database='dbhqpazymifxx6')
#     conn = mysql.connector.connect(
#             host='DocSender123.mysql.pythonanywhere-services.com',
#             port='3306',
#             user='DocSender123',
#             password='Saubhagyam@321',
#             database='DocSender123$newdb')
#     cursor = conn.cursor()
#     # cursor.execute("INSERT INTO Doc_Sender(gst_number,final_amount,mobile_number,email_id,date) VALUES ('a','b','c','d','21/02/12');")
#     sql1 = "INSERT INTO Doc_Sender(user_id,file_name,file_path,gst_number,final_amount,mobile_no,email_id,date,invoice_number,name,Doc_Type,Inv_No,Inv_Val,Cred_No,Cred_Val,Deb_No,Deb_Val,Select_Date,Notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#     val1= (user_id,filename,saved_path,gst,amnt,no,email,date,invoice_no,name,document_type,Invoice_No,Invoice_Value,Credit_No,Credit_Value,Debit_No,Debit_Value,select_date,Note)
#     cursor.execute(sql1, val1)
#     # cursor.fetchall()
#     conn.commit()
    return json_file
# conn = mysql.connector.connect(
#             host='localhost',
#               port='3306',
#               user='uoka9vojujcjk',
#               password='admin1234!@#$',
#               database='dbhqpazymifxx6')
  
# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
