package users

import (
	"database/sql"
	"fmt"
	"net/mail"

	"github.com/Yakov-Varnaev/fakebank/db"
	"golang.org/x/crypto/bcrypt"
)

func HashPassword(password string) (string, error) {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return "", err
	}
	return string(hash), nil
}

func VerifyPassword(hashedPassword, password string) error {
	return bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
}

type User struct {
	ID          string `json:"id,omitempty" db:"id"`
	FirstName   string `json:"first_name,omitempty" db:"first_name"`
	LastName    string `json:"last_name,omitempty" db:"last_name"`
	Email       string `json:"email,omitempty" db:"email"`
	IsActive    bool   `json:"is_active,omitempty" db:"is_active"`
	IsSuperuser bool   `json:"is_superuser,omitempty" db:"is_superuser"`
	IsVerified  bool   `json:"is_verified,omitempty" db:"is_verified"`
	Password    string `json:"-" db:"hashed_password"`
}

type UserRegisterData struct {
	Email     string `json:"email,omitempty"`
	FirstName string `json:"first_name,omitempty"`
	LastName  string `json:"last_name,omitempty"`
	Password  string `json:"password,omitempty"`
	IsActive  bool   `json:"_" db:"is_active"`
}

func (d *UserRegisterData) validateEmail() error {
	if d.Email == "" {
		return fmt.Errorf("Email is required")
	}
	_, err := mail.ParseAddress(d.Email)
	if err != nil {
		return fmt.Errorf("Invalid email")
	}

	query := `SELECT EXISTS(SELECT id FROM users WHERE email = LOWER($1))`
	var exists bool
	err = db.GetDB().QueryRow(query, d.Email).Scan(&exists)
	if err != nil {
		return err
	}

	if exists {
		return &EmailAlreadyExistsError{}
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
	var userDb UserDB
	user, err := userDb.Create(d)
	if err != nil {
		return nil, err
	}
	return user, nil
}

type UserLoginData struct {
	Email    string `json:"email,omitempty"`
	Password string `json:"password,omitempty"`
}

func (d *UserLoginData) Validate() error {
	if d.Email == "" {
		return fmt.Errorf("Email is required")
	}
	_, err := mail.ParseAddress(d.Email)
	if err != nil {
		return fmt.Errorf("Invalid email")
	}
	if d.Password == "" {
		return fmt.Errorf("Password is required")
	}
	return nil
}

func (d *UserLoginData) Authenticate() (*User, error) {
	var user User
	err := db.GetDB().QueryRow(
		`SELECT id, email, first_name, last_name, hashed_password, is_active, is_superuser, is_verified FROM users WHERE email = LOWER($1)`,
		d.Email,
	).Scan(&user.ID, &user.Email, &user.FirstName, &user.LastName, &user.Password, &user.IsActive, &user.IsSuperuser, &user.IsVerified)

	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("User not found")
	}

	err = VerifyPassword(user.Password, d.Password)
	if err != nil {
		return nil, fmt.Errorf("Invalid password")
	}

	return &user, nil
}
