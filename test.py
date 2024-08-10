# Python program to
# demonstrate creation of an 
# assistant using wolf ram API 

import wolframalpha
import ssl

# Disable Certificate Verification
ssl._create_default_https_context = ssl._create_unverified_context

# Taking input from user 
question = input('Question: ')

# App id obtained by the above steps 
app_id = "KXYP3X-E6WW5P97WR"

# Instance of wolf ram alpha  
# client class 
client = wolframalpha.Client(app_id)

# Stores the response from  
# wolf ram alpha 
res = client.query(question)

# Includes only text from the response 
answer = next(res.results).text

print(answer) 