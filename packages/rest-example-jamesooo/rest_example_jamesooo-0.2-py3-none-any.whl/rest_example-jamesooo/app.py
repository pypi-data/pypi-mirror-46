from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Pong(Resource):
    def get(self):
        return {'message': 'pong'}

api.add_resource(Pong, '/')
if __name__ == '__main__':
    app.run()

