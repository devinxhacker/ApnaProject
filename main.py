# In main.py
from parser import parse_config_files
from network_model import build_topology
from validator import validate_network, analyze_load_and_optimize
from simulator import Simulation
import time

# --- Part 1: Parsing and Building ---
print("1. Parsing configuration files...")
parsed_info = parse_config_files('conf')
routers, links = build_topology(parsed_info)
print(f"   - Found {len(routers)} routers and {len(links)} links.")

# --- Part 2: Validation and Analysis ---
print("\n2. Validating network configuration...")
findings = validate_network(routers, links)
for finding in findings:
    print(f"   - {finding}")

print("\n3. Analyzing for optimizations...")
recommendations = analyze_load_and_optimize(routers, links)
for rec in recommendations:
    print(f"   - {rec}")

# --- Part 3: Simulation ---
print("\n4. Starting Day-1 Simulation...")
sim = Simulation(routers, links)
sim.start()
time.sleep(2) # Let it run for a bit

# --- Part 4: Fault Injection ---
# Pause and resume is conceptually handled by controlling message passing [cite: 94]
sim.inject_link_failure('R1', 'R3')
time.sleep(2)

print("\n5. Retrieving simulation logs...")
print("Logs for R1:")
for log_entry in sim.get_logs('R1'):
    print(f"   {log_entry}")
print("\nLogs for R2:")
for log_entry in sim.get_logs('R2'):
    print(f"   {log_entry}")
    
sim.stop()
print("\nProject execution finished.")