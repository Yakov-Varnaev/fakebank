package accounts

import (
	"github.com/Yakov-Varnaev/fakebank/db"
	"github.com/Yakov-Varnaev/fakebank/users"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
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
}

func (filters *Filters) FromContext(c *gin.Context) error {
	filters.UserID = c.Query("user_id")
	return nil
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
	filters.FromContext(c)

	return nil
}

func (service *ListService) Act() (*pagination.Page[Account], error) {
	page, err := db.List[Account]("account", service.PaginationParms)
	if err != nil {
		return nil, err
	}
	return page, nil
}
