package auth

import (
	"fmt"
	"net/http"

	"github.com/Yakov-Varnaev/fakebank/config"
	"github.com/Yakov-Varnaev/fakebank/users"
	"github.com/gin-gonic/gin"
)

func CheckToken(token string) (*users.User, error) {
	user, ok := users.SessionStore[token]
	if !ok {
		return nil, fmt.Errorf("Invalid token")
	}
	return user, nil
}

func AuthenticateMiddleware(authenticatedOnly bool) gin.HandlerFunc {
	return func(c *gin.Context) {
		token, err := c.Cookie(config.AUTH_COOKIE_NAME)
		if err != nil {
			if authenticatedOnly {
				c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Auth cookie is missing"})
				return
			} else {
				c.Next()
				return
			}
		}

		if token == "" {
			if authenticatedOnly {
				c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Auth cookie is missing"})
				return
			} else {
				c.Next()
				return
			}
		}

		user, err := CheckToken(token)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid token check token"})
			return
		}

		err = user.Refresh()
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid token user refresh." + err.Error()})
			return
		}

		// if !user.IsActive {
		// 	c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "User is not active"})
		// 	return
		// }

		c.Set("user", user)
		c.Next()
	}
}
