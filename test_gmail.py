import gmail_api



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

tester()
