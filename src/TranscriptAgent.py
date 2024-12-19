import assemblyai as aai
from dotenv import load_dotenv
import os
from typing import Dict, List
from schemas import TranscriptionSchema, UserInputSchema
from pydantic import ValidationError

class TranscriptAgent:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Set up API key
        AAI_API_KEY = os.getenv("AAI_API_KEY")
        if not AAI_API_KEY:
            raise ValueError("AAI_API_KEY not found in environment variables")
        aai.settings.api_key = AAI_API_KEY

    def transcribe_audio(self, input_data: UserInputSchema) -> TranscriptionSchema:
        try:
            # Validate input using schema
            validated_input = UserInputSchema(
                url=input_data.url,
                requested_output_formats=input_data.requested_output_formats
            )

            # Configure transcription settings
            config = aai.TranscriptionConfig(
                speaker_labels=True,
            )

            # Create transcriber
            transcriber = aai.Transcriber()
            
            try:
                # Perform transcription
                transcript = transcriber.transcribe(str(validated_input.url), config)
                
                if not transcript or not hasattr(transcript, 'text'):
                    raise ValueError("Transcription failed: No transcript returned")

                # Prepare timestamps
                timestamps = []
                if hasattr(transcript, 'utterances') and transcript.utterances:
                    for utterance in transcript.utterances:
                        timestamps.append({
                            "start": utterance.start,
                            "end": utterance.end,
                            "text": utterance.text,
                            "speaker": f"Speaker {utterance.speaker}"
                        })

                # Create output using schema
                output = TranscriptionSchema(
                    transcript=transcript.text,
                    confidence_score=getattr(transcript, 'confidence', 0.0),
                    timestamps=timestamps
                )

                return output

            except aai.exceptions.AuthorizationError:
                raise ValueError("Invalid AssemblyAI API key")
            except aai.exceptions.RequestError as e:
                raise ValueError(f"AssemblyAI request error: {str(e)}")

        except ValidationError as e:
            raise ValueError(f"Input validation error: {str(e)}")
        except Exception as e:
            raise Exception(f"Transcription error: {str(e)}")


if __name__ == "__main__":
    # Example usage
    try:
        agent = TranscriptAgent()
        # Use a real audio URL for testing
        input_data = UserInputSchema(
            url="https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3",
            requested_output_formats=["transcript"]
        )
        result = agent.transcribe_audio(input_data)
        print("Transcription result:", result.dict())
    except Exception as e:
        print("Error:", str(e))
