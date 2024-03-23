package users

import (
	"net/http"

	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	_ "github.com/Yakov-Varnaev/fakebank/utils"
	"github.com/gin-gonic/gin"
)

type Controller struct{}

type UserPage struct {
	Total int    `json:"total"`
	Data  []User `json:"data"`
}

// Register user godoc
//
//	@Summary	Create new user
//	@Tags		users
//	@Accept		json
//	@Produce	json
//	@Param		data	body		UserRegisterData	true	"User Register Data"
//	@Success	200		{object}	User
//	@Router		/users [post]
func (ctrl *Controller) Signup(c *gin.Context) {
	var userData UserRegisterData
	err := c.ShouldBindJSON(userData)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
		return
	}

	service := SignupSerivce{Data: &userData}
	user, err := service.Signup()
	if err != nil {
		httpErr := httpErrors.GetHTTPError(err)
		c.JSON(httpErr.Code, gin.H{"detail": httpErr.Message})
		return
	}

	c.JSON(http.StatusCreated, user)
}

// Retrieve user godoc
//
//	@Summary		Retrieve user
//	@Description	Retrieve user
//	@Tags			users
//	@Accept			json
//	@Produce		json
//	@Param			id	path		string	true	"User ID"
//	@Success		200	{object}	User
//	@Router			/users/{id} [get]
func (ctrl *Controller) Retrieve(c *gin.Context) {
	var service RetrieveService
	service.FromContext(c)

	user, err := service.Act()
	if err := httpErrors.GetHTTPError(err); err != nil {
		c.JSON(err.Code, gin.H{"detail": err.Message})
		return
	}

	c.JSON(http.StatusOK, user)
}

// Get current user godoc
//
//	@Summary		Authenticated endpoint
//	@Description	Authenticated endpoint
//	@Tags			users
//	@Accept			json
//	@Produce		json
//	@Security		Bearer
//	@Success		200	{object}	User
//	@Router			/users/me [get]
func (ctrl *Controller) RetrieveMe(c *gin.Context) {
	user := c.MustGet("user").(*User)
	c.JSON(http.StatusOK, user)
}

// List users godoc
//
//	@Summary		List user
//	@Description	List user
//	@Tags			users
//	@Accept			json
//	@Produce		json
//	@Param			offset	query		int		false	"Offset"
//	@Param			limit	query		int		false	"Limit"
//	@Param			query	query		string	false	"Search query"
//	@Success		200		{object}	pagination.Page[User]
//	@Router			/users [get]
func (ctrl *Controller) List(c *gin.Context) {
	var service ListingService
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
