package users

import (
	"github.com/Yakov-Varnaev/fakebank/db"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
)

const userTable = "users"

type UserDB struct{}

func (userDb *UserDB) GetUserByID(id string) (*User, error) {
	return db.GetByID[User](userTable, id, nil)
}

func (userDb *UserDB) Create(userData *UserRegisterData) (*User, error) {
	return db.Create[UserRegisterData, User](userTable, *userData)
}

func (userDb *UserDB) List(paginationParams *pagination.Params, filters *Filters) (*pagination.Page[*User], error) {
	page, err := db.List[*User](
		userTable,
		paginationParams,
		filters,
	)
	if err != nil {
		return nil, err
	}
	return page, nil
}
