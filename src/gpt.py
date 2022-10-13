import os
import openai
from transformers import GPT2Tokenizer
from transformers.utils import logging


class GPT_Wrapper:
	def __init__(self):
		openai.api_key = os.environ.get('OPENAI_API_KEY')
		#Tokenizer will throw a warning for long sequences without the following line.
		logging.set_verbosity_error()

	def send_completion_request(self, completion_prompt, model_choice="text-davinci-002",
		model_temperature=1, max_output_tokens=200):
		response = openai.Completion.create(
			model=model_choice,
			prompt=completion_prompt,
			max_tokens=max_output_tokens,
			temperature=model_temperature
		)
		return (response['choices'][0]['text'], response['usage'])

	def num_tokens_in_string(self, input_string):
		return len(self.tokenizer(input_string)['input_ids'])
