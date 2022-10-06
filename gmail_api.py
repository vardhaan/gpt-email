from __future__ import print_function

import os.path

import json

import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.message import EmailMessage

class Gmail_Wrapper:

	def __init__(self):
		self.SCOPES = ['https://mail.google.com/']
		self.creds = self.authenticate()
		self.service = None
		self.email_address = None
		try:
			self.service = build('gmail', 'v1', credentials=self.creds)
			profile = self.service.users().getProfile(userId='me').execute()
			self.email_address = profile['emailAddress']
		except HttpError as error:
			print(f'Error: {error}')

	def authenticate(self):
		#Boiler plate code provided by Gmail docs
		creds = None

		if os.path.exists('token.json'):
			creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
				creds = flow.run_local_server(port=0)
			with open('token.json', 'w') as token:
				token.write(creds.to_json())
		return creds

	def get_message_ids(self, num_messages):
		try:
			results = self.service.users().messages().list(userId='me', maxResults=num_messages).execute()
			messages = results.get('messages', [])
			return messages
		except HttpError as error:
			print(f'Error: {error}')

	def get_message_data(self, message_id):
		try:
			results = self.service.users().messages().get(userId='me', id=message_id).execute()
			subject = self.get_subject(results)
			utf_body_string = self.get_body(results)
			return (subject, utf_body_string)
		except Exception as e:
			print(e)
			return None

	def get_messages(self, num_messages=5):
		message_ids_list = self.get_message_ids(num_messages)
		print(message_ids_list)
		return [self.get_message_data(message_id['id']) for message_id in message_ids_list]


	def get_subject(self, gmail_response):
		headers = gmail_response['payload']['headers']
		subject = [header['value'] for header in headers if header['name']=="Subject"]
		return subject[0]


	def get_body(self, gmail_response):
		body_string_b64 = gmail_response['payload']['parts'][0]['body']['data']
		#Tt seems like the below line is unnecessary. At least, in simple plain-text cases.
		#It simply returns the same thing as the body_string_b64 (perhaps Gmail provides it already encoded)
		#TODO: double check on harder cases and close this out.
		#encoded_string = body_string_b64.encode('UTF8') 
		b64_urlsafe_decoded = base64.urlsafe_b64decode(body_string_b64)
		return b64_urlsafe_decoded.decode('UTF-8')

	#Expects email_recipients as an array of strings.
	def send_email(self, email_subject, email_body, email_recipients):
		try:
			message = EmailMessage()
			message.set_content(email_body)
			message['To'] = self.format_recipients(email_recipients)
			message['From'] = self.email_address
			message['Subject'] = email_subject
			print(message)
			encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
			created_message = {
				'raw': encoded_message
			}
			print(created_message['raw'])
			sent_message = self.service.users().messages().send(userId='me', body=created_message).execute()
			print(sent_message)
		except HttpError as error:
			print(f'Error: {error}')

	def format_recipients(self, email_recipients_list):
		return ", ".join(email_recipients_list)




'''
def get_messages_list(credentials, num_messages=5):
	try:
		service = build('gmail', 'v1', credentials=credentials)
		results = service.users().messages().list(userId='me', maxResults=num_messages).execute()
		messages = results.get('messages', [])
		return messages
	except HttpError as error:
		print(f'hey {error}')


def get_message_data(message_id, credentials):
	subject = ""
	body_string_b64 = ""
	try:
		service = build('gmail', 'v1', credentials=credentials)
		results = service.users().messages().get(userId='me', id=message_id).execute()
		subject = get_subject(results)
		utf_body_string = get_body(results)
		return (subject, utf_body_string)
	except Exception as e:
		print(e)
		return None

def get_subject(gmail_response):
	headers = gmail_response['payload']['headers']
	subject = [header['value'] for header in headers if header['name']=="Subject"]
	return subject[0]


def get_body(gmail_response):
	body_string_b64 = gmail_response['payload']['parts'][0]['body']['data']
	#Tt seems like the below line is unnecessary. At least, in simple plain-text cases.
	#It simply returns the same thing as the body_string_b64 (perhaps Gmail provides it already encoded)
	#TODO: double check on harder cases and close this out.
	#encoded_string = body_string_b64.encode('UTF8') 
	b64_urlsafe_decoded = base64.urlsafe_b64decode(body_string_b64)
	return b64_urlsafe_decoded.decode('UTF-8')
'''

def main():
	gmail = Gmail_Wrapper()
	messages = gmail.get_messages()
	for message in messages:
		print(message[0])
	print(messages[0][1])
	'''
	creds = authenticate()
	messages = get_messages_list(creds)
	messages_arr = []
	for message in messages:
		info_tuple = get_message_data(message['id'], creds)
		if info_tuple is not None:
			messages_arr.append(info_tuple)
	return messages_arr'''


def test_decoding_option():
	tough_case_id = "183619badc73cf46"
	easy_case_id = "183619643e11d0a4"
	another_case = "183617ba5cbb208c"
	creds = authenticate()
	subject, body = get_message_data(easy_case_id, creds)
	print(subject, body)


def test_get_recent_messages():
	creds = authenticate()
	messages = get_messages_list(creds, num_messages=5)
	for message in messages:
		print(message['id'])


def test_send_email():
	gmail = Gmail_Wrapper()
	gmail.send_email("subj", "bod", ["jumpstart.onboard@gmail.com"])


def test_format_recipients():
	gmail = Gmail_Wrapper()
	recips = ["a@yahoo.com", "b@gmail.com", "c@lycos.com"]
	formatted = gmail.format_recipients(recips)
	print(formatted)



test_send_email()