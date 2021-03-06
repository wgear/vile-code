#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.mail import send_mail, send_mass_mail
from django.template import loader
from django.core.urlresolvers import reverse


def absreverse(reverse_name, *args, **kwargs):
    return 'http://www.hashorg.com{}'.format(
        reverse(reverse_name, *args, **kwargs)
    )


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


class TemplateEmail(object):
    def __init__(self, subject, from_email, to_emails, template, context={}):
        tpl = loader.get_template(template)
        self.sender = Email(subject, from_email, to_emails, tpl.render(context=context), True)

    def send(self):
        return self.sender.send()