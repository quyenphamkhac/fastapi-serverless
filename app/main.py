from fastapi import FastAPI
from mangum import Mangum
from .utils.power_tools import logger
import uvicorn

app = FastAPI()


@app.get("/")
def get_root():
    print("test")
    logger.info("Test fastapi with aws powertools")
    return {"message": "FastAPI running in a lambda function"}


handler = Mangum(app)
handler = logger.inject_lambda_context(handler, clear_state=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
