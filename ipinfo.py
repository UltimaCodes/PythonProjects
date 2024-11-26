# Uses the ipinfo API to get information of an ipv4 address

import tkinter as tk
import requests

def get_ip_details(ip_address):
    api_url = f"http://ipinfo.io/{ip_address}/json"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def check_connection(ip_address):
    try:
        requests.get(f"http://{ip_address}", timeout=2)
        return True
    except requests.ConnectionError:
        return False

def fetch_details():
    ip_address = ip_entry.get()

    ip_details = get_ip_details(ip_address)

    if ip_details:
        ip_info.set(f"IP Address: {ip_details.get('ip', 'N/A')}")
        hostname_info.set(f"Hostname: {ip_details.get('hostname', 'N/A')}")
        city_info.set(f"City: {ip_details.get('city', 'N/A')}")
        region_info.set(f"Region: {ip_details.get('region', 'N/A')}")
        country_info.set(f"Country: {ip_details.get('country', 'N/A')}")
        location_info.set(f"Location: {ip_details.get('loc', 'N/A')}")
        timezone_info.set(f"Timezone: {ip_details.get('timezone', 'N/A')}")
        organization_info.set(f"Organization: {ip_details.get('org', 'N/A')}")

        if check_connection(ip_address):
            connection_info.set("Connection Status: Reachable")
        else:
            connection_info.set("Connection Status: Not Reachable")
    else:
        ip_info.set("Failed to retrieve IP details.")
        hostname_info.set("")
        city_info.set("")
        region_info.set("")
        country_info.set("")
        location_info.set("")
        timezone_info.set("")
        organization_info.set("")
        connection_info.set("")

def clear_details():
    ip_entry.delete(0, tk.END)
    ip_info.set("")
    hostname_info.set("")
    city_info.set("")
    region_info.set("")
    country_info.set("")
    location_info.set("")
    timezone_info.set("")
    organization_info.set("")
    connection_info.set("")

# Create the main GUI window
root = tk.Tk()
root.title("FoodPandoxx")

# Variables to hold IP details
ip_info = tk.StringVar()
hostname_info = tk.StringVar()
city_info = tk.StringVar()
region_info = tk.StringVar()
country_info = tk.StringVar()
location_info = tk.StringVar()
timezone_info = tk.StringVar()
organization_info = tk.StringVar()
connection_info = tk.StringVar()

# IP Entry
ip_entry_label = tk.Label(root, text="Enter IP Address:")
ip_entry_label.pack(pady=5)
ip_entry = tk.Entry(root, width=30)
ip_entry.pack(pady=5)

# Buttons
fetch_button = tk.Button(root, text="Fetch Details", command=fetch_details)
fetch_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", command=clear_details)
clear_button.pack(pady=5)

# IP Details
ip_label = tk.Label(root, textvariable=ip_info)
ip_label.pack(pady=5)
hostname_label = tk.Label(root, textvariable=hostname_info)
hostname_label.pack()
city_label = tk.Label(root, textvariable=city_info)
city_label.pack()
region_label = tk.Label(root, textvariable=region_info)
region_label.pack()
country_label = tk.Label(root, textvariable=country_info)
country_label.pack()
location_label = tk.Label(root, textvariable=location_info)
location_label.pack()
timezone_label = tk.Label(root, textvariable=timezone_info)
timezone_label.pack()
organization_label = tk.Label(root, textvariable=organization_info)
organization_label.pack()

# Connection Status
connection_label = tk.Label(root, textvariable=connection_info)
connection_label.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
