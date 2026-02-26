from pydantic import BaseModel, Field
from typing import List, Optional

class BugReport(BaseModel):
    title: str = Field(..., description="Technical title for the bug.")
    severity: str = Field(..., description="Critical, High, Medium, or Low")
    description: str = Field(..., description="Detailed summary of the issue.")
    steps_to_reproduce: List[str] = Field(..., description="Step-by-step actions.")
    expected_behavior: str = Field(..., description="Intended functionality.")
    actual_behavior: str = Field(..., description="What actually happened in the video.")
    suggested_fix: Optional[str] = Field(None, description="AI-generated root cause hypothesis.")

class UploadResponse(BaseModel):
    status: str
    filename: str
    message: str
    report: Optional[BugReport] = None