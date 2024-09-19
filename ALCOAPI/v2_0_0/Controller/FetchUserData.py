# nomarl module
from flask import Blueprint, request, Response
from jsonschema import validate, ValidationError
from logging import getLogger
import time, json, re, os

# my module
from ..DB import CreateEngine,  makeSession, models
from .Responses import Responses
from .tools import ValidateSessionID, ReadJson

# initialize

## register blueprint
FetchUserData = Blueprint("FetchUserData", __name__, url_prefix="ALCOAPI/v2.0.0/FetchUserData")

## get env
VERSION = os.environ.get("VERSION")

## create db engine
CE = CreateEngine.CreateEngine()

## get logger
logger = getLogger("MainLog").getChild("FetchUserData")

## register re matcher
pattern_userID = r'[a-e0-9]'
matcher_userID = re.compile(pattern_userID)

## json schema path
PATH_SCHEMA = f"ALCOAPI/{VERSION}/Controller/schema/FetchUserData_put.json"

## instance Resposnses
Status = Responses()

# router
@FetchUserData.route("/<input_userID>", methods=["get"])
def get_FetchUserData(input_userID):
    
    return 

@FetchUserData.route("/<input_userID>", methods=["put"])
def put_FetchUserData(input_userID):
    
    return