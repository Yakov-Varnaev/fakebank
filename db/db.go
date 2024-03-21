package db

import (
	"database/sql"
	"log"

	pagination "github.com/Yakov-Varnaev/fakebank/utils"
	"github.com/doug-martin/goqu/v9"
	_ "github.com/doug-martin/goqu/v9/dialect/postgres"
	_ "github.com/lib/pq"
)

var db *goqu.Database

func Init() {
	// TODO: move to env
	connStr := "postgres://fakebank:fakebank@localhost:5432/test?sslmode=disable"
	dialect := goqu.Dialect("postgres")
	pgdb, err := sql.Open("postgres", connStr)
	db = dialect.DB(pgdb)
	if err != nil {
		log.Fatal(err)
	}
}

func GetDB() *goqu.Database {
	return db
}

type DBObject interface{}

type DB struct {
	Table string
}

func Create[CreateData DBObject, ReturnData any](table string, data CreateData) (*ReturnData, error) {
	var result ReturnData
	_, err := db.Insert(table).Rows(data).Returning(&result).Executor().ScanStruct(&result)
	if err != nil {
		return nil, err
	}
	return &result, nil
}

func List[ReturnData DBObject](table string, paginationParams *pagination.Params) (*pagination.Page[ReturnData], error) {
	var result []ReturnData
	query := db.From(table)
	total, err := query.Count()
	if err != nil {
		return nil, err
	}
	query = paginationParams.Paginate(query)
	err = query.ScanStructs(&result)
	if err != nil {
		return nil, err
	}
	return &pagination.Page[ReturnData]{Data: result, Total: total}, nil
}
