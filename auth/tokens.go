package auth

import (
	"fmt"
	"time"

	"github.com/Yakov-Varnaev/fakebank/config"
	"github.com/Yakov-Varnaev/fakebank/users"
	"github.com/golang-jwt/jwt/v5"
)

func CreateJWTToken(user_id string) (string, error) {
	claims := Claims{
		UserId: user_id,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Hour * 24)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Issuer:    "fakebank",
		},
	}
	jwtToken := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	token, err := jwtToken.SignedString([]byte(config.SECRET))
	if err != nil {
		return "", err
	}
	return token, nil
}

func ValidateJWTToken(tokenString string) (*users.User, error) {
	token, err := jwt.ParseWithClaims(
		tokenString,
		&Claims{},
		func(token *jwt.Token) (interface{}, error) {
			return []byte(config.SECRET), nil
		},
		jwt.WithLeeway(5*time.Second),
	)
	if err != nil {
		return nil, err
	}
	tokenClaims, ok := token.Claims.(*Claims)
	if !ok {
		return nil, fmt.Errorf("Invalid token claims")
	}

	var udb users.UserDB
	user, err := udb.GetUserByID(tokenClaims.UserId)
	if err != nil {
		return nil, err
	}
	return user, nil
}
