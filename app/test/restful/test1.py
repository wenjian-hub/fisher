from flask import Flask, request
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


class HelloWord(Resource):
    def get(self):
        return {"hello": "world"}

    
api.add_resource(HelloWord, "/", "/hello")


if __name__ == '__main__':
    app.run(debug=True)
