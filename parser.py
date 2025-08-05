import re
import os

def parse_config_files(config_directory):
    """
    Parses all config.dump files in a directory and returns a list of parsed device data.
    """
    parsed_data = []
    for device_name in os.listdir(config_directory):
        device_path = os.path.join(config_directory, device_name)
        if os.path.isdir(device_path):
            config_file = os.path.join(device_path, 'config.dump')
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    content = f.read()
                    
                    # Use regex to extract data
                    hostname = re.search(r'hostname\s+(\S+)', content).group(1)
                    device_info = {'hostname': hostname, 'interfaces': {}}
                    
                    # Find all interface blocks
                    interface_blocks = re.findall(r'interface\s+(\S+)(.*?)(?=interface|\Z)', content, re.DOTALL)
                    
                    for if_name, if_config in interface_blocks:
                        ip_match = re.search(r'ip\s+address\s+([\d\.]+)\s+([\d\.]+)', if_config)
                        bw_match = re.search(r'bandwidth\s+(\d+)', if_config)
                        mtu_match = re.search(r'mtu\s+(\d+)', if_config)

                        ip = ip_match.group(1) if ip_match else None
                        subnet = ip_match.group(2) if ip_match else None
                        bandwidth = int(bw_match.group(1)) * 1000 if bw_match else 100000000 # Default to 100 Mbps
                        mtu = int(mtu_match.group(1)) if mtu_match else 1500 # Default MTU

                        if ip: # Only add interfaces with IP addresses
                            device_info['interfaces'][if_name] = {
                                'ip': ip,
                                'subnet_mask': subnet,
                                'bandwidth': bandwidth, # [cite: 8]
                                'mtu': mtu # [cite: 13]
                            }
                    parsed_data.append(device_info)
    return parsed_data