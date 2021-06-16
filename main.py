import os
from flask import Flask,render_template,request,jsonify
import re
from werkzeug.utils import secure_filename
import mysql.connector
import datetime
import pandas as pd
import numpy as np
import jsonify 
import json

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

conn = mysql.connector.connect(
                host='127.0.0.1',
                # host = '192.168.1.200',
                port='8080',
                # port = '80',
                user='root',
                password='',
                database='docsender',
                charset='utf8')
# print(ocr_core('images/ocr_example_1.png'))
def text_to_info(text):

    data=text
    regex=re.compile(r'[0-9A-Z]{10}[0-9A-Za-z]{5}')
    gst_no = regex.findall(data)
    gst_no=gst_no[0]
    Total_Amount = re.compile(r'[0-9|,]{1,12}[.|][0-9]{2}')
    final_amount = Total_Amount.findall(data)
    final_amount = [i for i in final_amount]
    if final_amount=='[]':
        final_amnt=final_amount
    else:
        final_amnt=max(final_amount)
    contact_no = re.compile(r'[0-9]{3}[-|][0-9]{6,10}')
    contact_no = contact_no.findall(data)
    if len(contact_no)>0:
        contact_no=contact_no
    else:
        contact_no=None
    email_id = re.compile(r'[a-zA-Z0-9|.]{2,20}@[a-zA-Z]{2,5}.[a-zA-Z]{2,3}')
    email = email_id.findall(data)
    if len(email)>0:
        email=email
    else:
        email=None
    date=re.compile(r'[0-9]{2}[-|/]{1}[0-9]{2}[-|/]{1}[0-9]{4}')
    date=date.findall(data)
    if len(date)>0:
        result=str(date[0])
        result=datetime.datetime.strptime(result, "%d/%m/%Y").strftime("%Y-%m-%d")

    else:
        result=None

    # z=str(z)
    gst_no= re.sub(r"[\[]", "", str(gst_no))
    gst_no = re.sub(r"[\]]", "", str(gst_no))
    gst_no = re.sub(r"'", "", str(gst_no))

    # gst_no = re.sub(r"'", "", str(gst_no))

    final_amount=final_amnt
    contact_no=str(contact_no)
    email=str(email)
    email= re.sub(r"[\[]", "", str(email))
    email = re.sub(r"[\]]", "", str(email))
    email = re.sub(r"'", "", str(email))
    info_get = []
    info_get.extend([gst_no,final_amount,contact_no,email,result])

    return info_get


UPLOAD_FOLDER = '/home/parth/Documents/ocr_img/uploads'
#
# # allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','pdf','txt'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER']='/home/parth/Documents/ocr_img/uploads/'
# app.config["UPLOAD_FOLDER"]='/192.168.1.200/xampp/htdocs/docsender/public/document_file'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return "hello world"
# #
# # @app.route('/upload')
@app.route('/upload', methods=['POST'])
def upload_page():
    # user_id = request.args.get('user_id')
    user_id = request.form.get('user_id')
    # if request.method == 'POST':
    if 'file' not in request.files:
        return ('upload.html')
    file = request.files['file']
#         # if no file is selected
    if file.filename == '':
        return ('upload.html')
    # if request.method == 'POST':
#         # check if there is a file in the request
    if file and allowed_file(file.filename):
        # user_id = request.args.get('user_id')
        filename = secure_filename(file.filename)
        saved_path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(saved_path)
        
        # call the OCR function on it
        extracted_text = ocr_core(file)
        ms=text_to_info(text=extracted_text)
        get_data = []
        gst=ms[0]
        amnt=ms[1]
        no=ms[2]
        email=ms[3]
        date=ms[4]
        # user_id = 5
        # user_id = request.args.get("user_id", type=int)

        dic1={"user_id":user_id,"gst_no":gst,"Total_amnt":amnt,"Contact_no":no,"email_id":email,"date":date}
        json_file=json.dumps(dic1)
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO doc_sender(gst_number,final_amount,mobile_number,email_id,date) VALUES ('a','b','c','d','21/02/12');")
        sql1 = "INSERT INTO doc_sender(user_id,file_name,file_path,gst_number,final_amount,mobile_no,email_id,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val1= (user_id,filename,saved_path,gst,amnt,no,email,date)
        cursor.execute(sql1, val1)
        data=cursor.fetchall()
        
        conn.commit()
        return json_file
#             # extract the text and display it
        return render_template('upload.html',
                                msg='Successfully processed',
                                extracted_text=ms,
                                img_src=UPLOAD_FOLDER + file.filename)
@app.route('/api/foo/', methods=['GET'])
def foo():
    user_id = request.args['user_id']
    bar = request.args.to_dict()
    print(user_id)
    return 'success', 200

if __name__ == '__main__':
    app.run(debug=True)
# text_to_info("21/03/1887")
