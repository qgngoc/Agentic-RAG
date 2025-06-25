from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI, responses
import uvicorn

from adapters.primary.rest.routers.generate_response_router import router as generate_response_router
from adapters.primary.rest.routers.get_read_file_config_router import router as get_read_file_config_router
from adapters.primary.rest.routers.get_llm_configs_router import router as get_llm_configs_router
from adapters.primary.rest.routers.index_document_router import router as index_document_router

app = FastAPI()

# add health check endpoint
@app.get("/health")
async def health_check():
    return responses.JSONResponse(
        content={"status": "ok"},
        status_code=200
    )

app.include_router(
    generate_response_router,
    prefix="/api/v1")

app.include_router(
    get_read_file_config_router,
    prefix="/api/v1")

app.include_router(
    get_llm_configs_router,
    prefix="/api/v1")

app.include_router(
    index_document_router,
    prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8113, reload=False)
    