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

'''
This class iterates in reverse chronological order: oldest messages first.
'''

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
		self.history_id = self.load_history_id()
		if self.history_id == 0:
			self.history_id = self.get_history_id(self.get_latest_message())
			self.update_history_id(self.history_id)

	def close(self):
		self.update_history_id()

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

	#Will return None if errors (including trying to get data on a deleted email)
	def get_message_data(self, message_id):
		try:
			results = self.service.users().messages().get(userId='me', id=message_id).execute()
			return results
		except Exception as e:
			print(e)
			return None

	def get_messages(self, num_messages=5):
		message_ids_list = self.get_message_ids(num_messages)
		messages = []
		for message_id in message_ids_list:
			message_data = self.get_message_data(message_id['id'])
			subject = self.get_subject(message_data)
			body = self.get_body(message_data)
			messages.append((subject, body))
		return messages


	def get_latest_message(self):
		message_id = self.get_message_ids(1)[0]['id']
		print(message_id)
		return self.get_message_data(message_id)

		
	#History data is given in reverse chronological order (oldest first, lowest history id first) by the API.
	def get_history_data(self, history_id):
		results = self.service.users().history().list(userId='me', startHistoryId=history_id, 
			historyTypes = ['messageAdded']).execute()
		return results['history']

	#This method will return results that contain deleted emails! There may be a way to avoid that
	#via checking labels. TODO.
	def get_messages_history(self, history_id=None):
		if history_id is None:
			history_id = self.history_id
		history_data = self.get_history_data(history_id)
		messages = []
		for message in history_data:
			message_id = message['messages'][0]['id']
			message_data = self.get_message_data(message_id)
			if message_data is None:
				continue
			subject = self.get_subject(message_data)
			body = self.get_body(message_data)
			messages.append((subject, body))
			history_id = self.get_history_id(message_data)
		#self.update_history_id(history_id)
		return messages

	def get_history_id(self, gmail_response):
		return gmail_response['historyId']

	def load_history_id(self):
		#Load id from json file if exists.
		#If not, create file and then set to placeholder value of 0. This placeholder will be updated when 
		#new messages are fetched.
		if os.path.exists('history_id.json'):
			file = open('history_id.json')
			data = json.load(file)
			file.close()
			return data['history_id']
		else:
			self.update_history_id(0)
			return 0

	def update_history_id(self, new_history_id=None):
		if new_history_id is None:
			new_history_id = self.history_id
		file = open('history_id.json', 'w')
		data = dict()
		data['history_id'] = new_history_id
		json_data = json.dumps(data)
		file.write(json_data)
		file.close()


	def get_subject(self, gmail_response):
		print(gmail_response)
		headers = gmail_response['payload']['headers']
		subject = [header['value'] for header in headers if header['name']=="Subject"]
		return subject[0]


	def get_body(self, gmail_response):
		#if the email is only plain text, then it will not have the parts section.
		#if the email has multiple parts, then the first 'body' in 'payload' doesn't have 'data'.
		if "parts" in gmail_response['payload']:
			body_string_b64 = gmail_response['payload']['parts'][0]['body']['data']
		else:
			body_string_b64 = gmail_response['payload']['body']['data']
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
			encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
			created_message = {
				'raw': encoded_message
			}
			sent_message = self.service.users().messages().send(userId='me', body=created_message).execute()
		except HttpError as error:
			print(f'Error: {error}')

	def format_recipients(self, email_recipients_list):
		return ", ".join(email_recipients_list)

