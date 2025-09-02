from openai import OpenAI
import os
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def openai_stuctured_request(
        self,
        messages: list[dict[str, str]],
        response_format: BaseModel,
        model: Literal["gpt-4.1-mini"] = "gpt-4.1-mini",
    ):
        
        response = self.client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=response_format
        )

        result = response.choices[0].message.parsed
        return result.model_dump()
    