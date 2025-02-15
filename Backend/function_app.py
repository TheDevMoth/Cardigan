import azure.functions as func
from src.app import app as fastapp

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def main(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger that handles requests to the FastAPI app."""

    return app.AsgiMiddleware(fastapp).handle(req)