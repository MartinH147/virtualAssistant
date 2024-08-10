from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

print("now =", now)

# dd/mm/YY H:M:S
hour = now.strftime("%H")
print("hour =", hour)