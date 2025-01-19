from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union

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
class PieChartData(BaseModel):
    labels: List[str]
    values: List[Union[int, float]]

class BarChartData(BaseModel):
    x: List[str]
    y: List[Union[int, float]]

class LineChartData(BaseModel):
    x: List[str]
    y: Optional[List[Union[int, float]]] = None
    y_cac: Optional[List[Union[int, float]]] = None
    y_clv: Optional[List[Union[int, float]]] = None

class Chart(BaseModel):
    type: str
    title: str
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    data: Union[PieChartData, BarChartData, LineChartData]

class ResponseModel(BaseModel):
    charts: List[Chart]