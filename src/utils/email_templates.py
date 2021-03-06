
import auth.settings as settings
from django.template import loader


class EmailTemplate:

    def __init__(self, name, html_path, email_content, email_configuration_name, email_configuration_email_name) -> None:
        self.name = name
        self.html_path = html_path
        self.email_content = email_content
        self.email_configuration_name = email_configuration_name
        self.email_configuration_email_name = email_configuration_email_name

    def load_template(self):
        pass

    def __str__(self) -> str:
        return self.load_template()


class FollowUpEmailTemplate(EmailTemplate):

    def __init__(self, email_content, email_configuration_name, email_configuration_email_name, \
         logo_url=None, name="follow_up", html_path=settings.EMAIL_TEMPLATES_TYPES["follow_up"], website_url=None, reason_for_receiving=None) -> None:
        self.logo_url = logo_url
        self.reason_for_receiving = reason_for_receiving
        self.website_url = website_url
        super().__init__(name, html_path, email_content, email_configuration_name, email_configuration_email_name)

    def load_template(self):
        return loader.render_to_string(self.html_path, self.__dict__)