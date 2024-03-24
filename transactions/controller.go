package transactions

import (
	"net/http"

	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	"github.com/gin-gonic/gin"
)

type Controller struct{}

// Create Account redoc
//
//	@Summary Create Transaction
//	@Tags transactions
//	@Accept json
//	@Produce json
//	@Param data body TransactionCreateData true "Transaction Data"
//	@Success 200
//	@Router /transactions [post]
func (ctrl *Controller) Create(c *gin.Context) {
	var service CreateService
	service.FromContext(c)

	transaction, err := service.Act()
	if err := httpErrors.GetHTTPError(err); err != nil {
		c.AbortWithStatusJSON(err.Code, gin.H{"detail": err.Message})
		return
	}

	c.JSON(http.StatusCreated, transaction)
}
