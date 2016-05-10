#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.mail import send_mail, send_mass_mail


class Email(object):
    """
    Email sender
    """
    def __init__(self, subject, from_email, to_emails, message, html=True):
        self.subject = subject
        self.from_email = from_email
        self.to_emails = to_emails if type(to_emails) is list else [to_emails]
        self.message = message
        self.html = html

    def send(self):
        if len(self.to_emails) > 1:
            return send_mass_mail(self.make_tuple())

        return send_mail(
            subject=self.subject,
            message=self.message if not self.html else '',
            from_email=self.from_email,
            recipient_list=self.to_emails,
            html_message=self.message if self.html else None
        )

    def make_tuple(self):
        return (
            (self.subject, self.message, self.from_email, [element])
            for element in self.to_emails
        )
