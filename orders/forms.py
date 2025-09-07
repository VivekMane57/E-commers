from django import forms

class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=50)
    address_line_1 = forms.CharField(max_length=50)
    address_line_2 = forms.CharField(max_length=50, required=False)
    country = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    order_note = forms.CharField(widget=forms.Textarea, required=False)