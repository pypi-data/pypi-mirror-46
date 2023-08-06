from flask import jsonify, request
from flask_restful import Resource, reqparse


class SignalMap(Resource):

    def get(self):
        """
        response = {
            "internalSignalName1": "externalSignalName1",
            "internalSignalName2": "externalSignalName2"
        }
        """
        pass

    def post(self):
        """
        request = {
            "internalSignalName1": "externalSignalName1",
            "internalSignalName2": "externalSignalName2"
        }
        """
        pass

