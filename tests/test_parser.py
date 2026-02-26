import pytest
from core.vision_parser import VideoAnalyzer
from api.schemas import BugReport

@pytest.mark.asyncio
async def test_vision_parser_structure():
    """
    Validates that the AI parser returns a strictly formatted BugReport object.
    """
    # Simulate an analysis job
    report = await VideoAnalyzer.extract_and_analyze("fake_video_path.mp4")
    
    # Assertions to prove 'highly structured reports' claim
    assert isinstance(report, BugReport)
    assert hasattr(report, "title")
    assert hasattr(report, "steps_to_reproduce")
    assert len(report.steps_to_reproduce) > 0
    assert report.severity in ["Critical", "High", "Medium", "Low"]

@pytest.mark.asyncio
async def test_report_engine_markdown_conversion():
    """
    Tests the ReportEngine's ability to convert AI models into JIRA templates.
    """
    from core.report_engine import ReportEngine
    
    mock_report = await VideoAnalyzer.extract_and_analyze("mock.mp4")
    markdown = ReportEngine.to_markdown(mock_report)
    
    assert "# [BUG]" in markdown
    assert "Steps to Reproduce" in markdown