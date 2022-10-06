import os
import openai
from transformers import GPT2Tokenizer
from transformers.utils import logging


class GPT_Wrapper:
	def __init__(self):
		openai.api_key = os.environ.get('OPENAI_API_KEY')
		#Tokenizer will throw a warning for long sequences without the following line.
		logging.set_verbosity_error()
		self.email_format = """Email 1 subject: “{}”
							Email 1 body:
							“{}”"""
		self.prioritization_question = "I (Mike) am a busy person. How relevant is this email to me? Give your answer as an integer out of 100. Explain your reasoning."
		self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
		self.summarization_question = "I am a busy person. Summarize this email (be succinct). Write your answer in as few bullet points as needed:"

	def prioritize_email(self, email_subject, email_body):
		#61 tokens used in prompt excluding subject and body
		formatted_email = self.email_format.format(email_subject, email_body)
		full_prompt = formatted_email + "\n" + self.prioritization_question
		print(full_prompt)
		response = openai.Completion.create(
		model="text-davinci-002",
		prompt=full_prompt,
		max_tokens=500,
		temperature=1
		)
		return (response['choices'][0]['text'], response['usage'])

	def summarize_email(self, email_subject, email_body):
		#59 tokens used in prompt excluding subject and body
		formatted_email = self.email_format.format(email_subject, email_body)
		full_prompt = formatted_email + "\n" + self.summarization_question
		response = openai.Completion.create(
		model="text-davinci-002",
		prompt=full_prompt,
		max_tokens=500,
		temperature=1
		)
		return (response['choices'][0]['text'], response['usage'])

	def send_completion_request(self, completion_prompt, model_choice="text-davinci-002",
		model_temperature=1, max_output_tokens=500):
		response = openai.Completion.create(
			model=model_choice,
			prompt=completion_prompt,
			max_tokens=max_output_tokens,
			temperature=model_temperature
		)
		return (response['choices'][0]['text'], response['usage'])



	def num_tokens_in_string(self, input_string):
		return len(self.tokenizer(input_string)['input_ids'])
