from pydantic import UUID4, BaseModel, ConfigDict


class NotificationCreateSchema(BaseModel):
    kind: str
    message: str
    extra: dict | None = None


class NotificationSchema(NotificationCreateSchema):
    id: UUID4
    user_id: UUID4

    model_config = ConfigDict(from_attributes=True)
