import os
import shutil

from PIL import Image, ImageDraw, ImageFont
from flask import Flask
from flask_restful import Resource, Api, reqparse
import easyocr
import requests

app = Flask(__name__, static_url_path='/static')
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('image_url')
parser.add_argument('download')


def download_image(url, file_name):
    # full_path = app.root_path + app.static_url_path + '/' + file_name
    full_path = app.root_path + '/' + file_name
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        # shutil.move(os.path.join(app.root_path, file_name),
        #             os.path.join(app.root_path + app.static_url_path, file_name))
        print('Image sucessfully Downloaded: ', full_path)
    else:
        print('Image Couldn\'t be retrieved')
    return app.root_path, file_name


def detect_captcha(url):
    reader = easyocr.Reader(['en', 'en'])  # this needs to run only once to load the model into memory
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
        args = parser.parse_args()
        isDownload = args['download']
        imageURL = args['image_url']
        if isDownload == 'true':
            try:
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
        else:
            response_number = detect_captcha(imageURL)
            return {
                "code": response_number
            }


api.add_resource(OCR, '/ocr')

if __name__ == '__main__':
    app.run()
