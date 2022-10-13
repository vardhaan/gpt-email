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


def get_prioritization_buckets():
	config_file = open('config.json')
	data = config_file.read()
	json_data = json.loads(data)['prioritization_buckets']
	importance_dict = {}
	importance_dict['must_read'] = int(json_data['must_read'])
	importance_dict['nice_to_know'] = int(json_data['nice_to_know'])
	importance_dict['unimportant'] = int(json_data['unimportant'])
	return importance_dict


'''
Takes in a batch of emails, prioritizes them, and sorts them into "Must-read", "Nice-to-know", and "Unimportant."

Inputs:
- emails_list: List of (subj, body) tuples of type (str, str)
- gpt_requester: Callable that will prioritize each email
- importance_preferences: Dict containing minimum priority scores for each bucket of importance

Outputs:
- prioritized_emails: Dict containing three keys (must_read, nice_to_know, unimportant). Each key contains a list of (subj, body, priority) tuples
of type (str, str, int) that meet the minimum priority score for that bucket.
'''
def prioritize_emails(emails_list, gpt_requester, importance_preferences):
	must_read_score = importance_preferences['must_read']
	nice_to_know_score = importance_preferences['nice_to_know']
	prioritizer = Prioritizer()
	prioritized_email_list = prioritizer.prioritize_emails(emails_list, gpt_requester)
	prioritized_emails = {"must_read": [], "nice_to_know": [], "unimportant": []}
	for email in prioritized_email_list:
		priority = email[2]
		if priority >= must_read_score:
			prioritized_emails['must_read'].append(email)
			continue
		if priority >= nice_to_know_score:
			prioritized_emails['nice_to_know'].append(email)
			continue
		prioritized_emails['unimportant'].append(email)
	return prioritized_emails

'''
Cheap summarizer needs to run on each email. Then prioritizer works on them. Then we form summary email.
'''




gmail = Gmail_Wrapper()
gpt = GPT_Wrapper()
summarizer = Summarizer()

messages = gmail.get_messages_history()
summary = summarizer.summarize_emails(messages, gpt.send_completion_request, cheap=True)
print("!!!!!=====================================================================!!!!!")
print(generate_summary_email(summary))

