import azure.functions as func
from src.app import app as fastapp

# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app = func.AsgiFunctionApp(app=fastapp,http_auth_level=func.AuthLevel.ANONYMOUS)
