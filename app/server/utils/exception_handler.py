from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from server.utils.i18n import translate_error

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    locale = request.headers.get('Accept-Language', 'en').split(',')[0]

    translated_errors = []
    for err in exc.errors():
        err_code = err.get("type", "unknown_error")
        err["msg"] = translate_error(err_code, locale)
        translated_errors.append(err)

    return JSONResponse(
        status_code=422,
        content={"detail": translated_errors}
    )