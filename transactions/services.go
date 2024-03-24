package transactions

import (
	"fmt"
	"time"

	"github.com/Yakov-Varnaev/fakebank/accounts"
	"github.com/Yakov-Varnaev/fakebank/db"
	"github.com/Yakov-Varnaev/fakebank/users"
	"github.com/gin-gonic/gin"
	// "github.com/google/uuid"
)

type CreateService struct {
	Data *TransactionCreateData
	User *users.User
}

func (service *CreateService) FromContext(c *gin.Context) error {
	var data TransactionCreateData
	err := c.ShouldBindJSON(&data)
	if err != nil {
		return err
	}
	service.Data = &data
	service.User = c.MustGet("user").(*users.User)
	return nil
}

func (service *CreateService) Act() (*Transaction, error) {
	tx, err := db.GetDB().Begin()
	if err != nil {
		return nil, err
	}
	fmt.Println("Transaction started")
	defer tx.Rollback()

	// var result *Transaction
	err = tx.Wrap(func() error {
		sender_account, err := db.GetByID[accounts.Account]("account", service.Data.SenderID)
		if err != nil {
			return err
		}
		fmt.Println("Sender account found", sender_account.ID, sender_account.Name)

		if sender_account.UserID != service.User.ID {
			return err
		}

		recipient_account, err := db.GetByID[accounts.Account]("account", service.Data.RecipientID)
		if err != nil {
			return err
		}
		fmt.Println("Recipient account found", recipient_account.ID, recipient_account.Name)

		return nil
	})
	if err != nil {
		return nil, err
	}

	createData := TransactionCreate{
		SenderID:    service.Data.SenderID,
		RecipientID: service.Data.RecipientID,
		Amount:      service.Data.Amount,
		Status:      StatusPending,
		Time:        time.Now(),
	}
	result, err := db.Create[TransactionCreate, Transaction]("transaction", createData)
	if err != nil {
		fmt.Println("Error creating transaction", err.Error())
		return nil, err
	}
	fmt.Println("Transaction created", result.ID, result.Amount)

	return nil, nil
}
