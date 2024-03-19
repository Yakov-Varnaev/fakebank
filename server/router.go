package server

import (
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
		userGroup := v1.Group("users")
		{
			user := new(users.Controller)
			userGroup.GET("/:id", user.Retrieve)
			userGroup.POST("/", user.Signup)
			userGroup.GET("/", user.List)
		}
	}

	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	return router
}
