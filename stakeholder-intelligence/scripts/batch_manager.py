#!/usr/bin/env python3
"""
Batch Manager for PSI System
Handles batch tracking and activity logging
"""

import os
import re
from datetime import datetime
from pathlib import Path
import logging

class BatchManager:
    """Manages batch processing and tracking"""
    
    def __init__(self):
        self.logger = logging.getLogger('BatchManager')
        self.base_path = Path(__file__).parent.parent
        self.activity_ledger_path = self.base_path / 'activity_ledger.md'
        self.batch_tracker_path = self.base_path / 'batch_tracker.md'
    
    def create_batch(self) -> str:
        """Create a new batch ID and initialize tracking"""
        # Generate batch ID
        timestamp = datetime.now()
        date_str = timestamp.strftime('%Y-%m-%d')
        
        # Find next sequence number for today
        seq_num = self.get_next_sequence_number(date_str)
        batch_id = f"PSI-{date_str}-{seq_num:03d}"
        
        # Log to activity ledger
        self.log_activity(
            activity=f"Batch {batch_id} created",
            details=f"Processing initiated",
            status="Started"
        )
        
        # Initialize batch in tracker
        self.initialize_batch_tracking(batch_id)
        
        self.logger.info(f"Created batch: {batch_id}")
        return batch_id
    
    def get_next_sequence_number(self, date_str: str) -> int:
        """Get the next sequence number for a given date"""
        if not self.batch_tracker_path.exists():
            return 1
        
        content = self.batch_tracker_path.read_text()
        
        # Count existing batches for this date
        count = content.count(f"PSI-{date_str}-")
        return count + 1
    
    def log_activity(self, activity: str, details: str, status: str, user: str = None):
        """Append entry to activity ledger"""
        if user is None:
            user = os.environ.get('USER', 'System')
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        version = "v1.0"
        
        entry = f"| {timestamp} | {version} | {activity} | {user} | {details} | {status} |\n"
        
        # Append to ledger
        with open(self.activity_ledger_path, 'a') as f:
            f.write(entry)
    
    def initialize_batch_tracking(self, batch_id: str):
        """Initialize batch tracking entry"""
        template = f"""
### Batch ID: {batch_id}
- **Version**: v1.0
- **Status**: In Progress
- **Start Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **End Time**: TBD
- **Operator**: {os.environ.get('USER', 'System')}
- **Prospects Targeted**: TBD
- **Configuration**: 
  - Campaigns: M&A Due Diligence, Ransomware
  - Enrichment: Enabled
  - Parallel Agents: 8

#### Task Checklist:
- [x] Environment verification complete
- [x] MCP services verified
- [x] Prospect folders accessible
- [x] Batch initialized
- [ ] Extraction phase started
- [ ] Extraction phase completed
- [ ] Enrichment phase started
- [ ] Enrichment phase completed
- [ ] Scoring phase started
- [ ] Scoring phase completed
- [ ] Output generation started
- [ ] Output validation complete
- [ ] Files delivered to outputs/
- [ ] Activity ledger updated
- [ ] Stakeholders notified

#### Metrics:
- Prospects Processed: 0/TBD
- Personas Extracted: 0
- Enrichment Success Rate: 0%
- Processing Time: 0 minutes
- Errors Encountered: 0
- Data Quality Score: 0%

#### Notes:
- Processing started

---
"""
        
        # Find the right place to insert (before "## Completed Batches")
        if self.batch_tracker_path.exists():
            content = self.batch_tracker_path.read_text()
            
            # Find insertion point
            insert_marker = "## Completed Batches"
            if insert_marker in content:
                parts = content.split(insert_marker)
                new_content = parts[0].rstrip() + "\n" + template + "\n" + insert_marker + parts[1]
            else:
                new_content = content + template
            
            self.batch_tracker_path.write_text(new_content)
        else:
            self.batch_tracker_path.write_text(template)
    
    def update_progress(self, batch_id: str, personas_processed: int, total_prospects: int):
        """Update batch progress"""
        if not self.batch_tracker_path.exists():
            return
        
        content = self.batch_tracker_path.read_text()
        
        # Update metrics for this batch
        batch_section_start = content.find(f"### Batch ID: {batch_id}")
        if batch_section_start == -1:
            return
        
        # Find the metrics section
        metrics_start = content.find("#### Metrics:", batch_section_start)
        metrics_end = content.find("#### Notes:", metrics_start)
        
        if metrics_start != -1 and metrics_end != -1:
            old_metrics = content[metrics_start:metrics_end]
            
            # Update the progress line
            import re
            new_metrics = re.sub(
                r'Prospects Processed: \d+/\w+',
                f'Prospects Processed: {personas_processed}/{total_prospects}',
                old_metrics
            )
            
            content = content[:metrics_start] + new_metrics + content[metrics_end:]
            self.batch_tracker_path.write_text(content)
    
    def complete_batch(self, batch_id: str, total_personas: int, output_file: Path):
        """Mark batch as complete"""
        end_time = datetime.now()
        
        # Update activity ledger
        self.log_activity(
            activity=f"Batch {batch_id} completed",
            details=f"{total_personas} personas extracted, output: {output_file.name}",
            status="Complete"
        )
        
        # Update batch tracker
        if self.batch_tracker_path.exists():
            content = self.batch_tracker_path.read_text()
            
            # Update status
            content = content.replace(
                f"Batch ID: {batch_id}\n- **Version**: v1.0\n- **Status**: In Progress",
                f"Batch ID: {batch_id}\n- **Version**: v1.0\n- **Status**: Complete"
            )
            
            # Update end time
            content = re.sub(
                f"({batch_id}.*?End Time: )TBD",
                f"\\1{end_time.strftime('%Y-%m-%d %H:%M:%S')}",
                content,
                flags=re.DOTALL
            )
            
            # Check all tasks as complete
            batch_section = re.search(
                f"### Batch ID: {batch_id}.*?(?=###|$)",
                content,
                re.DOTALL
            )
            
            if batch_section:
                updated_section = batch_section.group(0)
                updated_section = updated_section.replace("- [ ]", "- [x]")
                content = content.replace(batch_section.group(0), updated_section)
            
            self.batch_tracker_path.write_text(content)
    
    def fail_batch(self, batch_id: str, error_message: str):
        """Mark batch as failed"""
        # Update activity ledger
        self.log_activity(
            activity=f"Batch {batch_id} failed",
            details=error_message,
            status="Failed"
        )
        
        # Update batch tracker status
        if self.batch_tracker_path.exists():
            content = self.batch_tracker_path.read_text()
            content = content.replace(
                f"Batch ID: {batch_id}\n- **Version**: v1.0\n- **Status**: In Progress",
                f"Batch ID: {batch_id}\n- **Version**: v1.0\n- **Status**: Failed"
            )
            
            # Add error to notes
            batch_section = re.search(
                f"### Batch ID: {batch_id}.*?#### Notes:.*?\n(.*?)\n---",
                content,
                re.DOTALL
            )
            
            if batch_section:
                old_notes = batch_section.group(1)
                new_notes = old_notes + f"\n- ERROR: {error_message}"
                content = content.replace(old_notes, new_notes)
            
            self.batch_tracker_path.write_text(content)