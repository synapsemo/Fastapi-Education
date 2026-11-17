import os
from fastapi import FastAPI, Depends, Request
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

oauth = OAuth()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Configure Google OAuth2 credentials
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID", "your-google-client-id"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET", "your-google-client-secret"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid profile email"},
)


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    authorization_url = await oauth.google.authorize_redirect(request, redirect_uri)
    return authorization_url


# callback route
@app.route("/auth")
async def auth(request):
    token = await oauth.google_authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return JSONResponse(content={"user":user})







