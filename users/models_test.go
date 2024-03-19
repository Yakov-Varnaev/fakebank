package users

import (
	"testing"

	"github.com/Yakov-Varnaev/fakebank/db"
)

const email = "existing@test.com"

func TestMain(m *testing.M) {
	db.Init()
	userData := UserRegisterData{
		Email:     email,
		FirstName: "John",
		LastName:  "Doe",
		Password:  "password",
	}
	_, err := userData.Save()
	if err != nil {
		panic(err)
	}
	m.Run()
	db.GetDB().Query("DELETE FROM users")
}

func TestUserRegisterData_Validate(t *testing.T) {
	type fields struct {
		Email     string
		FirstName string
		LastName  string
		Password  string
	}
	tests := []struct {
		name          string
		fields        fields
		wantErr       bool
		expectedError string
	}{
		{
			name: "Empty email",
			fields: fields{
				Email:     "",
				FirstName: "John",
				LastName:  "Doe",
				Password:  "password",
			},
			wantErr:       true,
			expectedError: "Email is required",
		},
		{
			name: "Empty first name",
			fields: fields{
				Email:     "test@test.com",
				FirstName: "",
				LastName:  "Doe",
				Password:  "password",
			},
			wantErr:       true,
			expectedError: "First name is required",
		},
		{
			name: "Empty last name",
			fields: fields{
				Email:     "test@test.com",
				FirstName: "John",
				LastName:  "",
				Password:  "password",
			},
			wantErr:       true,
			expectedError: "Last name is required",
		},
		{
			name: "Empty password",
			fields: fields{
				Email:     "test@test.com",
				FirstName: "John",
				LastName:  "Doe",
				Password:  "",
			},
			wantErr:       true,
			expectedError: "Password is required",
		},
		{
			name: "Email already taken",
			fields: fields{
				Email:     email,
				FirstName: "John",
				LastName:  "Doe",
				Password:  "password",
			},
			wantErr:       true,
			expectedError: "Email is already taken",
		},
		{
			name: "Valid data",
			fields: fields{
				Email:     "test@test.com",
				FirstName: "John",
				LastName:  "Doe",
				Password:  "password",
			},
			wantErr: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			d := &UserRegisterData{
				Email:     tt.fields.Email,
				FirstName: tt.fields.FirstName,
				LastName:  tt.fields.LastName,
				Password:  tt.fields.Password,
			}
			if err := d.Validate(); (err != nil) != tt.wantErr {
				t.Errorf("UserRegisterData.Validate() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}
