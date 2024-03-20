package users

import (
	"database/sql"
	"fmt"
	"net/mail"
	"strings"

	"github.com/Yakov-Varnaev/fakebank/db"
	"github.com/google/uuid"
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
	ID          string `json:"id"`
	FirstName   string `json:"first_name"`
	LastName    string `json:"last_name"`
	Email       string `json:"email"`
	IsActive    bool   `json:"is_active"`
	IsSuperuser bool   `json:"is_superuser"`
	IsVerified  bool   `json:"is_verified"`
	Password    string `json:"-"`
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
	_, err := mail.ParseAddress(d.Email)
	if err != nil {
		return fmt.Errorf("Invalid email")
	}

	query := `SELECT EXISTS(SELECT id FROM users WHERE email = LOWER($1))`
	var exists bool
	err = db.GetDB().QueryRow(query, d.Email).Scan(&exists)
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
	RETURNING id, email, first_name, last_name, hashed_password, is_active, is_superuser, is_verified`

	hashedPassword, err := HashPassword(d.Password)
	if err != nil {
		return nil, err
	}
	var user User
	err = db.GetDB().QueryRow(
		query, uuid.NewString(), strings.ToLower(d.Email), d.FirstName, d.LastName, hashedPassword, d.IsActive, d.IsSuperuser, d.IsVerified,
	).Scan(
		&user.ID, &user.Email, &user.FirstName, &user.LastName, &user.Password, &user.IsActive, &user.IsSuperuser, &user.IsVerified,
	)
	if err != nil {
		return nil, err
	}
	return &user, nil
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

var session_store = make(map[string]*User)

func CreateCookies(user *User) (string, error) {
	accessToken, err := uuid.NewRandom()
	if err != nil {
		return "", err
	}

	stringToken := accessToken.String()
	session_store[stringToken] = user

	return stringToken, nil
}
