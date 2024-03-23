package accounts

import (
	"fmt"

	"github.com/shopspring/decimal"
)

type Account struct {
	ID      string          `json:"id,omitempty" db:"id,omitempty"`
	Name    string          `json:"name,omitempty" db:"name,omitempty"`
	Balance decimal.Decimal `json:"balance,omitempty" db:"balance,omitempty"`
	UserID  string          `json:"user_id,omitempty" db:"user_id,omitempty"`
}

type AccountCreate struct {
	Name string `json:"name" db:"name"`
}

func (a *AccountCreate) Validate() error {
	if a.Name == "" {
		return fmt.Errorf("Name is required")
	}
	return nil
}

type AccountCreateData struct {
	AccountCreate
	UserID string `db:"user_id"`
}

func (a AccountCreateData) Table() string {
	return "account"
}
