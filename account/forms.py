from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length = 60,help_text="required")

    class Meta:
        model = Account

        fields = ('email','username','password1','password2')

class AccountAuthForm(forms.ModelForm):
    #
    password =  forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields =('email','password')

    def clean(self):
        # this is like a interceptor. it should run before form should do it's thing
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login")

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model =Account

        fields=('email','username')

    #Instead of doing clean we can do cleamn foor email as well
    #and
    # the user who is trying to update the information should not conflict with the existing username and email therefor below
    # functions will make sure both params should always be unique
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            # this should check that this email dooesnt equals to the other email which alreadyh exists in the database
            try:
                # checkcing if this account exists
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("Email '%s' already in use" %account)
    
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            # this should check that this email dooesnt equals to the other email which alreadyh exists in the database
            try:
                # checkcing if this account exists
                account = Account.objects.exclude(pk=self.instance.pk).get(email=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError("USername '%s' already in use" %account.username)