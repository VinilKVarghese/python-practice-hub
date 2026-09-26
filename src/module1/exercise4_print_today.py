from datetime import datetime
def get_today_date():
    # Get today's date and time
    now = datetime.now()

    # Return date and time in the required format
    return now.strftime("%S:%M:%H, %d/%m/%Y")

# Call the function
print(get_today_date())