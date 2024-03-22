package users

import (
	"database/sql"
	"net/http"

	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
)

type EmailAlreadyExistsError struct{}

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

type RetrieveService struct {
	ID string
	db *UserDB
}

func (service RetrieveService) Act() (*User, error) {
	user, err := service.db.GetUserByID(service.ID)

	if err == sql.ErrNoRows {
		return nil, &httpErrors.HTTPError{
			Code: http.StatusNotFound, Message: "User not found",
		}
	}
	if err != nil {
		return nil, &httpErrors.HTTPError{
			Code: http.StatusInternalServerError, Message: err.Error(),
		}
	}

	return user, nil
}

type ListingService struct {
	Pagination *pagination.Params
	Query      string
	db         *UserDB
}

func (service ListingService) Act() (*pagination.Page[*User], error) {
	users, err := service.db.List(service.Pagination, service.Query)
	if err != nil {
		return nil, &httpErrors.HTTPError{
			Code: http.StatusInternalServerError, Message: err.Error(),
		}
	}
	return users, nil
}
