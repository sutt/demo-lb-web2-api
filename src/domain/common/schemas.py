import uuid
import datetime
from typing import TypeVar, Any

from pydantic import BaseModel, ConfigDict, Extra, model_validator

Model = TypeVar('Model', bound='BaseModel')


class DomainSchema(BaseModel):
    model_config = ConfigDict(
        extra=Extra.ignore, from_attributes=True, use_enum_values=True, frozen=True
    )

    @classmethod
    def model_validate_or_none(cls: type[Model], obj: Any) -> Model | None:
        if obj is not None:
            return cls.model_validate(obj)
        return None


class IdentifiableSchema(DomainSchema):

    id: uuid.UUID


class CreatedAtField(DomainSchema):
    created_at: datetime.datetime


class ModifiedAtField(DomainSchema):
    modified_at: datetime.datetime


class TimestampedSchema(CreatedAtField, ModifiedAtField):
    pass


class UpdateRequestSchema(DomainSchema):
    @model_validator(mode="after")
    def check_if_not_all_fields_are_none(self) -> "UpdateRequestSchema":
        if self.model_dump(exclude_unset=True) == {}:
            msg = "At least one updatable field has to be passed."
            raise ValueError(msg)
        return self
