package auth

import (
	"net/http"

	"github.com/Yakov-Varnaev/fakebank/config"
	httpErrors "github.com/Yakov-Varnaev/fakebank/errors"
	"github.com/Yakov-Varnaev/fakebank/users"
	"github.com/gin-gonic/gin"
)

type Controller struct{}

// Signin godoc
//
//	@Summary	Sign In
//	@Tags		users, auth
//	@Accept		json
//	@Produce	json
//	@Param		loginData	body	users.UserLoginData	true	"User Credentials"
//	@Success	200
//	@Router		/auth/signin [post]
func (ctrl *Controller) Signin(c *gin.Context) {
	var loginData users.UserLoginData

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
