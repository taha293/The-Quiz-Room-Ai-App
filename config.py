from agents import AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig,ModelSettings
from dotenv import load_dotenv
import os

load_dotenv()
Gemini_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=Gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

external_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

rununer_config = RunConfig(
    model=external_model,
    model_provider=external_client,
    model_settings=ModelSettings(
        temperature=0.8
    )
)
