package accounts

import (
	"net/http"

	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	_ "github.com/Yakov-Varnaev/fakebank/utils"
	"github.com/gin-gonic/gin"
)

type Controller struct{}

// Create Account godoc
//
//	@Summary	Create new account
//	@Tags		accounts
//	@Accept		json
//	@Produce	json
//	@Param		data	body		AccountCreate	true	"Account Data"
//	@Success	200		{object}	Account
//	@Router		/accounts [post]
func (ctrl *Controller) CreateAccount(c *gin.Context) {
	var service CreateService
	err := service.FromContext(c)
	if err := httpErrors.GetHTTPError(err); err != nil {
		c.JSON(err.Code, gin.H{"detail": err.Message})
		return
	}
	account, err := service.Act()
	if err := httpErrors.GetHTTPError(err); err != nil {
		c.JSON(err.Code, gin.H{"detail": err.Message})
		return
	}

	c.JSON(http.StatusOK, account)
}

// List Accounts godoc
//
//	@Summary	List accounts
//	@Tags		accounts
//	@Accept		json
//	@Produce	json
//	@Param		offset	query		int		false	"Offset"
//	@Param		limit	query		int		false	"Limit"
//	@Param		user_id	query		string	false	"User ID"
//	@Param		query query		string	false	"Search query"
//	@Success	200		{object}	pagination.Page[Account]
//	@Router		/accounts [get]
func (ctrl *Controller) List(c *gin.Context) {
	var service ListService
	err := service.FromContext(c)
	if err := httpErrors.GetHTTPError(err); err != nil {
		c.JSON(err.Code, gin.H{"detail": err.Message})
		return
	}

	page, err := service.Act()
	if err := httpErrors.GetHTTPError(err); err != nil {
		c.JSON(err.Code, gin.H{"detail": err.Message})
		return
	}
	c.JSON(http.StatusOK, page)
}
