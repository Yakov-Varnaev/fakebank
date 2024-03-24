package db

import (
	"database/sql"
	"fmt"
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

func Create[CreateData DBObject, ReturnData any](table string, data CreateData) (*ReturnData, error) {
	var result ReturnData
	query := db.Insert(table).Rows(data).Returning(&result)
	sql, _, _ := query.ToSQL()
	fmt.Println(sql)
	_, err := db.Insert(table).Rows(data).Returning(&result).Executor().ScanStruct(&result)
	if err != nil {
		return nil, err
	}
	return &result, nil
}

type QueryProcessFunc func(query *goqu.SelectDataset) *goqu.SelectDataset

func List[ReturnData DBObject](
	table string,
	paginationParams *pagination.Params,
	filterFunc QueryProcessFunc,
) (*pagination.Page[ReturnData], error) {
	var result []ReturnData
	query := db.From(table)
	query = filterFunc(query)
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

func GetByID[ReturnData DBObject](table string, id string) (*ReturnData, error) {
	var result ReturnData
	found, err := db.From(table).Where(goqu.C("id").Eq(id)).ScanStruct(&result)
	if err != nil {
		return nil, err
	}
	if !found {
		return nil, nil
	}
	return &result, nil
}

func Exists(table string, queryProcessFunc QueryProcessFunc) (bool, error) {
	query := db.From(table)
	query = queryProcessFunc(query)
	cnt, err := query.Count() // There is no exists method in goqu
	if err != nil {
		return false, err
	}
	return cnt > 0, nil
}

func Update[UpdateData DBObject, ReturnData any](table string, id string, data UpdateData) (*ReturnData, error) {
	var result ReturnData
	_, err := db.Update(table).Set(data).Where(goqu.C("id").Eq(id)).Returning(&result).Executor().ScanStruct(&result)
	if err != nil {
		return nil, err
	}
	return &result, nil
}
