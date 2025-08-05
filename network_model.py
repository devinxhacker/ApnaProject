from ipaddress import IPv4Interface # Helpful library for network math

class Interface:
    def __init__(self, name, ip, subnet_mask, bandwidth, mtu):
        self.name = name
        self.ip_address = ip
        self.subnet_mask = subnet_mask
        self.bandwidth = bandwidth
        self.mtu = mtu
        self.link = None # This will point to a Link object
        # The IPv4Interface object makes it easy to find the network address
        self.ip_interface = IPv4Interface(f"{ip}/{subnet_mask}")

    def __repr__(self):
        return f"Interface({self.name}, {self.ip_interface})"

class Router:
    def __init__(self, hostname):
        self.hostname = hostname
        self.interfaces = {}

    def add_interface(self, interface):
        self.interfaces[interface.name] = interface
        
    def __repr__(self):
        return f"Router({self.hostname})"

class Link:
    def __init__(self, interface1, interface2):
        self.endpoint1 = interface1
        self.endpoint2 = interface2
        # A link's bandwidth is the minimum of its two endpoints
        self.bandwidth = min(interface1.bandwidth, interface2.bandwidth)
        interface1.link = self
        interface2.link = self
    
    def __repr__(self):
        return f"Link({self.endpoint1.parent.hostname}:{self.endpoint1.name} <--> {self.endpoint2.parent.hostname}:{self.endpoint2.name})"

def build_topology(parsed_data):
    """
    Takes parsed data and builds a network of Router and Link objects.
    """
    routers = {data['hostname']: Router(data['hostname']) for data in parsed_data}
    all_interfaces = []

    # Create all Interface objects first
    for data in parsed_data:
        router = routers[data['hostname']]
        for if_name, if_data in data['interfaces'].items():
            interface = Interface(if_name, **if_data)
            interface.parent = router # Link back to the parent router
            router.add_interface(interface)
            all_interfaces.append(interface)

    # Discover and create Link objects
    links = []
    for i in range(len(all_interfaces)):
        for j in range(i + 1, len(all_interfaces)):
            if1 = all_interfaces[i]
            if2 = all_interfaces[j]
            # If two interfaces are in the same subnet, they are connected
            if if1.ip_interface.network == if2.ip_interface.network and not if1.link and not if2.link:
                link = Link(if1, if2)
                links.append(link)
                
    return list(routers.values()), links