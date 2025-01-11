from pydantic import BaseModel, HttpUrl
from typing import List, Optional

# Input schema for user-provided data
class UserInputSchema(BaseModel):
    #url: HttpUrl
    url: str
    requested_output_formats: List[str]  # e.g., ["transcript", "decisions", "graphs"]

# Data schema for transcription output
class TranscriptionSchema(BaseModel):
    transcript: str
    confidence_score: Optional[float]  # Confidence level of the transcription process


# Data schema for decision extraction output
class DecisionExtractionSchema(BaseModel):
    decisions: List[str] = []
    highlights: Optional[List[str]] = []
    accomplishments: Optional[List[str]] = []
    todos: Optional[List[str]] = []
    further: Optional[List[str]] = []

    

# Data schema for graph generation output
class GraphDataSchema(BaseModel):
    graphs: List[dict]  # e.g., [{"type": "bar", "data": {...}, "title": "Revenue Analysis"}]
