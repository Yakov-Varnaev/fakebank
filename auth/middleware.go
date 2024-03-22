package auth

import (
	"fmt"
	"net/http"

	"github.com/Yakov-Varnaev/fakebank/config"
	"github.com/gin-gonic/gin"
)

func AuthenticateMiddleware(authenticatedOnly bool) gin.HandlerFunc {
	return func(c *gin.Context) {
		token, err := c.Cookie(config.AUTH_COOKIE_NAME)
		if err != nil {
			if authenticatedOnly {
				c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Auth cookie is missing"})
				return
			}
			c.Next()
			return
		}

		user, err := ValidateJWTToken(token)
		if err != nil {
			fmt.Println(err)
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid token"})
			return
		}

		c.Set("user", user)
		c.Next()
	}
}
