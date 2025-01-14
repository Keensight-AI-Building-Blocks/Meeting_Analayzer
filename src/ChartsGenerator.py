import json
from pydantic_ai import Agent
from dotenv import load_dotenv
import os
import asyncio
import re
import matplotlib.pyplot as plt


class ChartGeneratorAgent:
    def __init__(self):
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file. Please add it.")

        self.agent = Agent(
            "gemini-1.5-flash",
            system_prompt="""
Analyze the following transcript of a business meeting and identify any quantitative data or trends discussed. Based on the information extracted, propose possible charts that can be generated. For each chart, include the chart type, title, labels for the x and y axes (if applicable), and the data points.  

**Important**: 
1. Always respond with valid JSON only (no markdown).
2. The output should be structured as JSON and contain a list of charts with the following structure:

{
  "charts": [
    {
      "type": "line",
      "title": "Chart Title",
      "x_label": "X Axis Label",
      "y_label": "Y Axis Label",
      "data": {
        "x": ["X Data Points"],
        "y": ["Y Data Points"]
      }
    },
    {
      "type": "bar",
      "title": "Chart Title",
      "x_label": "X Axis Label",
      "y_label": "Y Axis Label",
      "data": {
        "x": ["X Data Points"],
        "y": ["Y Data Points"]
      }
    },
    {
      "type": "pie",
      "title": "Chart Title",
      "data": {
        "labels": ["Labels"],
        "values": ["Values"]
      }
    }
  ]
}
"""
        )

    async def analyze_transcript(self):
        file_path = "outputs/transcript.json"
        try:
            with open(file_path, "r") as file:
                transcript = json.load(file)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return None

        transcript_text = json.dumps(transcript) if isinstance(transcript, dict) else str(transcript)
        result = await self.agent.run(transcript_text)
        assistant_response = result._all_messages[-1].content
        cleaned_response = self.clean_json_response(assistant_response)
        #print("cleaned_response", cleaned_response)
        return cleaned_response

    def clean_json_response(self, response: str) -> str:
        """
        Remove the '```json' at the beginning and '```' at the end.
        """
        cleaned_response = re.sub(r'^```json\s*', '', response.strip())
        cleaned_response = re.sub(r'```$', '', cleaned_response.strip())
        return cleaned_response
    
    def DisplayCharts(self, datapath):
        with open(datapath, "r") as f:
            charts_data = json.load(f)
        for chart in charts_data['charts']:
            plt.figure()
            if chart['type'] == 'line':
                plt.plot(chart['data']['x'], chart['data']['y'])
                plt.title(chart['title'])
                plt.xlabel(chart['x_label'])
                plt.ylabel(chart['y_label'])
            elif chart['type'] == 'bar':
                plt.bar(chart['data']['x'], chart['data']['y'])
                plt.title(chart['title'])
                plt.xlabel(chart['x_label'])
                plt.ylabel(chart['y_label'])
            elif chart['type'] == 'pie':
                plt.pie(chart['data']['values'], labels=chart['data']['labels'], autopct='%1.1f%%')
                plt.title(chart['title'])
            plt.show()

    async def main(self):
        result = await self.analyze_transcript()
        if result:
            try:
                result_json = json.loads(result)  # Convert string back to JSON object
                filename = "outputs/charts_data_test.json"
                with open(filename, "w") as f:
                    json.dump(result_json, f, indent=2)
                print(f"Analysis result saved to: {filename}")
            except json.JSONDecodeError as e:
                print("Failed to decode JSON:", e)
        else:
            print("No result to save.")

        self.DisplayCharts('outputs/charts_data_test.json')


# To run the async function
if __name__ == "__main__":
    agent = ChartGeneratorAgent()
    asyncio.run(agent.main())
