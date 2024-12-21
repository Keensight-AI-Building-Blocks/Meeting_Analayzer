import csv
import json
from pydantic_ai import Agent
from dotenv import load_dotenv
import os
from pydantic import ValidationError, BaseModel
import asyncio
from datetime import datetime
import re
from typing import List, Optional
from .schemas import DecisionExtractionSchema


class AnalyzerAgent:
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file. Please add it.")

    agent = Agent(
        "gemini-1.5-flash",
        system_prompt="""
You are a highly capable AI specializing in text analysis. Your task is to analyze the given text to highlight significant points and identify any decisions made. 

**Important**: 
1. Always respond with valid JSON only (no markdown). 
2. Your response **must** have the following structure exactly:

{
    "decisions": [],
    "highlights": []
}
"""
    )

    async def analyze_transcript(self):
        """
        Reads a JSON transcript from disk, runs it through the Agent,
        serializes the run result, and cleans the assistant's JSON response
        before returning.
        """
        try:
            file_path = "outputs/transcript.json"
            with open(file_path, "r") as file:
                transcript = json.load(file)

            # Convert transcript to string
            if isinstance(transcript, dict):
                transcript_text = json.dumps(transcript)
            else:
                transcript_text = str(transcript)
            
            # Get the RunResult from the Agent
            result = await self.agent.run(transcript_text)

            # Serialize the run result (useful for debugging or token usage tracking)
            serialized_result = self.serialize_run_result(result)

            # Extract the assistant’s final message
            assistant_response = result._all_messages[-1].content

            # Clean out any markdown fences or extraneous formatting
            cleaned_response = self.clean_json_response(assistant_response)

            # Convert the cleaned response to a Python dictionary
            try:
                final_json = json.loads(cleaned_response)
            except json.JSONDecodeError as decode_err:
                print("Warning: Could not parse assistant's JSON response:", decode_err)
                # Fall back to a default structure if parsing fails
                final_json = {
                    "decisions": [],
                    "highlights": []
                }


            try:
                validated_data = DecisionExtractionSchema(**final_json)
            except ValidationError as e:
                print("Schema validation error:", e)
                raise ValueError("Invalid data shape from AI response.") from e

            # Return validated data as a dict (which is guaranteed to match your schema)
            return {
                "analysis_result": validated_data.dict(),
            }

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {file_path}")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")
        except Exception as e:
            print(f"Error during analysis: {e}")
            return None

    def serialize_run_result(self, result):
        """
        Convert RunResult into a JSON-serializable dictionary.
        """
        return {
            "messages": [message.content for message in result._all_messages],
            "cost": {
                "request_tokens": result._cost.request_tokens,
                "response_tokens": result._cost.response_tokens,
                "total_tokens": result._cost.total_tokens,
            }
        }

    def clean_json_response(self, response: str) -> str:
        """
        Remove the '```json' at the beginning and '```' at the end.
        """
        cleaned_response = re.sub(r'^```json\s*', '', response.strip())
        cleaned_response = re.sub(r'```$', '', cleaned_response.strip())
        return cleaned_response

    async def main(self):
        """
        Main entry point to run the analysis and save the result.
        """
        result = await self.analyze_transcript()
        
        if result:
            analysis_json = result["analysis_result"]


            filename = "analysis_result.json"
            with open(filename, "w") as f:
                json.dump(analysis_json, f, indent=2)
            print(f"Analysis result saved to: {filename}")


        else:
            print("No result to save.")
