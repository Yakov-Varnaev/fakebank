package users

import (
	"fmt"

	"github.com/Yakov-Varnaev/fakebank/db"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
	"github.com/doug-martin/goqu/v9"
	"github.com/google/uuid"
)

type Page[T any] struct {
	Total int64 `json:"total"`
	Data  []T   `json:"data"`
}

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

func (userDb *UserDB) List(paginationParams *pagination.Params, searchQuery string) (*Page[*User], error) {
	var users []*User
	query := db.GetDB().From("users")
	if paginationParams != nil {
		query = query.Limit(uint(paginationParams.Limit)).Offset(uint(paginationParams.Offset))
	}

	if searchQuery != "" {
		query = query.Where(goqu.Or(
			goqu.C("email").ILike(fmt.Sprintf("%%%s%%", searchQuery)),
			goqu.L("CONCAT(first_name, ' ', last_name) ILIKE ?", fmt.Sprintf("%%%s%%", searchQuery)),
			goqu.L("CONCAT(last_name, ' ', first_name) ILIKE ?", fmt.Sprintf("%%%s%%", searchQuery)),
		))
	}

	err := query.ScanStructs(&users)
	if err != nil {
		return nil, err
	}

	total, err := query.Count()
	if err != nil {
		return nil, err
	}
	page := &Page[*User]{
		Total: total,
		Data:  users,
	}
	return page, nil
}
