import json
import logging
import os
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Observra GCP Log Test Service")
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("observra-log-test")


def log_event(level: str, event: str, request_id: str, **fields: object) -> None:
    payload = {"service": "observra-gcp-log-test", "event": event, "request_id": request_id, **fields}
    getattr(logger, level)(json.dumps(payload))


@app.get("/")
def health(request: Request) -> dict:
    log_event("info", "health_check", request.headers.get("x-request-id", str(uuid.uuid4())))
    return {"ok": True, "service": "observra-gcp-log-test"}


@app.get("/api/success")
def success(request: Request) -> dict:
    log_event("info", "request_completed", request.headers.get("x-request-id", str(uuid.uuid4())), endpoint="/api/success")
    return {"ok": True, "message": "Successful test response"}


@app.get("/api/error")
def intentional_error(request: Request) -> JSONResponse:
    error_id = str(uuid.uuid4())
    log_event("error", "intentional_application_error", request.headers.get("x-request-id", str(uuid.uuid4())), endpoint="/api/error", error_id=error_id, error_type="TestApplicationError", message="Intentional error generated for Observra testing")
    return JSONResponse({"ok": False, "error": {"id": error_id, "type": "TestApplicationError", "message": "Intentional error generated for Observra testing"}}, status_code=500)


@app.get("/api/slow-error")
def slow_error(request: Request) -> JSONResponse:
    time.sleep(float(os.getenv("SLOW_ERROR_DELAY_SECONDS", "2")))
    error_id = str(uuid.uuid4())
    log_event("error", "intentional_timeout_error", request.headers.get("x-request-id", str(uuid.uuid4())), endpoint="/api/slow-error", error_id=error_id, error_type="TestTimeoutError", message="Intentional delayed error generated for Observra testing")
    return JSONResponse({"ok": False, "error": {"id": error_id, "type": "TestTimeoutError", "message": "Intentional delayed error generated for Observra testing"}}, status_code=504)


@app.exception_handler(Exception)
async def unhandled_error(request: Request, error: Exception) -> JSONResponse:
    error_id = str(uuid.uuid4())
    log_event("exception", "unhandled_exception", request.headers.get("x-request-id", str(uuid.uuid4())), error_id=error_id, error_type=type(error).__name__, message=str(error))
    return JSONResponse({"ok": False, "error": {"id": error_id, "type": "UnhandledApplicationError", "message": "Unhandled test application error"}}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
