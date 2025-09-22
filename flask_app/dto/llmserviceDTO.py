







from pydantic import BaseModel, Field
class KorRelation(BaseModel):
            related:bool = Field(description="Whether if the text is related to the Korean history")
            unsure:bool = Field(description="If you are not sure about it, mark as true")