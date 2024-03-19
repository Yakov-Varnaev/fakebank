swagger:
	swag init --parseInternal
run:
	make swagger && go run main.go
fmt:
	swag fmt
build:
	go build -ldflags "-s -w"
