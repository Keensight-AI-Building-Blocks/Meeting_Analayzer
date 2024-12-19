from pydantic import BaseModel, HttpUrl
from typing import List, Optional

# Input schema for user-provided data
class UserInputSchema(BaseModel):
    url: HttpUrl
    requested_output_formats: List[str]  # e.g., ["transcript", "decisions", "graphs"]

# Data schema for transcription output
class TranscriptionSchema(BaseModel):
    transcript: str
    confidence_score: Optional[float]  # Confidence level of the transcription process
    timestamps: Optional[List[dict]]  # e.g., [{"start": 0.0, "end": 2.5, "text": "Hello world"}]


# Data schema for decision extraction output
class DecisionExtractionSchema(BaseModel):
    decisions: List[str]  # List of decisions extracted
    highlights: Optional[List[str]]  # Key phrases or highlights from the discussion

# Data schema for graph generation output
class GraphDataSchema(BaseModel):
    graphs: List[dict]  # e.g., [{"type": "bar", "data": {...}, "title": "Revenue Analysis"}]
