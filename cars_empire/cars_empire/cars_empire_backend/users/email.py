from djoser.email import ActivationEmail as DjoserActivationEmail

class CustomActivationEmail(DjoserActivationEmail):
    template_name = "email/activation.html"
    template_name_txt = "email/activation.txt"
    subject_template_name = "email/activation_subject.txt"

    def send(self, to, *args, **kwargs):
        print("=== DJOSER ACTIVATION EMAIL SUBJECT ===")
        print(self.subject)
        print("=== DJOSER ACTIVATION EMAIL BODY (TXT) ===")
        print(self.body)
        return super().send(to, *args, **kwargs) 