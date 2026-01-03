from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "registration_number",
            "password",
        ]

    def clean_registration_number(self):
        reg_no = self.cleaned_data.get("registration_number")

        if User.objects.filter(registration_number=reg_no).exists():
            raise forms.ValidationError(
                "This registration number is already registered."
            )

        return reg_no

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Passwords do not match")

        return cleaned_data
