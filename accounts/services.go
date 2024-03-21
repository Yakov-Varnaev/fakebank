package accounts

import (
	"github.com/Yakov-Varnaev/fakebank/db"
	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
	"github.com/gin-gonic/gin"
)

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

	if err := httpErrors.GetHTTPError(err); err != nil {
		return nil, err
	}
	return page, nil
}
