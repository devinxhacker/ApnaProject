def validate_network(routers, links):
    """
    Runs a series of validation checks on the network model.
    """
    findings = []

    # 1. Check for Duplicate IP Addresses [cite: 70]
    ips_seen = {}
    for router in routers:
        for interface in router.interfaces.values():
            if interface.ip_address in ips_seen:
                findings.append(f"ERROR: Duplicate IP {interface.ip_address} found on {router.hostname}:{interface.name} and {ips_seen[interface.ip_address]}")
            else:
                ips_seen[interface.ip_address] = f"{router.hostname}:{interface.name}"

    # 2. Check for MTU Mismatches on Links [cite: 75]
    for link in links:
        if link.endpoint1.mtu != link.endpoint2.mtu:
            findings.append(f"WARNING: MTU Mismatch on link. {link.endpoint1.parent.hostname}:{link.endpoint1.name} has MTU {link.endpoint1.mtu}, but {link.endpoint2.parent.hostname}:{link.endpoint2.name} has MTU {link.endpoint2.mtu}.")

    # 3. Check for Missing Components (simple version) [cite: 12, 66]
    # This checks if an interface is up but has no link in our model.
    for router in routers:
        for interface in router.interfaces.values():
            if not interface.link:
                 findings.append(f"INFO: Unconnected Interface - {router.hostname}:{interface.name} has an IP but is not connected to any other parsed device.")

    # Additional checks like incorrect VLANs or gateways would require parsing switch configs and end-host data.
    
    return findings


def find_path(start_router_name, end_router_name, routers):
    """
    Finds a path between two routers using BFS.
    Returns the list of router objects in the path.
    """
    # (Implementation of BFS algorithm on the router graph)
    # This is a standard algorithm you can find resources for.
    # ... for brevity, we'll assume this function exists.
    # In a real implementation, you would use a library like `networkx` or write your own.
    pass

def analyze_load_and_optimize(routers, links):
    """
    Analyzes load and suggests optimizations.
    """
    recommendations = []

    # 1. Load Balancing Recommendation [cite: 10, 64]
    # Example: Check the path from R1 to Server0's network (via R3).
    # We assume a 'traffic_demand' value for this example.
    traffic_demand = 150_000_000 # 150 Mbps, which is > FastEthernet speed

    # Find the primary path (R1 -> R3)
    r1_r3_link = next((link for link in links if (link.endpoint1.parent.hostname == 'R1' and link.endpoint2.parent.hostname == 'R3') or \
                                                 (link.endpoint1.parent.hostname == 'R3' and link.endpoint2.parent.hostname == 'R1')), None)

    if r1_r3_link and traffic_demand > r1_r3_link.bandwidth:
        recommendations.append(f"LOAD WARNING: The primary path R1-R3 has a capacity of {r1_r3_link.bandwidth/1_000_000} Mbps, which may not support peak load of {traffic_demand/1_000_000} Mbps.")
        # Suggest activating the secondary path
        recommendations.append("RECOMMENDATION: Activate the secondary path via R2 for load balancing lower-priority traffic. [cite: 65]")

    # 2. Protocol Recommendation (BGP vs OSPF) [cite: 14, 74]
    if len(routers) > 10: # A simple heuristic
        recommendations.append("OPTIMIZATION: The network has a significant number of routers. Consider using BGP for more scalable routing, especially if connecting different administrative domains.")

    return recommendations