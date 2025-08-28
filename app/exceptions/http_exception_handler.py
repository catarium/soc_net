from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request
from starlette.responses import JSONResponse


def register_http_exception_handler(app):

    @app.exception_handler(StarletteHTTPException)
    async def http_exc_handler(request: Request, exc: StarletteHTTPException):
        # Exc.detail can already be a list/dict—if you want always list-of-detail-objects:
        detail = exc.detail if isinstance(exc.detail, list) else [
            {"loc": ["body"], "msg": exc.detail,
                "type": f"http_error.{exc.status_code}"}
        ]
        return JSONResponse(status_code=exc.status_code, content={"detail": detail})
