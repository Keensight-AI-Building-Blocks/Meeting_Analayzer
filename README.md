# Meeting Analyzer

This script analyzes recorded business meetings.

## Overview
The Meeting Analyzer is a Python-based application designed to analyze text transcripts from meetings. It utilizes an AI agent to highlight significant points and identify decisions made during discussions.

## Key Features
- Reads JSON transcripts from disk.
- Analyzes text using the Gemini AI agent and returns structured JSON responses.
- Serializes and cleans the AI's output for easier handling.
- Saves analysis results to a JSON file.

## Dependencies
- `pydantic_ai`: For AI agent functionality.
- `python-dotenv`: To load environment variables from a `.env` file.
- `asyncio`: For asynchronous operations.
- `pydantic`: For data validation.

## Usage
1. Ensure that you have the required dependencies installed.
2. Set up your `.env` file with the necessary API keys.
3. Run the `main.py` script to start the analysis.

## Schemas

### UserInputSchema
- **url**: A valid URL.
- **requested_output_formats**: A list of output formats requested by the user (e.g., transcript, decisions, graphs).

### TranscriptionSchema
- **transcript**: The transcribed text.
- **confidence_score**: An optional score indicating the confidence level of the transcription.

### DecisionExtractionSchema
- **decisions**: A list of decisions made during the meeting.
- **highlights**: Optional highlights from the meeting.

### GraphDataSchema
- **graphs**: A list of graph data in dictionary format.

## License
This project is licensed under the MIT License.
