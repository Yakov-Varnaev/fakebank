package users

import (
	"fmt"

	"github.com/Yakov-Varnaev/fakebank/db"
	"github.com/google/uuid"
)

type User struct {
	ID          string `json:"id"`
	FirstName   string `json:"first_name"`
	LastName    string `json:"last_name"`
	Email       string `json:"email"`
	IsActive    bool   `json:"is_active"`
	IsSuperuser bool   `json:"is_superuser"`
	IsVerified  bool   `json:"is_verified"`
}

type UserRegisterData struct {
	Email       string `json:"email,omitempty"`
	FirstName   string `json:"first_name,omitempty"`
	LastName    string `json:"last_name,omitempty"`
	Password    string `json:"password,omitempty"`
	IsActive    bool   `json:"is_active,omitempty"`
	IsSuperuser bool   `json:"is_superuser,omitempty"`
	IsVerified  bool   `json:"is_verified,omitempty"`
}

func (d *UserRegisterData) validateEmail() error {
	if d.Email == "" {
		return fmt.Errorf("Email is required")
	}

	query := `SELECT EXISTS(SELECT id FROM users WHERE email = $1)`
	var exists bool
	err := db.GetDB().QueryRow(query, d.Email).Scan(&exists)
	if err != nil {
		panic(err.Error())
	}

	fmt.Println(exists)
	if exists {
		return fmt.Errorf("Email is already taken")
	}
	return nil
}

func (d *UserRegisterData) Validate() error {
	if err := d.validateEmail(); err != nil {
		return err
	}
	if d.FirstName == "" {
		return fmt.Errorf("First name is required")
	}
	if d.LastName == "" {
		return fmt.Errorf("Last name is required")
	}
	if d.Password == "" {
		return fmt.Errorf("Password is required")
	}
	return nil
}

func (d *UserRegisterData) Save() (*User, error) {
	query := `
	INSERT INTO users (id, email, first_name, last_name, hashed_password, is_active, is_superuser, is_verified)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
	RETURNING id, email, first_name, last_name, is_active, is_superuser, is_verified`

	var user User
	err := db.GetDB().QueryRow(
		query, uuid.NewString(), d.Email, d.FirstName, d.LastName, d.Password, d.IsActive, d.IsSuperuser, d.IsVerified,
	).Scan(
		&user.ID, &user.Email, &user.FirstName, &user.LastName, &user.IsActive, &user.IsSuperuser, &user.IsVerified,
	)
	if err != nil {
		return nil, err
	}
	return &user, nil
}
