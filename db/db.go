package db

import (
	"database/sql"
	"log"

	"github.com/doug-martin/goqu/v9"
	_ "github.com/doug-martin/goqu/v9/dialect/postgres"
	_ "github.com/lib/pq"
)

var db *goqu.Database

func Init() {
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
