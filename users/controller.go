package users

import (
	"fmt"
	"net/http"
	"strconv"
	"strings"

	"github.com/Yakov-Varnaev/fakebank/config"
	"github.com/Yakov-Varnaev/fakebank/db"
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

	err := c.ShouldBindJSON(&userData)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
		return
	}
	// lower case email
	userData.Email = strings.ToLower(userData.Email)

	err = userData.Validate()
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
		return
	}

	user, err := userData.Save()
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
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
	err = loginData.Validate()
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"detail": err.Error()})
	}
	user, err := loginData.Authenticate()
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"detail": err.Error()})
		return
	}
	token, err := CreateCookies(user)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
		return
	}

	c.SetCookie(config.AUTH_COOKIE_NAME, token, 60*60*24, "/", "localhost", false, true)
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
	db := db.GetDB()
	userId := c.Param("id")
	var user User
	err := db.QueryRow(
		`SELECT id, email, first_name, last_name FROM users WHERE users.id = $1 LIMIT 1`,
		userId,
	).Scan(&user.ID, &user.Email, &user.FirstName, &user.LastName)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detal": err.Error()})
		return
	}
	c.JSON(200, user)
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
//	@Success		200		{object}	UserPage
//	@Router			/users [get]
func (ctrl *Controller) List(c *gin.Context) {
	db := db.GetDB()
	offsetStr := c.DefaultQuery("offset", "0")
	offset, err := strconv.Atoi(offsetStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": "Invalid offset"})
		return
	}

	limitStr := c.DefaultQuery("limit", "10")
	limit, err := strconv.Atoi(limitStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": "Invalid limit"})
		return
	}

	baseQuery := `SELECT id, email, first_name, last_name FROM users`
	pageQuery := fmt.Sprintf(`%s %s`, baseQuery, `LIMIT $1 OFFSET $2`)

	rows, err := db.Query(
		pageQuery,
		limit,
		offset,
	)

	result := make([]User, 0)
	for {
		ok := rows.Next()
		if !ok {
			err = rows.Err()
			if err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
				return
			}
			break
		}
		var id, email, firstName, lastName string
		rows.Scan(&id, &email, &firstName, &lastName)
		user := User{ID: id, Email: email, FirstName: firstName, LastName: lastName}
		result = append(result, user)
	}

	var total int
	err = db.QueryRow(`SELECT COUNT(*) FROM users`).Scan(&total)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
		return
	}

	c.JSON(200, UserPage{Total: total, Data: result})
}

// Authenticated endpoint godoc
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
