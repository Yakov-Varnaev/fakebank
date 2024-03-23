package server

import (
	"github.com/Yakov-Varnaev/fakebank/accounts"
	"github.com/Yakov-Varnaev/fakebank/auth"
	"github.com/Yakov-Varnaev/fakebank/users"
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"

	_ "github.com/Yakov-Varnaev/fakebank/docs"
)

func NewRouter() *gin.Engine {
	router := gin.New()
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	api := router.Group("/api")
	v1 := api.Group("v1")
	{
		authGroup := v1.Group("auth")
		{
			auth := new(auth.Controller)
			authGroup.POST("/signin", auth.Signin)
		}

		userGroup := v1.Group("users")
		{
			user := new(users.Controller)
			userGroup.GET("/:id", user.Retrieve)
			userGroup.POST("/", user.Signup)
			userGroup.GET("/", user.List)

			userAuthenticatedOnlyGroup := userGroup.Group("/")
			userAuthenticatedOnlyGroup.Use(auth.AuthenticateMiddleware(true))
			userAuthenticatedOnlyGroup.GET("/me", user.RetrieveMe)
		}
		accountGroup := v1.Group("accounts")
		accountGroup.Use(auth.AuthenticateMiddleware(true))
		{
			account := new(accounts.Controller)
			accountGroup.POST("/", account.Create)
			accountGroup.GET("/", account.List)
			accountGroup.PUT("/:id", account.Update)
		}
	}

	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	return router
}
