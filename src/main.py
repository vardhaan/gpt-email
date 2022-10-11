from gmail_api import *
from gpt import *
from email_assistant import *


def generate_summary_email(summary):
	super_summary = summary['super_summary']
	individual_summaries = ""
	for tup in summary['summary_list']:
		subj, summ = tup
		line = subj + " : " + summ
		individual_summaries = individual_summaries + line + "\n\n"
	summary_email_string = "Super summary:" + "\n\n" + super_summary + "\n\n" + individual_summaries
	return summary_email_string
	


def send_summary_email(summary):
	summary_email_subj = "Your super summary!"
	gmail.send_email(summary_email_subj, summary, ["jumpstart.onboard@gmail.com"])



gmail = Gmail_Wrapper()
gpt = GPT_Wrapper()
summarizer = Summarizer()

messages = gmail.get_messages_history()
summary = summarizer.summarize_emails(messages, gpt.send_completion_request, cheap=True)
print("!!!!!=====================================================================!!!!!")
print(generate_summary_email(summary))

