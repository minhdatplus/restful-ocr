from flask import Flask
from flask_restful import Resource, Api, reqparse
import easyocr

app = Flask(__name__, static_url_path='/static')
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('image_url')


class OCR(Resource):
    def post(self):
        args = parser.parse_args()
        reader = easyocr.Reader(['en', 'en'])  # this needs to run only once to load the model into memory
        result = reader.readtext(args['image_url'])
        response_number = 0
        for cap in result:
            try:
                response_number = cap[1]
                continue
            except ValueError:
                print("Catch Error")
        return {
            "code": response_number
        }


api.add_resource(OCR, '/ocr')

if __name__ == '__main__':
    app.run()
