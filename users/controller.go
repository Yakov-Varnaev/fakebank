package users

import (
	"net/http"

	"github.com/Yakov-Varnaev/fakebank/config"
	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
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

// Signin godoc
//
//	@Summary	Sign In
//	@Tags		users, auth
//	@Accept		json
//	@Produce	json
//	@Param		loginData	body	UserLoginData	true	"User Credentials"
//	@Success	200
//	@Router		/auth/signin [post]
func (ctrl *Controller) Signin(c *gin.Context) {
	var loginData UserLoginData

	err := c.ShouldBindJSON(&loginData)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
		return
	}

	service := SigninService{Data: &loginData}
	token, err := service.Act()
	if err != nil {
		err := httpErrors.GetHTTPError(err)
		c.AbortWithStatusJSON(err.Code, gin.H{"detail": err.Error()})
	}

	c.SetCookie(config.AUTH_COOKIE_NAME, token, config.TOKEN_LIFETIME, "/", "localhost", false, true)
	c.Status(http.StatusOK)
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
	userId := c.Param("id")

	user, err := RetrieveService{ID: userId}.Act()
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
//	@Success		200 {object}	User
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
//	@Param			offset	query		int	false	"Offset"
//	@Param			limit	query		int	false	"Limit"
//	@Success		200		{object} pagination.Page[User]
//	@Router			/users [get]
func (ctrl *Controller) List(c *gin.Context) {
	paginationParams, _ := pagination.FromContext(c)

	query := c.DefaultQuery("query", "")

	page, err := ListingService{Pagination: paginationParams, Query: query}.Act()

	if err := httpErrors.GetHTTPError(err); err != nil {
		c.JSON(err.Code, gin.H{"detail": err.Message})
		return
	}

	c.JSON(http.StatusOK, page)
}
