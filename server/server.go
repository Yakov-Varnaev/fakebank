package server

import "github.com/Yakov-Varnaev/fakebank/db"

func Init() {
	db.Init()
	r := NewRouter()

	r.Run(":8000")
}
