package transactions

import (
	"time"

	"github.com/shopspring/decimal"
)

type TransactionStatus string

const (
	StatusPending  TransactionStatus = "pending"
	StatusComplete TransactionStatus = "done"
	StatusFailed   TransactionStatus = "failed"
)

type TransactionCreateData struct {
	SenderID    string          `json:"sender_id,omitempty" db:"sender"`
	RecipientID string          `json:"recipient_id,omitempty" db:"recipient"`
	Amount      decimal.Decimal `json:"amount,omitempty" db:"amount"`
}

type TransactionCreate struct {
	SenderID    string            `db:"sender"`
	RecipientID string            `db:"recipient"`
	Amount      decimal.Decimal   `db:"amount"`
	Status      TransactionStatus `db:"status"`
	Time        time.Time         `db:"time"`
}

type Transaction struct {
	ID          string          `json:"id,omitempty" db:"id"`
	SenderID    string          `json:"sender_id,omitempty" db:"sender"`
	RecipientID string          `json:"recipient_id,omitempty" db:"recipient"`
	Status      string          `json:"status,omitempty" db:"status"`
	Amount      decimal.Decimal `json:"amount,omitempty" db:"amount"`
	Time        time.Time       `json:"time,omitempty" db:"time"`
}
