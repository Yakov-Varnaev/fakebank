package users

import (
	"database/sql"
	"fmt"
	"net/http"

	"github.com/Yakov-Varnaev/fakebank/db"
	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
	"github.com/doug-martin/goqu/v9"
	"github.com/gin-gonic/gin"
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

func (service *RetrieveService) FromContext(c *gin.Context) error {
	service.ID = c.Param("id")
	return nil
}

type Filters struct {
	Query string
}

func (filters *Filters) FromContext(c *gin.Context) {
	filters.Query = c.Query("query")
}

func (filters *Filters) FilterFunc(query *goqu.SelectDataset) *goqu.SelectDataset {
	if filters.Query != "" {
		query = query.Where(goqu.Or(
			goqu.C("name").ILike(fmt.Sprintf("%%%s%%", filters.Query)),
		))
	}
	return query
}

type ListingService struct {
	Pagination *pagination.Params
	Query      *Filters
	db         *UserDB
}

func (service *ListingService) FromContext(c *gin.Context) error {
	var filters Filters
	filters.FromContext(c)
	return nil
}

func (service ListingService) Act() (*pagination.Page[*User], error) {
	return db.List[*User]("users", service.Pagination, service.Query.FilterFunc)
}
