package auth

import (
	"net/http"

	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	"github.com/Yakov-Varnaev/fakebank/users"
)

type DoesNotExistError struct{}

func (e *DoesNotExistError) Error() string {
	return "User not found"
}

type SigninService struct {
	Data *users.UserLoginData
	db   *users.UserDB
}

func (service *SigninService) Act() (string, error) {
	err := service.Data.Validate()
	if err != nil {
		return "", &httpErrors.HTTPError{Code: http.StatusBadRequest, Message: err.Error()}
	}
	user, err := service.Data.Authenticate()
	if err != nil {
		return "", &httpErrors.HTTPError{Code: http.StatusUnauthorized, Message: err.Error()}
	}
	token, err := CreateJWTToken(user.ID)
	if err != nil {
		return "", &httpErrors.HTTPError{Code: http.StatusInternalServerError, Message: err.Error()}
	}
	return token, nil
}
