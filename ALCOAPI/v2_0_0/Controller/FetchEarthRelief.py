# nomarl module
from flask import Blueprint, request, Response
from jsonschema import validate, ValidationError
from logging import getLogger
import time, json, re, os

# my module
from ..DB import CreateEngine,  makeSession, models
from .CreateHistory import CreateHistory as CH
from .Responses import Responses
from .tools import ValidateSessionID, ReadJson

# initialize

## register blueprint
FetchEarthRelief = Blueprint("FetchEarthRelief", __name__, url_prefix="/ALCOAPI/v2.0.0/FetchEarthRelief")

## get env
VERSION = os.environ.get("VERSION")

## create db engine
CE = CreateEngine.CreateEngine()

## get logger
logger = getLogger("MainLog").getChild("FetchEarthRelief")

## register re matcher
pattern_userID = r'[a-e0-9]'
matcher_userID = re.compile(pattern_userID)

## json schema path
PATH_SCHEMA = f"ALCOAPI/{VERSION}/Controller/schema/FetchEarthRelief_post.json"

## instance Resposnses
Status = Responses()
