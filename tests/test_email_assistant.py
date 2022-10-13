import unittest
from src.email_assistant import *
from src.gpt import *


class TestPrioritizer(unittest.TestCase):

	def setUp(self):
		self.prioritizer = Prioritizer()
		self.summarizer = Summarizer()
		self.gpt = GPT_Wrapper()
		self.sample_data = self.open_sample_data('important_data_request.txt')

	def test_prioritizer(self):
		emails = [("a", "b"), ("C", "D"), ("E", "F")]
		sorted_emails = self.prioritizer.prioritize_emails(emails, self.gpt.send_completion_request)
		self.assertTrue(self.is_sorted(sorted_emails))

	def test_prompt_import(self):
		self.assertTrue((self.prioritizer.prompt is not None))

	def test_gpt_request_completes(self):
		subj, body = self.sample_data
		priority_response = self.prioritizer.handle_email(subj, body, self.gpt.send_completion_request)
		priority = self.prioritizer.find_priority_in_response(priority_response)
		print("Priority:", priority)
		self.assertTrue((priority==80))

	def test_priority_finder(self):
		cases = ["Final Answer. 90", "Final Answer. 90.", "90", "90.", "\n 90\n", "\n90.\n"]
		for case in cases:
			self.assertTrue((self.prioritizer.find_priority_in_response(case) == 90))

	def is_sorted(self, col):
		return all(col[i][2] >= col[i+1][2] for i in range(len(col)-1))

	def open_sample_data(self, sample_file):
		file = open("sample_data/" + sample_file)
		subject = file.readline().split("Subject: ")[-1]
		body = file.read().split("Body: ")[-1]
		file.close()
		return (subject, body)


if __name__=='__main__':
	unittest.main()