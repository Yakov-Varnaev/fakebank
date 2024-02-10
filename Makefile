migrations:
	@echo "Making migrations"
	# check if name is set
ifndef name
	@echo "Please set name=<name>"f
else
	alembic revision --autogenerate -m $(name)
endif

migrate:
	@echo "Migrating"
	alembic upgrade head


downgrade:
	@echo "Downgrading"
	alembic downgrade -1
