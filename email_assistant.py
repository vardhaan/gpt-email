'''
This class takes in email subjects and bodies and outputs a prioritization (in list format) for them.
How we will prioritize:
- Ask GPT-3 the priority (this may require handling incorrect response formats from GPT-3)
- Sort according to that order
'''
class Prioritizer:
	def __init__(self):
		self.email_format = """Email 1 subject: “{}”
							Email 1 body:
							“{}”"""
		self.prioritization_question = "I (Mike) am a busy person. How relevant is this email to me? Give your answer as an integer out of 100. Explain your reasoning."

	def prioritize_emails():
		pass


'''
This class takes in email subjects and bodies and summarizes each of them. It also computes a summary
of summaries (i.e. the TL;DR of the entire batch of emails).
'''
class Summarizer:
	def __init__(self):
		self.email_format = """Email 1 subject: “{}”
							Email 1 body:
							“{}”"""
		self.summarization_question = "I am a busy person. Summarize this email (be succinct). Write your answer in as few bullet points as needed:"

	def summarize_emails(self, email_batch, gpt_requester):
		summary = {}
		summary["summary_list"] = []
		super_summary_body = ""
		for email in email_batch:
			subject = email[0]
			body = email[1]
			email_summary = self.summarize_email(subject, body, gpt_requester)
			summary['summary_list'].append((subject, email_summary))
			super_summary_body = super_summary_body + "\n" + email_summary
		super_summary = self.summarize_email("Summary", super_summary_body, gpt_requester)
		summary['super_summary'] = super_summary
		return summary

	def summarize_email(self, subject, body, gpt_requester):
		formatted_email = self.email_format.format(subject, body)
		full_prompt = formatted_email + "\n" + self.summarization_question
		results = gpt_requester(full_prompt)
		email_summary = results[0]
		return email_summary