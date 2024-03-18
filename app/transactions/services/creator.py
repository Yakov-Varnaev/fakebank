from app.core.service import BaseService
from app.transactions.kafka.producers import TransactionProducer
from app.transactions.schemas import (TransactionCreateSchema,
                                      TransactionReadSchema)
from app.transactions.services.performer import TransactionPerformer
from app.users.models import User


class TransactionCreator(BaseService[TransactionReadSchema]):
    def __init__(
        self,
        user: User,
        data: TransactionCreateSchema,
        transaction_producer: TransactionProducer | None = None,
    ):
        self.user = user
        self.data = data
        self.producer = transaction_producer

    async def act(self) -> TransactionReadSchema:
        performer = TransactionPerformer(self.db, self.producer)
        transaction = await performer(self.user.id, self.data)
        return TransactionReadSchema.model_validate(transaction)
