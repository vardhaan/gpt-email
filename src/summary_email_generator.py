

class Summary_Email_Generator():

    def generate_email(self, emails_dict):
        pass

    def load_template(self, template_file_name):
        file = open('email_templates/' + template_file_name)
        return file.read()

class Formatted_Summary_Email_Generator(Summary_Email_Generator):
    '''
    This class creates a nicely formatted summary email.
    It has a super TL;DR at the top. Then it has a summary (and links) to the must-read emails. Then summaries of the nice-to-know emails. Then a list of the
    unimportant emails.
    '''

    def generate_email(self, emails_dict):
        '''Turns a dict of email tuples into a formatted html email string to be sent as a summary email.
        
        Inputs:
        - emails_dict: a dict (with "tldr", "must_read", "nice_to_know", and "unimportant" keys) whose values are lists of tuples. Each tuple is (email_subject, email_body, email_id, email_summary) of types (str, str, str, str).
        
        Outputs:
        - email: a string of the email in html format, ready to be sent'''
        template = self.load_template('simple_template.html')
        tldr = self.generate_tldr(emails_dict['tldr'])
        must_read = self.generate_section(emails_dict['must_read'], user_email_address="jumpstart.onboard@gmail.com", must_read=True)
        nice_to_know = self.generate_section(emails_dict['nice_to_know'])
        unimportant = self.generate_section(emails_dict['unimportant'])
        email = template.format(tldr, must_read, nice_to_know, unimportant)
        return email

    def generate_tldr(self, tldr):
        #We can assume the tldr is in "-" bullet point format.
        return ""
 
    def generate_section(self, email_list, user_email_address=None, must_read=False):
        '''
        Puts subject of email (that is also link to email), followed by summary of email.
        Each email is a bullet point (with email link), then the summary is a nested list after that.
        We assume that the summaries are in "--" bullet point format.

        Inputs:
        - must_read_list: list of (subj, body, email_id, summary) tuples'''
        section_email_string = "<ul>"
        first_iter = True
        for email in email_list:
            summary = email[3]
            email_html_string = self.format_summary_html(summary)
            if must_read:
                #must_read section also contains the subject of each individual email, which also serves as a link to that email.
                subject = email[0]
                summarized_email_url = self.generate_email_id_url(email[2], user_email_address)
                subject_html = self.format_url_in_html(summarized_email_url, subject+":")
                email_html_string = "<li>" + subject_html + "<ul>" + email_html_string + "</ul></li>"
                if first_iter is False:
                    email_html_string = "</br>" + email_html_string
                first_iter = False
            section_email_string = section_email_string + email_html_string
        return section_email_string + "</ul>"


    def format_summary_html(self, summary):
        '''Assumes summary is a string containing multiple bullet point sentences (may or may not contain periods).
        This method returns a html-formatted string of those bullet points'''
        summary_points = summary.split("--")
        summary_string = ""
        for point in summary_points:
            clean_point = point.strip()
            if len(clean_point)>0:
                summary_string = summary_string + "<li>" + clean_point + "</li>"
        return summary_string

    def format_url_in_html(self, url, inner_text):
        url_format = '<a href="{}">{}</a>'
        url = url_format.format(url, inner_text)
        return url

    def generate_email_id_url(self, email_id, user_email_address):
        #Standard url for email: https://mail.google.com/mail/u/0/#inbox/FMfcgzGqQmZzRxGTcKXgNmbqxtpTKxfq
        #If we replace the "0" with the full email address of the user, then it will load the right inbox.
        url_standard = "https://mail.google.com/mail/u/{}/#inbox/{}"
        return url_standard.format(user_email_address, email_id)

