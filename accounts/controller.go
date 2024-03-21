package accounts

import (
	"net/http"

	"github.com/Yakov-Varnaev/fakebank/db"
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
	var accountData AccountCreate
	err := c.ShouldBindJSON(&accountData)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
		return
	}
	accountCreateData := AccountCreateData{
		AccountCreate: accountData,
		UserID:        "d7c77823-2eff-4f1e-ac84-cc3f33e6a570",
	}

	account, err := db.Create[AccountCreateData, Account]("account", accountCreateData)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
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
