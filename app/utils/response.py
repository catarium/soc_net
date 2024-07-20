from starlette.responses import JSONResponse


class ResponseState:
    successful = 'successful'
    error = 'error'


class Response:
    def __new__(cls, state: str = ResponseState.successful, **kwargs) -> JSONResponse:
        json = {
            'state': state,
            **kwargs,
        }
        return json
