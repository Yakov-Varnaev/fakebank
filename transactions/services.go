package transactions

import (
	"fmt"
	"time"

	"github.com/Yakov-Varnaev/fakebank/accounts"
	"github.com/Yakov-Varnaev/fakebank/db"
	"github.com/Yakov-Varnaev/fakebank/users"
	pagination "github.com/Yakov-Varnaev/fakebank/utils"
	"github.com/doug-martin/goqu/v9"
	"github.com/gin-gonic/gin"
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
		sender_account, err := db.GetByID[accounts.Account]("account", service.Data.SenderID, nil)
		if err != nil {
			return err
		}
		fmt.Println("Sender account found", sender_account.ID, sender_account.Name)

		if sender_account.UserID != service.User.ID {
			return err
		}

		recipient_account, err := db.GetByID[accounts.Account]("account", service.Data.RecipientID, nil)
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
	// This have to be inside the transaction
	result, err := db.Create[TransactionCreate, Transaction]("transaction", createData)
	if err != nil {
		fmt.Println("Error creating transaction", err.Error())
		return nil, err
	}
	fmt.Println("Transaction created", result.ID, result.Amount)

	transaction, err := db.GetByID[Transaction]("transaction", result.ID, nil)
	if err != nil {
		return nil, err
	}
	return transaction, nil
}

type ListService struct {
	User       *users.User
	Pagination *pagination.Params
}

func (service *ListService) FromContext(c *gin.Context) error {
	var err error
	service.User = c.MustGet("user").(*users.User)
	service.Pagination, err = pagination.FromContext(c)
	return err
}

func (service ListService) Process(query *goqu.SelectDataset) *goqu.SelectDataset {
	query = (query.
		Join(goqu.T("account").As("sender_account"), goqu.On(goqu.I("sender").Eq(goqu.I("sender_acount.id")))).
		Join(goqu.T("account").As("recipient_account"), goqu.On(goqu.I("recipient").Eq(goqu.I("recipient_account.id")))).
		Join(goqu.T("user").As("recipient_user"), goqu.On(goqu.I("recipient_account.user_id").Eq(goqu.I("recipient_user.id")))).
		Join(goqu.T("user").As("sender_user"), goqu.On(goqu.I("sender_account.user_id").Eq(goqu.I("sender_user.id")))))

	return query
}

func (service *ListService) Act() (*pagination.Page[Transaction], error) {}
