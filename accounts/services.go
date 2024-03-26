package accounts

import (
	"fmt"
	"net/http"

	"github.com/Yakov-Varnaev/fakebank/db"
	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	"github.com/Yakov-Varnaev/fakebank/users"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
	"github.com/doug-martin/goqu/v9"
	"github.com/gin-gonic/gin"
)

type CreateService struct {
	UserID        string
	AccountCreate *AccountCreate
}

func (service *CreateService) FromContext(c *gin.Context) error {
	var accountCreate AccountCreate
	err := c.ShouldBindJSON(&accountCreate)
	if err != nil {
		return err
	}

	service.AccountCreate = &accountCreate

	user, ok := c.Get("user")
	if !ok || user == nil {
		panic("User not found in context")
	}

	service.UserID = user.(*users.User).ID
	return nil
}

func (service *CreateService) Act() (*Account, error) {
	accountCreateData := AccountCreateData{
		AccountCreate: *service.AccountCreate,
		UserID:        service.UserID,
	}

	account, err := db.Create[AccountCreateData, Account]("account", accountCreateData)
	if err != nil {
		return nil, err
	}
	return account, nil
}

type Filters struct {
	UserID string
	Query  string
}

func (filters *Filters) FromContext(c *gin.Context) error {
	filters.UserID = c.Query("user_id")
	filters.Query = c.Query("query")
	return nil
}

func (filter *Filters) Process(query *goqu.SelectDataset) *goqu.SelectDataset {
	if filter == nil {
		return query
	}

	if filter.UserID != "" {
		query = query.Where(goqu.C("user_id").Eq(filter.UserID))
	}

	if filter.Query != "" {
		query = query.Where(goqu.Or(
			goqu.C("name").ILike(fmt.Sprintf("%%%s%%", filter.Query)),
		))
	}
	return query
}

type ListService struct {
	PaginationParms *pagination.Params
	Filters         *Filters
}

func (service *ListService) FromContext(c *gin.Context) error {
	paginationParams, err := pagination.FromContext(c)
	if err != nil {
		return err
	}
	service.PaginationParms = paginationParams

	var filters Filters
	err = filters.FromContext(c)
	if err != nil {
		return err
	}
	service.Filters = &filters
	return nil
}

func (service *ListService) Act() (*pagination.Page[Account], error) {
	page, err := db.List[Account]("account", service.PaginationParms, service.Filters)
	if err != nil {
		return nil, err
	}
	return page, nil
}

type UpdateService struct {
	ID   string
	Data *AccountCreate
	User *users.User
}

func (service *UpdateService) FromContext(c *gin.Context) error {
	var data AccountCreate
	err := c.ShouldBindJSON(&data)
	if err != nil {
		return err
	}
	service.Data = &data
	service.ID = c.Param("id")

	user, ok := c.Get("user")
	if !ok || user == nil {
		panic("User not found in context")
	}

	service.User = user.(*users.User)
	return nil
}

func (service *UpdateService) Act() (*Account, error) {
	account, err := db.GetByID[Account]("account", service.ID, nil)
	if err != nil {
		return nil, err
	}

	if account == nil {
		return nil, &httpErrors.HTTPError{
			Code: http.StatusNotFound, Message: "Not found",
		}
	}

	if account.UserID != service.User.ID {
		return nil, &httpErrors.HTTPError{
			Code: http.StatusForbidden, Message: "Forbidden",
		}
	}

	updatedAccount, err := db.Update[AccountCreate, Account]("account", service.ID, *service.Data)
	if err != nil {
		return nil, err
	}

	return updatedAccount, nil
}
