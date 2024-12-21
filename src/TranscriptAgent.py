import assemblyai as aai
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from .schemas import TranscriptionSchema, UserInputSchema
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

                # Prepare data
                data = ""
                if hasattr(transcript, 'utterances') and transcript.utterances:
                    for utterance in transcript.utterances:
                        data += f"Speaker {utterance.speaker}: " + utterance.text

                # Create output using schema
                output = TranscriptionSchema(
                    transcript=data,
                    confidence_score=getattr(transcript, 'confidence', 0.0),
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

    def save_to_json(self, transcription: TranscriptionSchema, output_dir: str = "outputs") -> str:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"transcript.json"
        filepath = os.path.join(output_dir, filename)
        
        # Save to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(transcription.dict(), f, indent=4, ensure_ascii=False)
            
        return filepath

