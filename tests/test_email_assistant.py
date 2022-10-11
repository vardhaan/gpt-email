import unittest
from src.email_assistant import *
from src.gpt import *


class TestPrioritizer(unittest.TestCase):

	def setUp(self):
		self.prioritizer = Prioritizer()
		self.summarizer = Summarizer()
		self.gpt = GPT_Wrapper()

	def test_prioritizer_sorts(self):
		emails = [("a", "b"), ("C", "D"), ("E", "F")]
		sorted_emails = self.prioritizer.prioritize_emails(emails, self.gpt.send_completion_request)
		self.assertTrue(self.is_sorted(sorted_emails))

	def test_prompt_import(self):
		self.assertTrue((self.prioritizer.prompt is not None))

	def is_sorted(self, col):
		return all(col[i][2] >= col[i+1][2] for i in range(len(col)-1))

	def open_sample_data(self, sample_file):
		file = open("sample_data/" + sample_file)
		subject = file.readline().split("Subject: ")[-1]
		body = file.read().split("Body: ")[-1]
		return (subject, body)


if __name__=='__main__':
	unittest.main()