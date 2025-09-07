# # accounts/forms.py
# from django import forms
# from .models import Account, UserProfile

# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Enter Password',
#             'class': 'form-control'
#         })
#     )
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Confirm Password',
#             'class': 'form-control'
#         })
#     )
#     referral_code = forms.CharField(
#         required=False, 
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Referral Code (optional)',
#             'class': 'form-control'
#         })
#     )

#     class Meta:
#         model = Account
#         fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']  # Removed referral_code from here

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password and confirm_password and password != confirm_password:
#             raise forms.ValidationError("Passwords do not match!")
        
#         return cleaned_data

#     def clean_email(self):
#         """Validate email uniqueness"""
#         email = self.cleaned_data.get('email')
#         if email and Account.objects.filter(email=email).exists():
#             raise forms.ValidationError("An account with this email already exists!")
#         return email

#     def clean_password(self):
#         """Validate password strength"""
#         password = self.cleaned_data.get('password')
#         if password and len(password) < 8:
#             raise forms.ValidationError("Password must be at least 8 characters long!")
#         return password

#     def clean_phone_number(self):
#         """Validate phone number"""
#         phone_number = self.cleaned_data.get('phone_number')
#         if phone_number and len(phone_number) < 10:
#             raise forms.ValidationError("Please enter a valid phone number!")
#         return phone_number

