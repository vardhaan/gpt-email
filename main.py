from gmail_api import *
from gpt import *




gmail = Gmail_Wrapper()
gpt = GPT_Wrapper()

messages = gmail.get_messages()
for message in messages:
	subject, body = message
	num_tokens_body = gpt.num_tokens_in_string(body)
	if num_tokens_body > 3000: 
		continue
	prioritization, usage = gpt.prioritize_email(subject, body)
	print(subject, prioritization)
	break
