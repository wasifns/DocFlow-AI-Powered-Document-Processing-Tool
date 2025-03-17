from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv

load_dotenv()

model_id = "gemini-2.0-flash"
agent = Agent(
    model=Gemini(id=model_id),
    markdown=True,
)
