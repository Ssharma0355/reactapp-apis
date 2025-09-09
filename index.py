from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Debug root
@app.get("/")
def root():
    return {"status": "API running 🚀", "EMAIL_USER": os.getenv("EMAIL_USER", "NOT_SET")}

# Allow frontend origin(s)
origins = [
    "http://localhost:3000",              # Local dev
    "http://127.0.0.1:3000",              # Local dev
    "https://react-tech-social-media.vercel.app",  # Deployed frontend
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # loosen in dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes
from routes.user import user
app.include_router(user, prefix="/user", tags=["Users"])

# Required for Vercel (ASGI → Lambda)
handler = Mangum(app)
