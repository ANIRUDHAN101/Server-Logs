def display_ip_request_counts(ip_request_data):
    # Print the header
    print(f"{'IP Address':<20}{'Request Count':<15}")
    print("-" * 35)
    
    # Print each row
    for entry in ip_request_data:
        print(f"{entry[0]:<20}{entry[1]:<15}")

def display_most_accessed_endpoint(endpoint_data):
    # Extract the endpoint and access count
    endpoint = endpoint_data[0]
    access_count = endpoint_data[1]
    
    # Format and print the output
    print("Most Frequently Accessed Endpoint:")
    print(f"{endpoint} (Accessed {access_count} times)")

def display_suspicious_activity(suspicious_activity_data):
    # Print the header
    print("Suspicious Activity Detected:")
    print(f"{'IP Address':<20}{'Failed Login Attempts':<25}")
    print("-" * 45)
    
    # Print each row
    for entry in suspicious_activity_data:
        print(f"{entry[0]:<20}{entry[1]:<25}")


