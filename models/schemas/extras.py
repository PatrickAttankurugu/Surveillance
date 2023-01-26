from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    message: str = Field(
        ...,
        title="Message",
        description="The success message"
    )