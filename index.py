from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend origin(s)
origins = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",  # sometimes needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

# include your routers
from routes.user import user
app.include_router(user, prefix="/user", tags=["Users"])
