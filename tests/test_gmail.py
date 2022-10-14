from cgitb import html
import unittest
from src.gmail_api import *


'''



#Need to be refactored since in different file now.
def test_decoding_option():
	tough_case_id = "183619badc73cf46"
	easy_case_id = "183619643e11d0a4"
	another_case = "183617ba5cbb208c"
	creds = authenticate()
	subject, body = get_message_data(easy_case_id, creds)
	print(subject, body)

#Need to be refactored since in different file now.
def test_get_recent_messages():
	gmail = gmail_api.Gmail_Wrapper()
	messages = gmail.get_messages()
	for msg in messages:
		print(msg([0]))


def test_send_email():
	gmail = gmail_api.Gmail_Wrapper()
	gmail.send_email("subj", "bod", ["jumpstart.onboard@gmail.com"])


def test_format_recipients():
	gmail = gmail_api.Gmail_Wrapper()
	recips = ["a@yahoo.com", "b@gmail.com", "c@lycos.com"]
	formatted = gmail.format_recipients(recips)
	print(formatted)

def test_history():
	gmail = gmail_api.Gmail_Wrapper()
	messages = gmail.get_messages_history()
	print(messages)

def tester():
	gmail = gmail_api.Gmail_Wrapper()
	r = gmail.get_message_data('183ac06a271b7549')
	print(r)
'''

class Test_Gmail(unittest.TestCase):

	def setUp(self):
		self.gmail = Gmail_Wrapper()

	def test_send_html(self):

		test_html_string = """<h1>TL;DR</h1>
			<ul>
			<li><a href="www.google.com">Email subject</a>
				<ul>
					<li> Summary point 1</li>
					<li> Summary point 2</li>
				</ul>
			</li>
			</ul>"""
		sent_email_id = self.gmail.send_email("Test HTML email", test_html_string, ['jumpstart.onboard@gmail.com'], html=True)
		self.assertTrue((sent_email_id is not None))
		

if __name__=='__main__':
	unittest.main()





