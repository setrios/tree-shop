from django import forms
from .models import ShippingAddress, Order

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ('user',)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'status', 'shipping_address')  # We'll handle shipping_address separately

class OrderPlacementForm(forms.Form):
    """Combined form for order placement with shipping address"""
    
    # Dropdown for logged-in users (will be hidden for anonymous)
    existing_address = forms.ModelChoiceField(
        queryset=ShippingAddress.objects.none(),
        required=False,
        empty_label="-- Enter New Address --",
        widget=forms.Select(attrs={'id': 'id_existing_address'})
    )
    
    # Shipping address fields
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)
    address1 = forms.CharField(max_length=255, required=False, label="Address Line 1")
    address2 = forms.CharField(max_length=255, required=False, label="Address Line 2")
    city = forms.CharField(max_length=255, required=False)
    state = forms.CharField(max_length=255, required=False)
    postal_code = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=255, required=False)
    phone = forms.CharField(max_length=20, required=False)
    special_instructions = forms.CharField(widget=forms.Textarea, required=False)
    
    # Order fields
    payment_provider = forms.ChoiceField(
        choices=Order.PAYMENT_PROVIDER_CHOICES,
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            # Show existing addresses for logged-in users
            self.fields['existing_address'].queryset = ShippingAddress.objects.filter(user=user)
        else:
            # Hide the dropdown for anonymous users
            self.fields['existing_address'].widget = forms.HiddenInput()
    
    def clean(self):
        cleaned_data = super().clean()
        existing_address = cleaned_data.get('existing_address')
        
        # If no existing address selected, validate that all required fields are filled
        if not existing_address:
            required_fields = ['first_name', 'last_name', 'address1', 'city', 
                             'state', 'postal_code', 'country', 'phone']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required.')
        
        return cleaned_data