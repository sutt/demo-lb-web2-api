from typing import Any

from pydantic import BaseModel, Field


class CreateInvoiceSchema(BaseModel):
    amount: int
    memo: str