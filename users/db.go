package users

import (
	"fmt"

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

func (userDb *UserDB) List(paginationParams *pagination.Params, searchQuery string) (*pagination.Page[*User], error) {
	filterFunc := func(query *goqu.SelectDataset) *goqu.SelectDataset {
		if searchQuery != "" {
			query = query.Where(goqu.Or(
				goqu.C("email").ILike(fmt.Sprintf("%%%s%%", searchQuery)),
				goqu.L("CONCAT(first_name, ' ', last_name) ILIKE ?", fmt.Sprintf("%%%s%%", searchQuery)),
				goqu.L("CONCAT(last_name, ' ', first_name) ILIKE ?", fmt.Sprintf("%%%s%%", searchQuery)),
			))
		}
		return query
	}
	page, err := db.List[*User](
		"users",
		paginationParams,
		filterFunc,
	)
	if err != nil {
		return nil, err
	}
	return page, nil
}
