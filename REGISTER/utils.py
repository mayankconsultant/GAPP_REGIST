import requests

from fuzzywuzzy import fuzz


def gen_otp(len):
    import math, random

    digits = "0123456789"

    OTP = ""

    for i in range(len):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def send_message(msisdn):
    otp = gen_otp(6)
    # print (str(msisdn)[3:])
    # print('OTP:' + str(otp))
    Api = 'http://173.212.218.174:6005/api/v2/SendSMS?SenderId=ZainSS&Is_Unicode=false&Is_Flash=false'
    message = 'To register USE OTP as ' + str(otp)
    Api = Api + '&Message=' + str(message)
    Api = Api + '&MobileNumbers=' + str(msisdn)[3:]
    Api = Api + '&ApiKey=TqEuq9o58233RcYkFIm5w1CS2HB7yJHejc0a3tbMpfg%3D&ClientId=94393ba7-afef-4744-880b-175368936e9b'

    r = requests.get(url=Api)
    # print(Api)
    print('SMS response status code : ' + str(r.status_code))

    return otp


import os

# import pytesseract
# from pytesseract import image_to_string
from PIL import Image, ImageFilter

# def extract_text(filepath, id_num, first_name, last_name):
#     img_grey = Image.open(filepath)
#     img_grey = img_grey.convert('L')
#     img_grey.save('media\ALL\grey_' + os.path.basename(filepath))
#     img_grey = Image.open('media\ALL\grey_' + os.path.basename(filepath))
#     blurImage = img_grey.filter(ImageFilter.DETAIL)
#     os.remove('media\ALL\grey_' + os.path.basename(filepath))
#     blurImage.save(r'media\ALL\blur_' + os.path.basename(filepath))
#     config = ('-l eng --oem 1 --psm 3')
#
#     try:
#         pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#         k = pytesseract.image_to_string(Image.open(r'media\ALL\blur_' + os.path.basename(filepath)), config=config)
#     except Exception as e:
#         import cv2
#         print('IN EXCEPTION CV2')
#         # im = cv2.imread('./test3.jpg')
#         k = pytesseract.image_to_string(cv2.imread(r'media\ALL\blur_' + os.path.basename(filepath)), config=config)
#
#
#
#
#     # config = (' -l eng')
#
#     # print (image_to_string(Image.open(filepath),lang='eng'))
#
#
#     os.remove(r'media\ALL\blur_' + os.path.basename(filepath))
#     points = 0
#     if id_num in k :points +=1
#     if first_name in k: points += 1
#     if last_name in k: points += 1
#     # print(k)
#     # print( data in k)
#     # print(k)
#     # print(data in k)
#     # k= k.split('\n')
#     # for j in k:
#     #     print( str(j) + ' Matched with ' + str(k))
#     #     print(j in str(k))
#     if points >=2 :
#         return True
#     else :
#         return False


from PIL import Image
from django.core.files.storage import FileSystemStorage, default_storage


def detect_text(file_path, id, first_name, last_name):
    """Detects text in the file."""
    from google.cloud import vision
    from django.conf import settings
    import io
    client_options = {'api_endpoint': 'eu-vision.googleapis.com', 'languageHints': ["en-t-i0-handwrit"]}

    client = vision.ImageAnnotatorClient()
    # cl = vision.ImageAnnotatorClient().from_service_account_json('')

    # credential_path = os.path.join( settings.BASE_DIR,'mykeys.json')
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path #settings.GS_CREDENTIALS

    tmp = default_storage.open('tmp_' + file_path)

    # with open(tmp, 'rb') as image_file:
    #     content = image_file.read()
    # img = file_path
    # buffer = io.BytesIO()
    # img.save(buffer,'JPEG')
    # content = buffer.getvalue()
    content = tmp.read()

    image = vision.Image(content=content)
    # image = vision.Image()
    # image.source.image_uri =  tmp
    # image.source.image_uri = bytes(file_path)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print(id, first_name, last_name)
    print('Texts:')

    points = 0
    first_name_f, last_name_f, id_f = False, False, False
    for i, text in enumerate(texts):
        if i == 0:
            print(text.description)
            # pass
        if i > 0:
            # print (str(i) +" --> " +  str(text.description).strip('\n') )
            if len(id) <= len(str(text.description).strip('\n').strip('<')):
                ratio = fuzz.partial_ratio(id, str(text.description).strip('\n').strip('<').replace('0', 'O'))
                if ratio >= 55:
                    print(str(text.description).strip('\n').strip('<') + ' -ID ratio ' + str(ratio))
                # if id == str(text.description).strip('\n').strip('<'):
                if ratio >= 89:
                    points = points + 1
                    print(str(id) + ' Matched with ' + str(text.description).strip('\n').replace('0', 'O'))
                    id_f = True
            # print(str(text.description).strip('\n').strip('<').strip().upper())
            if str(first_name).upper() == str(text.description).strip('\n').strip('<').strip().upper():
                points = points + 1
                print(str(first_name) + ' Matched with ' + str(text.description).strip('\n'))
                first_name_f = True
            if str(last_name).upper() == str(text.description).strip('\n').strip('<').strip().upper():
                points = points + 1
                print(str(last_name) + ' Matched with ' + str(text.description).strip('\n').upper())
                last_name_f = True

    # print('Points ' + str(points))
    # if (points >= 3):
    #     # print( 'Points ' + str(points) )
    #     default_storage.delete('tmp_' + file_path)
    #     return points,first_name_f,last_name_f,id_f
    # else:
    default_storage.delete('tmp_' + file_path)
    return points, first_name_f, last_name_f, id_f


# new

from django.core.files import File
from pathlib import Path
from PIL import Image
from io import BytesIO

image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
    "JPG": "JPEG",
    "PNG": "PNG",
}


def image_resize(image, width, height):
    # Open the image using Pillow
    img = Image.open(image)

    # check if either the width or height is greater than the max
    if img.width > width or img.height > height:
        if img.width <= width: width = img.width
        if img.height <= height: height = img.height
        output_size = (width, height)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
        # Find the file name of the image
        img_filename = Path(image.file.name).name
        # Spilt the filename on “.” to get the file extension only
        img_suffix = Path(image.file.name).name.split(".")[-1]
        # Use the file extension to determine the file type from the image_types dictionary
        img_format = image_types[img_suffix]
        # Save the resized image into the buffer, noting the correct file type
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        # Save the new resized file as usual, which will save to S3 using django-storages
        image.save(img_filename, file_object)
