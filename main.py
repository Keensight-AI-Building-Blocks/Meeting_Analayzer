import json
from src.schemas import UserInputSchema
from src.TranscriptAgent import TranscriptAgent
from src.AnalyzerAgent import AnalyzerAgent
import asyncio

# User input for requested output formats
requested_output_formats = ["transcript", "analyze"]

# PLACE .MP3 WEB URL OR LOCAL PATH
input_data = UserInputSchema(
    url="https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3",
    requested_output_formats=requested_output_formats
)

def transcribe():
    try:
        agent = TranscriptAgent()
        # Use a real audio URL for testing
        result = agent.transcribe_audio(input_data)
        # Save the transcription to a JSON file
        json_path = agent.save_to_json(result)
        print(f"Transcription saved to: {json_path}")
        return result
    except Exception as e:
        print("Error in transcription:", str(e))
        return None

async def analyze():
    try:
        agent = AnalyzerAgent()
        result = await agent.analyze_transcript()
        if result:
            filename = 'outputs/analysis_results.json'
            with open(filename, 'w') as f:
                json.dump(result, f)
            print(f"Analysis results saved to: {filename}")
    except Exception as e:
        print("Error in analysis:", str(e))

if __name__ == '__main__':
    if "transcript" in requested_output_formats:
        print("Transcribing....")
        transcription_result = transcribe()
    
    if "analyze" in requested_output_formats:
        print("Analyzing....")
        asyncio.run(analyze())
