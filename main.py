import json
from src.schemas import UserInputSchema
from src.TranscriptAgent import TranscriptAgent
from src.AnalyzerAgent import AnalyzerAgent
from src.SentimentAnalysis import SentimentAnalyzer
from src.ChartsGenerator import ChartGeneratorAgent
import asyncio

# User input for requested output formats
requested_output_formats = ["transcript"] # you can use ["transcript", "analyze", "sentiment","charts"]
url="src/audio/dsMeeting.mp3"
#url="https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3",


input_data = UserInputSchema(
    url=url,
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

async def analyzeMeeting():
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

async def GenerateCharts():
    try:
        agent = ChartGeneratorAgent()
        result = await agent.analyze_transcript()
        if result:
            result_json = json.loads(result)
            filename = 'outputs/charts_data.json'
            with open(filename, 'w') as f:
                json.dump(result_json, f, indent=2)
            print(f"charts data results saved to: {filename}")
            agent.DisplayCharts(filename)
    except Exception as e:
        print("Error in analysis:", str(e))

async def analyzeSentimentsMeeting():
    try:
        agent = SentimentAnalyzer()
        with open("outputs/transcript.json", 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            Transcript = json.dumps(data, indent=4)  # Convert JSON object to a pretty-printed string

        result = await agent.execute_agent(Transcript)
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
        asyncio.run(analyzeMeeting())

    if "charts" in requested_output_formats:
        print("generating charts....")
        asyncio.run(GenerateCharts())
    
    if "sentiment" in requested_output_formats:
        print("Analyzing Sentiments....")
        asyncio.run(analyzeSentimentsMeeting())
