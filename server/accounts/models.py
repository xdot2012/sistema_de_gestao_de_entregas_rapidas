from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from meuapp.settings import PASSWORD_RESET_URL


class User(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = self.username.upper()
        self.email = self.email.upper()
        
        super(User, self).save(*args, **kwargs)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(PASSWORD_RESET_URL, reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )