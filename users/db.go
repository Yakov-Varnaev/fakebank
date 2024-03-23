package users

import (
	"github.com/Yakov-Varnaev/fakebank/db"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
	"github.com/doug-martin/goqu/v9"
)

type UserDB struct{}

func (userDb *UserDB) GetUserByID(id string) (*User, error) {
	return db.GetByID[User]("users", id)
}

func (userDb *UserDB) Create(userData *UserRegisterData) (*User, error) {
	return db.Create[UserRegisterData, User]("user", *userData)
}

func (userDb *UserDB) List(paginationParams *pagination.Params, filters *Filters) (*pagination.Page[*User], error) {
	page, err := db.List[*User](
		"users",
		paginationParams,
		filters.FilterFunc,
	)
	if err != nil {
		return nil, err
	}
	return page, nil
}
