package users

import (
	"fmt"

	"github.com/Yakov-Varnaev/fakebank/db"
	"github.com/doug-martin/goqu/v9"
)

func GetUserByID(id string) (*User, error) {
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

func (u User) Refresh() error {
	if u.ID == "" {
		return fmt.Errorf("User ID is required")
	}

	dbUser, err := GetUserByID(u.ID)
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
