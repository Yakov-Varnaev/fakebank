package users

import (
	"database/sql"
	"net/http"

	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
)

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

func (service ListingService) Act() (*Page[*User], error) {
	users, err := service.db.List(service.Pagination, service.Query)
	if err != nil {
		return nil, &httpErrors.HTTPError{
			Code: http.StatusInternalServerError, Message: err.Error(),
		}
	}
	return users, nil
}
