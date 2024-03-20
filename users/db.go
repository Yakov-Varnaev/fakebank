package users

import (
	"fmt"

	"github.com/Yakov-Varnaev/fakebank/db"
	"github.com/doug-martin/goqu/v9"
	"github.com/google/uuid"
)

type UserDB struct{}

func (userDb *UserDB) GetUserByID(id string) (*User, error) {
	var user User
	found, err := db.GetDB().From("users").Where(goqu.C("id").Eq(id)).ScanStruct(&user)
	if err != nil {
		return nil, err
	}
	if !found {
		return nil, fmt.Errorf("User not found")
	}
	return &user, nil
}

func (userDb *UserDB) Create(userData *UserRegisterData) (*User, error) {
	user := User{
		ID:          uuid.NewString(),
		Email:       userData.Email,
		FirstName:   userData.FirstName,
		LastName:    userData.LastName,
		IsActive:    userData.IsActive,
		IsSuperuser: userData.IsSuperuser,
		IsVerified:  userData.IsVerified,
	}

	hashedPassword, err := HashPassword(userData.Password)
	if err != nil {
		return nil, err
	}
	user.Password = hashedPassword

	_, err = db.GetDB().Insert("users").Rows(user).Returning(&user).Executor().ScanStruct(&user)
	if err != nil {
		return nil, err
	}

	return &user, nil
}

func (u User) Refresh() error {
	if u.ID == "" {
		return fmt.Errorf("User ID is required")
	}
	var userDb UserDB

	dbUser, err := userDb.GetUserByID(u.ID)
	if err != nil {
		return err
	}
	u.Email = dbUser.Email
	u.FirstName = dbUser.FirstName
	u.LastName = dbUser.LastName
	u.IsActive = dbUser.IsActive
	u.IsSuperuser = dbUser.IsSuperuser
	u.IsVerified = dbUser.IsVerified

	return nil
}
