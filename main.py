from starlette.middleware.cors import CORSMiddleware
from dbs.load_data import load_data
from settings import settings
from router import api_router
from fastapi import FastAPI

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_VERSION}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_event_handler('startup', load_data)

@app.get("/", tags=["Health Check"], response_description="Ok", response_model=str)
async def health_check():
    return "ok"


app.include_router(api_router, prefix=settings.API_VERSION)
