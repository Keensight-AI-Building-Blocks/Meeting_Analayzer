from __future__ import annotations as _annotations

import asyncio
from dataclasses import dataclass
from typing import Any
from dotenv import load_dotenv
from httpx import AsyncClient
from pydantic_ai import Agent, RunContext
import os


@dataclass
class Deps:
    client: AsyncClient  # For any API calls if needed
    transcript: str      # Raw transcript text


class SentimentAnalyzer:
    def __init__(self):
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        # Define the agent
        self.sentiment_agent = Agent(
            "gemini-1.5-flash",
            system_prompt=(
                "You are a sentiment analysis assistant for business meeting transcripts. "
                "Your job is to analyze the sentiment of the transcript and provide an overall tone "
                "(e.g., Positive, Neutral, or Negative). Provide a concise explanation for the rating."
            ),
            deps_type=Deps,
            retries=2,
        )
        self.register_tools()

    def register_tools(self):
        @self.sentiment_agent.tool
        def analyze_sentiment(ctx: RunContext[Deps]) -> dict[str, Any]:
            """Analyze the sentiment of the meeting transcript.

            Args:
                ctx: The context with dependencies.

            Returns:
                A dictionary containing the sentiment and an explanation.
            """
            transcript = ctx.deps.transcript
            # Dummy logic: analyze the sentiment based on keywords or tone
            positive_keywords = ["great", "good", "excellent", "agreed", "success"]
            negative_keywords = ["problem", "issue", "concern", "fail", "disagree"]

            positive_count = sum(1 for word in transcript.split() if word.lower() in positive_keywords)
            negative_count = sum(1 for word in transcript.split() if word.lower() in negative_keywords)

            if positive_count > negative_count:
                sentiment = "Positive"
                explanation = "The meeting had a positive tone with encouraging words like 'great' and 'success'."
            elif negative_count > positive_count:
                sentiment = "Negative"
                explanation = "The meeting highlighted several concerns or problems."
            else:
                sentiment = "Neutral"
                explanation = "The meeting had a balanced tone with no strong positive or negative sentiment."

            return {"sentiment": sentiment, "explanation": explanation}

    def save_data_in_file(self, filename: str, data: str) -> None:
        with open(filename, "w") as file:
            file.write(data)

    async def execute_agent(self, transcript: str):
        async with AsyncClient() as client:
            deps = Deps(client=client, transcript=transcript)
            prompt = f"Analyze the sentiment of the following meeting transcript: \n{transcript}"
            result = await self.sentiment_agent.run(prompt, deps=deps)
            print("Response:", result.data)
            self.save_data_in_file("outputs/SentimentResults.txt", result.data)

# Example usage
#print("Example usage:")
#asyncio.run(SentimentAnalyzer().execute_agent("The meeting was great and we had a successful discussion."))
