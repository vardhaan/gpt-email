from operator import itemgetter
import random


class EmailHandler():
	def __init__(self, prompt_file_string):
		prompt_file = open('prompts/' + prompt_file_string) #no ".." in path because this module should be called from the root email_gpt dir, not from within src.
		self.prompt = prompt_file.read()
		prompt_file.close()

	def handle_email(self, subject, body, gpt_requester, cheap=False, temperature=0):
		model = "text-davinci-002"
		if cheap:
			model="text-curie-001"
		full_prompt = self.prompt.format(subject, body)
		results = gpt_requester(full_prompt, model_choice=model, model_temperature=temperature)
		return results[0]



class Prioritizer(EmailHandler):
	'''This class takes in email subjects and bodies, prioritizes each of them, and sorts them in descending order of priority.
	It uses GPT-3 to prioritize each email. The constructor takes in an optional text file containing a prompt used to prioritize each email.'''
	
	def __init__(self, prompt_file='prioritization.txt'):
		self.priority_regex = "Final Answer." #Depends on prompt being used. Could I put this in the prompt file too?
		super().__init__(prompt_file)

	def prioritize_emails(self, email_batch, gpt_requester):
		'''This method takes in a list of (subject, body) tuples representing emails, prioritizes each of them, and returns a sorted list of the emails in 
		descending order of priority.

		Inputs:
		- email_batch: List of (subject, body) tuples of type (str, str).
		- gpt_requester: A callable that will return a priority score for each email.
		
		Outputs:
		- priority_ordered_emails: List of (subject, body, priority) tuples of type (str, str, int) sorted in descending order of priority.
		'''
		priority_ordered_emails = []
		for email in email_batch:
			subject = email[0]
			body = email[1]
			priority_response = self.handle_email(subject, body, gpt_requester)
			priority = self.find_priority_in_response(priority_response)
			priority_tuple = (subject, body, priority)
			priority_ordered_emails.append(priority_tuple)
		priority_ordered_emails.sort(key=itemgetter(2), reverse=True)
		return priority_ordered_emails


	def find_priority_in_response(self, prioritization_response):
		priority = prioritization_response.split(self.priority_regex)[-1]
		priority = int(priority.strip().split(".")[0]) #remove spaces and any periods in answer
		return priority



'''
This class takes in email subjects and bodies and summarizes each of them. It also computes a summary
of summaries (i.e. the TL;DR of the entire batch of emails).
'''
class Summarizer(EmailHandler):
	def __init__(self, prompt_file='summarization.txt'):
		super().__init__(prompt_file)


	def summarize_emails(self, email_batch, gpt_requester, cheap=False):
		summary = {}
		summary["summary_list"] = []
		super_summary_body = ""
		for email in email_batch:
			subject = email[0]
			body = email[1]
			email_summary = self.handle_email(subject, body, gpt_requester, cheap)
			summary['summary_list'].append((subject, email_summary))
			super_summary_body = super_summary_body + "\n" + email_summary
		super_summary = self.summarize_email("Summary", super_summary_body, gpt_requester, cheap)
		summary['super_summary'] = super_summary
		return summary

