# app
run:
	poetry run uvicorn app.main:app --reload

# database
migrations:
	@echo "Making migrations"
	# check if name is set
ifndef name
	@echo "Please set name=<name>"f
else
	poetry run alembic revision --autogenerate -m $(name)
endif

migrate:
	@echo "Migrating"
	poetry run alembic upgrade head

downgrade:
	@echo "Downgrading"
	poetry run alembic downgrade -1

transaction_consumer:
	poetry run python app/main.py --name=transactions
