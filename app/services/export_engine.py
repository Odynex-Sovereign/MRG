import csv
import io
from typing import List
from app.database.models import DBMeteredUsage

class UsageExportEngine:
    def generate_csv_report(self, entries: List[DBMeteredUsage]) -> str:
        """
        Aggregates operational database entities and formats them 
        into a clean, paste-ready, standard CSV data stream.
        """
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
        # Write structural header baseline
        writer.writerow([
            "Record ID", 
            "Tenant ID", 
            "Session ID", 
            "Compute Duration (Min)", 
            "DeepSeek Token Drain", 
            "Riva Stream Duration (Sec)", 
            "Timestamp UTC"
        ])
        
        # Parse out database rows sequentially
        for entry in entries:
            writer.writerow([
                entry.id,
                entry.tenant_id,
                entry.session_id,
                entry.simulation_minutes,
                entry.deepseek_tokens,
                entry.riva_audio_seconds,
                entry.timestamp.isoformat() if entry.timestamp else "N/A"
            ])
            
        return output.getvalue()

usage_export_engine = UsageExportEngine()
