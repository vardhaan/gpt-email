from gmail_api import *
from gpt import *

messages = main()
for message in messages:
	subject, body = message
	print("token func called")
	num_tokens_body = num_tokens_for_string(body)
	if num_tokens_body > 3000: 
		#print("too big!")
		continue
	#print(body)
	prioritization, usage = prioritize_email(subject, body)
	#print(subject, prioritization, usage)