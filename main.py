from gmail_api import *
from gpt import *
from email_assistant import *




gmail = Gmail_Wrapper()
gpt = GPT_Wrapper()
summarizer = Summarizer()

messages = gmail.get_messages_history()
summary = summarizer.summarize_emails(messages, gpt.send_completion_request)
print(summary)