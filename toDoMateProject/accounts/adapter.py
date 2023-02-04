from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        if "localhost" in context['activate_url']:
            context['activate_url'] = context['activate_url'].replace("localhost", "3.38.100.94")
        msg = self.render_mail(template_prefix, email, context)
        msg.send()
