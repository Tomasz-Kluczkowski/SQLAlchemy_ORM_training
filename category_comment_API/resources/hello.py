from flask_restful import Resource


class Hello(Resource):

    def get(self): # this is a method for a GET request
        return {"message": "Get Hello World"}

    def post(self):
        return {"message": "Post Hello World"}
