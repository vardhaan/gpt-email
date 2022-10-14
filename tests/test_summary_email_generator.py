import unittest
from src.summary_email_generator import *

class Test_Formatted_Summary_Email(unittest.TestCase):

    def setUp(self):
        self.email_gen = Formatted_Summary_Email_Generator()
        self.emails_dict = {"tldr":"", "must_read":[], "nice_to_know":[], "unimportant":[]}


    def test_must_read_section(self):
        example_must_read_emails = [("subj_a", "bod", "1", "--point a\n--point b\n--point c"), ("subj_b", "bod", "2", "--point d\n--point e\n--point f")]
        example_nice_to_know_emails = [("subj_c", "bod", "3", "--point g\n--point h\n--point i"), ("subj_d", "bod", "4", "--point j\n--point k\n--point l")]
        self.emails_dict['must_read'] = example_must_read_emails
        self.emails_dict['nice_to_know'] = example_nice_to_know_emails
        email = self.email_gen.generate_email(self.emails_dict)
        print(email)
        self.assertTrue((email is not None))
        