#     def clean_referral_code(self):
#         """Validate referral code if provided"""
#         referral_code = self.cleaned_data.get('referral_code')
#         if referral_code:
#             if not Account.objects.filter(referral_code=referral_code).exists():
#                 raise forms.ValidationError("Invalid referral code!")
#         return referral_code

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['first_name'].widget.attrs.update({
#             'placeholder': 'Enter First Name',
#             'class': 'form-control'
#         })
#         self.fields['last_name'].widget.attrs.update({
#             'placeholder': 'Enter Last Name',
#             'class': 'form-control'
#         })
#         self.fields['phone_number'].widget.attrs.update({
#             'placeholder': 'Enter Phone Number',
#             'class': 'form-control'
#         })
#         self.fields['email'].widget.attrs.update({
#             'placeholder': 'Enter Email Address',
#             'class': 'form-control'
#         })


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = ('first_name', 'last_name', 'phone_number')

#     def clean_phone_number(self):
#         """Validate phone number"""
#         phone_number = self.cleaned_data.get('phone_number')
#         if phone_number and len(phone_number) < 10:
#             raise forms.ValidationError("Please enter a valid phone number!")
#         return phone_number

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['first_name'].widget.attrs.update({
#             'placeholder': 'First Name',
#             'class': 'form-control'
#         })
#         self.fields['last_name'].widget.attrs.update({
#             'placeholder': 'Last Name',
#             'class': 'form-control'
#         })
#         self.fields['phone_number'].widget.attrs.update({
#             'placeholder': 'Phone Number',
#             'class': 'form-control'
#         })


# class UserProfileForm(forms.ModelForm):
#     profile_picture = forms.ImageField(
#         required=False, 
#         error_messages={'invalid': "Please upload a valid image file"}, 
#         widget=forms.FileInput(attrs={
#             'class': 'form-control-file',
#             'accept': 'image/*'
#         })
#     )

#     class Meta:
#         model = UserProfile
#         fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

#     def clean_profile_picture(self):
#         """Validate profile picture"""
#         picture = self.cleaned_data.get('profile_picture')
#         if picture:
#             # Check file size (max 5MB)
#             if picture.size > 5 * 1024 * 1024:
#                 raise forms.ValidationError("Image file too large ( > 5MB )")
            
#             # Check file type
#             if not picture.content_type.startswith('image/'):
#                 raise forms.ValidationError("Please upload a valid image file")
        
#         return picture

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['address_line_1'].widget.attrs.update({
#             'placeholder': 'Address Line 1',
#             'class': 'form-control'
#         })
#         self.fields['address_line_2'].widget.attrs.update({
#             'placeholder': 'Address Line 2 (Optional)',
#             'class': 'form-control'
#         })
#         self.fields['city'].widget.attrs.update({
#             'placeholder': 'City',
#             'class': 'form-control'
#         })
#         self.fields['state'].widget.attrs.update({
#             'placeholder': 'State',
#             'class': 'form-control'
#         })
#         self.fields['country'].widget.attrs.update({
#             'placeholder': 'Country',
#             'class': 'form-control'
#         })


# class PasswordResetForm(forms.Form):
#     """Form for password reset"""
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'placeholder': 'Enter your email address',
#             'class': 'form-control'
#         })
#     )

#     def clean_email(self):
#         """Validate email exists"""
#         email = self.cleaned_data.get('email')
#         if email and not Account.objects.filter(email__iexact=email).exists():
#             raise forms.ValidationError("No account found with this email address!")
#         return email


# class SetPasswordForm(forms.Form):
#     """Form for setting new password"""
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Enter new password',
#             'class': 'form-control'
#         })
#     )
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Confirm new password',
#             'class': 'form-control'
#         })
#     )

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password and confirm_password:
#             if len(password) < 8:
#                 raise forms.ValidationError("Password must be at least 8 characters long!")
            
#             if password != confirm_password:
#                 raise forms.ValidationError("Passwords do not match!")
        
#         return cleaned_data


# class ChangePasswordForm(forms.Form):
#     """Form for changing password"""
#     current_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Enter current password',
#             'class': 'form-control'
#         })
#     )
#     new_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Enter new password',
#             'class': 'form-control'
#         })
#     )
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Confirm new password',
#             'class': 'form-control'
#         })
#     )

#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)

#     def clean_current_password(self):
#         """Validate current password"""
#         current_password = self.cleaned_data.get('current_password')
#         if current_password and not self.user.check_password(current_password):
#             raise forms.ValidationError("Current password is incorrect!")
#         return current_password

#     def clean(self):
#         cleaned_data = super().clean()
#         new_password = cleaned_data.get('new_password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if new_password and confirm_password:
#             if len(new_password) < 8:
#                 raise forms.ValidationError("Password must be at least 8 characters long!")
            
#             if new_password != confirm_password:
#                 raise forms.ValidationError("New passwords do not match!")
        
#         return cleaned_data


# accounts/forms.py
from django import forms
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'form-control'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })
    )
    referral_code = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Referral Code (optional)',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Account.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists!")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long!")
        return password

    def clean_referral_code(self):
        referral_code = self.cleaned_data.get('referral_code')
        if referral_code and not Account.objects.filter(referral_code=referral_code).exists():
            raise forms.ValidationError("Invalid referral code!")
        return referral_code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter First Name',
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter Last Name',
            'class': 'form-control'
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter Phone Number',
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter Email Address',
            'class': 'form-control'
        })

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and len(phone_number) < 10:
            raise forms.ValidationError("Please enter a valid phone number!")
        return phone_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name',
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last Name',
            'class': 'form-control'
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Phone Number',
            'class': 'form-control'
        })

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False, 
        error_messages={'invalid': "Please upload a valid image file"}, 
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Check file size (max 5MB)
            if picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            
            # Check file type
            if not picture.content_type.startswith('image/'):
                raise forms.ValidationError("Please upload a valid image file")
        
        return picture

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address_line_1'].widget.attrs.update({
            'placeholder': 'Address Line 1',
            'class': 'form-control'
        })
        self.fields['address_line_2'].widget.attrs.update({
            'placeholder': 'Address Line 2 (Optional)',
            'class': 'form-control'
        })
        self.fields['city'].widget.attrs.update({
            'placeholder': 'City',
            'class': 'form-control'
        })
        self.fields['state'].widget.attrs.update({
            'placeholder': 'State',
            'class': 'form-control'
        })
        self.fields['country'].widget.attrs.update({
            'placeholder': 'Country',
            'class': 'form-control'
        })