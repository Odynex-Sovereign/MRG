import pytest
from datetime import datetime
from app.database.models import DBMeteredUsage
from app.services.export_engine import usage_export_engine

def test_csv_string_generation_logic():
    """
    Validates that the export engine formats metric parameters 
    into correct comma-delimited structural elements.
    """
    # 1. Arrange a mock collection of raw database entries
    mock_logs = [
        DBMeteredUsage(
            id=1,
            tenant_id="test_corp_77",
            session_id="sim_x92a1",
            simulation_minutes=2.5,
            deepseek_tokens=3200,
            riva_audio_seconds=150.0,
            timestamp=datetime(2026, 11, 7, 12, 0, 0)
        ),
        DBMeteredUsage(
            id=2,
            tenant_id="test_corp_77",
            session_id="sim_y83b2",
            simulation_minutes=0.75,
            deepseek_tokens=900,
            riva_audio_seconds=45.0,
            timestamp=datetime(2026, 11, 7, 12, 15, 0)
        )
    ]
    
    # 2. Act: Generate the CSV stream string layout
    csv_output = usage_export_engine.generate_csv_report(mock_logs)
    
    # 3. Assert: Verify components match structural requirements
    assert "Record ID,Tenant ID,Session ID" in csv_output
    assert "test_corp_77,sim_x92a1,2.5,3200,150.0" in csv_output
    assert "test_corp_77,sim_y83b2,0.75,900,45.0" in csv_output
    
    # Confirm appropriate row generation splitting
    lines = [line for line in csv_output.split("\r\n") if line]
    assert len(lines) == 3 # Header row + 2 data rows
