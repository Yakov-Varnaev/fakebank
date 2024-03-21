package httpErrors

import "net/http"

type HTTPError struct {
	Code    int
	Message string
}

func (e *HTTPError) Error() string {
	return e.Message
}

type ValidationError struct {
	Message string
}

func (e *ValidationError) Error() string {
	return e.Message
}

func GetHTTPError(err error) *HTTPError {
	if err == nil {
		return nil
	}
	httpError, ok := err.(*HTTPError)
	if !ok {
		return &HTTPError{Code: http.StatusInternalServerError, Message: err.Error()}
	}
	return httpError
}
