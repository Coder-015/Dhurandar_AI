import time
import random
from log_generator import LogGenerator

def simulate_events():
    """Simulate various operational events and generate logs."""
    logger = LogGenerator()
    print("Starting DhurandarAI Event Simulation...\n")
    
    events_to_simulate = [
        ("simulate_abnormal_login", simulate_abnormal_login),
        ("simulate_cpu_spike", simulate_cpu_spike),
        ("simulate_suspicious_traffic", simulate_suspicious_traffic),
        ("simulate_normal_traffic", simulate_normal_traffic)
    ]
    
    # Run a quick simulated sequence
    for _ in range(10):
        # Choose a random event to simulate, weighted towards normal traffic
        weights = [0.2, 0.1, 0.2, 0.5] 
        event_func = random.choices(events_to_simulate, weights=weights, k=1)[0][1]
        
        event_func(logger)
        time.sleep(1) # Small delay between events
        
    print("\nSimulation complete. Check 'dhurandar_logs.db' for generated logs.")
    print("Recent Logs:")
    recent = logger.get_recent_logs(limit=5)
    for log in recent:
        print(f"  - {log}")

def simulate_abnormal_login(logger):
    """Simulate abnormal login attempts (e.g. brute force)."""
    devices = ['s1', 'r1', 'fw1']
    target = random.choice(devices)
    failed_attempts = random.randint(5, 20)
    
    print(f"--> Simulating Abnormal Login on {target} ({failed_attempts} attempts)")
    logger.generate_log(
        device=target,
        event="ABNORMAL_LOGIN",
        value=failed_attempts,
        severity="high" if failed_attempts > 10 else "medium"
    )

def simulate_cpu_spike(logger):
    """Simulate a CPU spike on a device."""
    devices = ['s1', 'r1']
    target = random.choice(devices)
    cpu_util = random.uniform(85.0, 99.9)
    
    severity = "high" if cpu_util > 95 else "medium"
    
    print(f"--> Simulating CPU Spike on {target} ({cpu_util:.1f}%)")
    logger.generate_log(
        device=target,
        event="CPU_SPIKE",
        value=round(cpu_util, 1),
        severity=severity
    )

def simulate_suspicious_traffic(logger):
    """Simulate suspicious network traffic (e.g. unexpected volume)."""
    devices = ['h1', 'h2', 'h3']
    target = random.choice(devices)
    # value represents Mbps transferred suddenly
    traffic_volume = random.randint(500, 2000) 
    
    print(f"--> Simulating Suspicious Traffic from {target} ({traffic_volume} Mbps)")
    logger.generate_log(
        device=target,
        event="SUSPICIOUS_TRAFFIC",
        value=traffic_volume,
        severity="high"
    )
    
def simulate_normal_traffic(logger):
    """Simulate normal background network activity."""
    devices = ['h1', 'h2', 'h3', 's1']
    target = random.choice(devices)
    # normal CPU usage
    cpu_util = random.uniform(5.0, 30.0)
    
    print(f"--> Simulating Normal Activity on {target}")
    logger.generate_log(
        device=target,
        event="NORMAL_HEARTBEAT",
        value=round(cpu_util, 1),
        severity="low"
    )

if __name__ == "__main__":
    simulate_events()
