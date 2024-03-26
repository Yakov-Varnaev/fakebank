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

	service.Data.IsActive = true
	service.Data.IsVerified = false
	service.Data.IsSuperuser = false
	hashedPassword, err := HashPassword(service.Data.Password)
	if err != nil {
		return nil, err
	}
	service.Data.Password = hashedPassword
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

func (filters *Filters) Process(query *goqu.SelectDataset) *goqu.SelectDataset {
	if filters == nil || filters.Query == "" {
		return query
	}

	return query.Where(goqu.Or(
		goqu.C("email").ILike(fmt.Sprintf("%%%s%%", filters.Query)),
		goqu.L("CONCAT(first_name, ' ', last_name) ILIKE ?", fmt.Sprintf("%%%s%%", filters.Query)),
		goqu.L("CONCAT(last_name, ' ', first_name) ILIKE ?", fmt.Sprintf("%%%s%%", filters.Query)),
	))
}

type ListingService struct {
	Pagination *pagination.Params
	Filters    *Filters
	db         *UserDB
}

func (service *ListingService) FromContext(c *gin.Context) error {
	var filters Filters
	var err error
	filters.FromContext(c)
	service.Filters = &filters
	service.Pagination, err = pagination.FromContext(c)
	if err != nil {
		return &httpErrors.HTTPError{Code: http.StatusBadRequest, Message: err.Error()}
	}
	return nil
}

func (service ListingService) Act() (*pagination.Page[*User], error) {
	return db.List[*User]("users", service.Pagination, service.Filters)
}
