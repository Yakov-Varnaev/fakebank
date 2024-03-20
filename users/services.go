package users

import (
	"net/http"

	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
)

type EmailAlreadyExistsError struct{}

type DoesNotExistError struct{}

func (e *DoesNotExistError) Error() string {
	return "User not found"
}

func (e *EmailAlreadyExistsError) Error() string {
	return "User already exists"
}

type SignupSerivce struct {
	Data *UserRegisterData
	db   *UserDB
}

func (service *SignupSerivce) Validate() error {
	if err := service.Data.Validate(); err != nil {
		return &httpErrors.ValidationError{Message: err.Error()}
	}
	return nil
}

func (service *SignupSerivce) Signup() (*User, error) {
	if err := service.Validate(); err != nil {
		return nil, &httpErrors.HTTPError{Code: http.StatusBadRequest, Message: err.Error()}
	}

	user, err := service.db.Create(service.Data)
	if err != nil {
		return nil, &httpErrors.HTTPError{Code: http.StatusInternalServerError, Message: err.Error()}
	}

	return user, nil
}
