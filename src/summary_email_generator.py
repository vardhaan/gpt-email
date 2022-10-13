

class Summary_Email_Generator():

    def generate_email(emails_dict):
        pass

class Formatted_Summary_Email_Generator(Summary_Email_Generator):
    '''
    This class creates a nicely formatted summary email.
    It has a super TL;DR at the top. Then it has a summary (and links) to the must-read emails. Then summaries of the nice-to-know emails. Then a list of the
    unimportant emails.
    '''

    def generate_email(self, emails_dict):
        pass

    def generate_tldr(self):
        #Ideally, this method would only talk about the must-read emails (with more important nice-to-know emails sprinkled in if needed).
        pass

    '''
    Puts subject of email (that is also link to email), followed by summary of email.

    Inputs:
    - must_read_list: list of (subj, body, email_id, summary) tuples'''
    def generate_must_read_section(self, must_read_list):
        pass




    def format_url(self, url, inner_text):
        url_format = '<a href="{}">{}</a>'
        url = url_format.format(url, inner_text)
        return url
