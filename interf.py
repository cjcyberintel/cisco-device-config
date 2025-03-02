from netmiko import ConnectHandler

# Device connection details
device = {
    "device_type": "cisco_xe",  # Device type for Cisco IOS XE
    "ip": "devnetsandboxiosxe.cisco.com",  # Public URL
    "username": "admin",  # Username
    "password": "C1sco12345",  # Password
    "port": 22,  # SSH port
}

# Function to display interfaces
def display_interfaces(interfaces):
    print("\nCurrent Interface Status:")
    print(interfaces)

# Function to get unassigned interfaces
def get_unassigned_interfaces(interfaces):
    unassigned = []
    for line in interfaces.splitlines():
        if "unassigned" in line:
            interface = line.split()[0]
            unassigned.append(interface)
    return unassigned

# Function to configure an interface
def configure_interface(net_connect, interface, ip_address, subnet_mask):
    config_commands = [
        f"interface {interface}",
        f"ip address {ip_address} {subnet_mask}",
        "no shutdown",
    ]
    output = net_connect.send_config_set(config_commands)
    print(f"\nConfiguration output for {interface}:")
    print(output)

# Main script
try:
    # Connect to the device
    print("Connecting to the device...")
    net_connect = ConnectHandler(**device)
    print("Connected successfully!")

    # Get current interface status
    interfaces = net_connect.send_command("show ip int brief")
    display_interfaces(interfaces)

    # Get unassigned interfaces
    unassigned_interfaces = get_unassigned_interfaces(interfaces)
    if not unassigned_interfaces:
        print("\nNo unassigned interfaces found.")
    else:
        print("\nUnassigned Interfaces:")
        for i, interface in enumerate(unassigned_interfaces, 1):
            print(f"{i}. {interface}")

        # Prompt user to select an interface
        try:
            selection = int(input("\nSelect an interface to configure (enter number): ")) - 1
            if 0 <= selection < len(unassigned_interfaces):
                selected_interface = unassigned_interfaces[selection]
                print(f"You selected: {selected_interface}")

                # Prompt user for IP address and subnet mask
                ip_address = input(f"Enter IP address for {selected_interface}: ")
                subnet_mask = input(f"Enter subnet mask for {selected_interface}: ")

                # Configure the selected interface
                configure_interface(net_connect, selected_interface, ip_address, subnet_mask)

                # Display updated interface status
                updated_interfaces = net_connect.send_command("show ip int brief")
                display_interfaces(updated_interfaces)
            else:
                print("Invalid selection. Please choose a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Disconnect from the device
    net_connect.disconnect()
    print("\nDisconnected from the device.")

except Exception as e:
    print(f"An error occurred: {e}")
