# Automated Network Analysis and Simulation Tool

This project is a Python-based tool designed to automate the analysis and simulation of computer networks. It reads Cisco device configuration files, builds an in-memory model of the network topology, and then uses this model to perform validation, analysis, and dynamic simulation of network events.

## Features

*   **Configuration Parsing**: Reads and parses Cisco `config.dump` files to extract key information like hostnames, interfaces, IP addresses, and bandwidth.
*   **Network Topology Modeling**: Automatically builds a graph-like model of the network, representing routers, interfaces, and the links connecting them based on shared subnets.
*   **Configuration Validation**: Checks the network model for common configuration errors, such as:
    *   Duplicate IP addresses across the network.
    *   MTU mismatches on connected links.
    *   Interfaces that are configured but not connected to another device in the model.
*   **Performance Analysis & Optimization**: Provides high-level recommendations for network optimization, including:
    *   Identifying potential bandwidth bottlenecks under assumed traffic loads.
    *   Suggesting load balancing opportunities.
    *   Recommending more scalable routing protocols (e.g., BGP) for larger networks.
*   **Dynamic Simulation**: Simulates the real-time operation of routers using multi-threading. It can simulate events like:
    *   Router startup and initial protocol discovery.
    *   Link failures and the subsequent propagation of failure notifications to affected devices.

## Project Structure

The project is organized into several modules, each with a specific responsibility.

```
.
├── main.py             # Main script to orchestrate the tool's workflow
├── parser.py           # Logic for parsing configuration files
├── network_model.py    # Defines the core classes: Router, Interface, Link
├── validator.py        # Logic for validating the network model and finding optimizations
├── simulator.py        # Multi-threaded simulation engine
└── conf/               # Directory for device configuration files
    ├── R1/
    │   └── config.dump
    ├── R2/
    │   └── config.dump
    └── R3/
        └── config.dump
```

## Getting Started

### Prerequisites

*   Python 3.6 or newer.

The tool uses standard Python libraries, so no external packages are required for installation.

### Setup

1.  Clone the repository to your local machine.

2.  Place your Cisco configuration files in the `conf` directory. Each device must have its own subdirectory (e.g., `R1/`), containing a `config.dump` file, as shown in the project structure above. The parser will automatically discover and process these files.

## Usage

To run the complete analysis and simulation pipeline, execute the main script from the project's root directory:

```bash
python main.py
```

The script will output the results of each stage directly to the console:

1.  **Parsing**: Shows the number of routers and links found.
2.  **Validation**: Lists any configuration errors or warnings discovered.
3.  **Analysis**: Prints optimization recommendations.
4.  **Simulation**: Indicates the start of the simulation and logs events from the simulated routers, including the reaction to a hardcoded link failure between R1 and R3.

### Example Output

```
1. Parsing configuration files...
   - Found 3 routers and 3 links.

2. Validating network configuration...
   - WARNING: MTU Mismatch on link. R1:FastEthernet1/0 has MTU 1500, but R2:FastEthernet1/0 has MTU 1400.
   - INFO: Unconnected Interface - R1:FastEthernet0/0 has an IP but is not connected to any other parsed device.
   - INFO: Unconnected Interface - R3:FastEthernet0/0 has an IP but is not connected to any other parsed device.

3. Analyzing for optimizations...
   - LOAD WARNING: The primary path R1-R3 has a capacity of 100.0 Mbps, which may not support peak load of 150.0 Mbps.
   - RECOMMENDATION: Activate the secondary path via R2 for load balancing lower-priority traffic. [cite: 65]

4. Starting Day-1 Simulation...
Simulation started. All router threads are running.

--- INJECTING FAULT: Failing link between R1 and R3 ---

5. Retrieving simulation logs...
Logs for R1:
   1755601108.610635: Powering ON.
   1755601109.6156778: Starting OSPF discovery...
   1755601110.616205: Received message: {'type': 'LINK_FAILURE', 'neighbor': 'R3'}
   CRITICAL: Detected failure on link to R3. Recalculating routes.

Logs for R2:
   1755601108.610718: Powering ON.
   1755601109.615743: Starting OSPF discovery...
Simulation stopped.

Project execution finished.
```