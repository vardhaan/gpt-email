import os
import openai
from transformers import GPT2Tokenizer


class GPT_Wrapper:
	def __init__(self):
		openai.api_key = os.environ.get('OPENAI_API_KEY')
		self.email_format = """Email 1 subject: “{}”
							Email 1 body:
							“{}”"""
		self.prioritization_question = "I am a busy person. How relevant is this email to me? Give your answer as an integer out of 100. Explain your reasoning."
		self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
		self.summarization_question = "I am a busy person. Summarize this email (be succinct). Write your answer in as few bullet points as needed:"

	def prioritize_email(self, email_subject, email_body):
		formatted_email = self.email_format.format(email_subject, email_body)
		full_prompt = formatted_email + "\n" + self.prioritization_question
		response = openai.Completion.create(
		model="text-davinci-002",
		prompt=full_prompt,
		max_tokens=500,
		temperature=1
		)
		return (response['choices'][0]['text'], response['usage'])

	def summarize_email(self, email_subject, email_body):
		formatted_email = self.email_format.format(email_subject, email_body)
		full_prompt = formatted_email + "\n" + self.summarization_question
		response = openai.Completion.create(
		model="text-davinci-002",
		prompt=full_prompt,
		max_tokens=500,
		temperature=1
		)
		return (response['choices'][0]['text'], response['usage'])

	def num_tokens_in_string(self, input_string):
		return len(self.tokenizer(input_string)['input_ids'])

'''
API_KEY = os.environ.get('OPENAI_API_KEY')

EMAIL_FORMAT = """Email 1 subject: “{}”
Email 1 body:
“{}”"""

PRIORITIZATION_QUESTION = "I am a busy person. How relevant is this email to me? Give your answer as an integer out of 100. Explain your reasoning."


EXAMPLE_EMAIL_BODY = 'Mike,\r\n\r\nHere\xe2\x80\x99s the spreadsheet you asked for. The partner meeting was rescheduled\r\nfor next Tuesday, giving us a few extra days. Can you pull the following:\r\n\r\n\r\n   1.\r\n\r\n   CAC/LTV for the cohort starting March 1st\r\n   2.\r\n\r\n   28DAU and retention per cohort\r\n\r\n\r\nIf you send those over by tomorrow EOD, I\xe2\x80\x99ll put it in the deck for review\r\n'
EXAMPLE_EMAIL_SUBJECT = "Re: Data for slides"

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


def prioritize_email(email_subject, email_body):
	formatted_email = EMAIL_FORMAT.format(email_subject, email_body)
	full_prompt = formatted_email + "\n" + PRIORITIZATION_QUESTION
	openai.api_key = API_KEY
	response = openai.Completion.create(
		model="text-davinci-002",
		prompt=full_prompt,
		max_tokens=500,
		temperature=1
	)
	return (response['choices'][0]['text'], response['usage'])


def num_tokens_for_string(input_string):
	print(type(input_string))
	return len(tokenizer(input_string)['input_ids'])
'''