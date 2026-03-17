import sqlite3
import json
import datetime
from abc import ABC, abstractmethod

DB_FILE = 'dhurandar_logs.db'

class Rule(ABC):
    """Base class for event correlation rules."""
    
    @abstractmethod
    def evaluate(self, device, events):
        """
        Evaluate a sequence of events for a specific device.
        Returns a dictionary representing the diagnosis report if matched, else None.
        """
        pass

class CompromisedMachineRule(Rule):
    """
    Detects a possible compromised machine based on:
    - Abnormal Login (or unusual login location)
    - CPU usage spike
    - Abnormal network traffic (Suspicious traffic)
    """
    def evaluate(self, device, events):
        has_abnormal_login = False
        has_cpu_spike = False
        has_suspicious_traffic = False
        
        contributing_events = []
        
        for event in events:
            evt_type = event.get('event')
            
            if evt_type == 'ABNORMAL_LOGIN':
                has_abnormal_login = True
                contributing_events.append("login anomaly")
            elif evt_type == 'CPU_SPIKE':
                has_cpu_spike = True
                contributing_events.append("cpu spike")
            elif evt_type == 'SUSPICIOUS_TRAFFIC':
                has_suspicious_traffic = True
                contributing_events.append("abnormal network traffic")
                
        # If all conditions are met
        if has_abnormal_login and has_cpu_spike and has_suspicious_traffic:
            # Deduplicate contributing events while preserving order roughly
            unique_events = list(dict.fromkeys(contributing_events))
            return {
                "incident": "Possible Account/Machine Compromise",
                "affected_host": device,
                "confidence_score": 0.87,
                "events": unique_events
            }
        
        return None

class CorrelationEngine:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.rules = []
        self._register_rules()
        
    def _register_rules(self):
        """Register all active correlation rules."""
        self.rules.append(CompromisedMachineRule())
        # More rules can easily be added here later
        
    def fetch_recent_logs(self, minutes=60):
        """Fetch logs from the past N minutes."""
        # For simulation purposes without exact time filtering in SQL, 
        # we will fetch the last 100 logs or all logs to analyze.
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate time threshold (if we want strict time limits)
        time_threshold = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=minutes)
        threshold_iso = time_threshold.isoformat()
        
        cursor.execute(
            'SELECT raw_json FROM security_logs WHERE timestamp >= ? ORDER BY timestamp ASC',
            (threshold_iso,)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [json.loads(row[0]) for row in rows]
        
    def group_events_by_device(self, events):
        """Group a list of events by their device identifier."""
        grouped = {}
        for event in events:
            device = event.get('device')
            if not device:
                continue
            if device not in grouped:
                grouped[device] = []
            grouped[device].append(event)
        return grouped

    def analyze(self):
        """Analyze recent logs and run them against the registered rules."""
        print("Starting Event Correlation Engine...")
        logs = self.fetch_recent_logs(minutes=60)
        
        if not logs:
            print("No recent logs found to analyze.")
            return []
            
        print(f"Fetched {len(logs)} recent events for analysis.")
        
        grouped_logs = self.group_events_by_device(logs)
        reports = []
        
        for device, events in grouped_logs.items():
            for rule in self.rules:
                report = rule.evaluate(device, events)
                if report:
                    reports.append(report)
                    
        return reports

if __name__ == '__main__':
    engine = CorrelationEngine()
    diagnoses = engine.analyze()
    
    if diagnoses:
        print("\n--- DIAGNOSIS REPORTS ---")
        for report in diagnoses:
            print(json.dumps(report, indent=4))
    else:
        print("\nNo correlated incidents detected based on current rules.")
