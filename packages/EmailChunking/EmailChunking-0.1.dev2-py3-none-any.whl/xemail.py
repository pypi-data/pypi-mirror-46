from itertools import product
import json
import re
import string
import spacy

class XEmail:

    def __init__(self, text):
        self.text = self.custom_preprocessing(text)
        self.body = None
        self.signature = None
        self.salutation = None
        self.reply_text = None
        # Lets populate fields above
        self.parse(remove_quoted_statements=False)

    def custom_preprocessing(self, text):
        return text

    def parse(self, remove_quoted_statements=True):
        return self.text

    # automated_notation could be any labels or sections in the email giving special notation for
    # human readers of the email text. For example, email_text may start with "A message from your customer:"
    def strip_automated_notation(self, email_text):
        return email_text

    def get_reply_text(self, email_text):
        return ""

    def get_signature(self, email_text):
        return ""

    # todo: complete this out (I bit off a bit more than I could chew with this function. Will probably take a bunch
    #  of baysian stuff
    def is_word_likely_in_signature(self, word, text_before="", text_after=""):

        return False

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


if __name__ == "__main__":
    text = """Dear Team, We wish to terminate the above-mentioned mobile no. 9776 8479 with immediate effect. Kindly acknowledge and confirm upon termination. Margaret Wong Volvo Group Singapore (Pte) Ltd 152 Beach Road #32-00 Gateway East Singapore 189721 Email: margaret.wong@volvo.com This email message and any attachments may contain confidential information and may be privileged. If you are not the intended recipient or otherwise not authorized to receive this message, you are prohibited to use, copy, disclose or take any action based on this email or any information contained herein. If you are not the intended recipient, please advise the sender immediately by replying to this email and permanently delete this message and any attachments from your system."""
    eo = Email(str(text))
    print(eo.to_json())
