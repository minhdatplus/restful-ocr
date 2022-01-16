import os
import shutil

from PIL import Image, ImageDraw, ImageFont
from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import easyocr
import requests

app = Flask(__name__, static_url_path='/static')
api = Api(app)


def download_image(url, file_name):
    full_path = app.root_path + '/' + file_name
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ', full_path)
    else:
        print('Image Couldn\'t be retrieved')
    return app.root_path, file_name


def detect_captcha(url):
    reader = easyocr.Reader(['en', 'en'])
    result = reader.readtext(url)
    return result[0][1]


def convert_gif_to_png(url, file_name):
    print('gif ', url)
    image_name = "captcha.png"
    gif_path = url + '/' + file_name
    convert_path = os.path.join(url, image_name)
    img = Image.open(gif_path)
    img.save(convert_path, 'png', optimize=True, quality=70)
    return convert_path


class OCR(Resource):
    def post(self):
        dict_data = request.json
        json_data = dict_data['data']
        imageURL = json_data['image_url']
        imageType = json_data['image_type']
        print(json_data)
        print(imageURL)
        print(imageType)
        try:
            if imageType != 'gif':
                response_number = detect_captcha(imageURL)
                return {
                    "code": response_number
                }
            else:
                full_path, file_name = download_image(imageURL, 'image.gif')
                print(full_path)
                convert_image_path = convert_gif_to_png(full_path, file_name)
                print('convert ', convert_image_path)
                response_number = detect_captcha(convert_image_path)
                return {
                    "code": response_number
                }
        except ValueError:
            return {
                "code": "error"
            }


api.add_resource(OCR, '/ocr')

if __name__ == '__main__':
    app.run()
