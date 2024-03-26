package users

import (
	"database/sql"
	"fmt"
	"net/mail"

	"github.com/Yakov-Varnaev/fakebank/db"
	"github.com/doug-martin/goqu/v9"
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
	IsActive    bool   `json:"-" db:"is_active"`
	IsSuperuser bool   `json:"-" db:"is_superuser"`
	IsVerified  bool   `json:"-" db:"is_verified"`
	Password    string `json:"-" db:"hashed_password"`
}

type UserRegisterData struct {
	Email       string `json:"email,omitempty" db:"email"`
	FirstName   string `json:"first_name,omitempty" db:"first_name"`
	LastName    string `json:"last_name,omitempty" db:"last_name"`
	Password    string `json:"password,omitempty" db:"hashed_password"`
	IsActive    bool   `json:"-," db:"is_active"`
	IsSuperuser bool   `json:"-" db:"is_superuser"`
	IsVerified  bool   `json:"-" db:"is_verified"`
}

func (d *UserRegisterData) validateEmail() error {
	if d.Email == "" {
		return fmt.Errorf("Email is required")
	}
	_, err := mail.ParseAddress(d.Email)
	if err != nil {
		return fmt.Errorf("Invalid email")
	}

	exists, err := db.Exists("users", func(query *goqu.SelectDataset) *goqu.SelectDataset {
		return query.Where(goqu.C("email").ILike(d.Email))
	})
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
	user, err := db.GetByField[User]("users", "email", d.Email, nil)
	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("User not found")
	}
	err = VerifyPassword(user.Password, d.Password)
	if err != nil {
		return nil, fmt.Errorf("Invalid password")
	}

	return user, nil
}
