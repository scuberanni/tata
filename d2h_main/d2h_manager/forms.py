
from django.forms import ModelForm
from django import forms
from . models import product_master,retailer_master,box_master,product,to_ret_product,sale_product,sale_to_ret_product,box_product
from .models import box_retailer_master,ret_ret



class Pr_Form(ModelForm):
      class Meta:
            model=product_master
            fields='__all__'

class ret_Form(ModelForm):
      class Meta:
            model=retailer_master
            fields='__all__'  

class box_Form(ModelForm):
      class Meta:
            model=box_master
            fields='__all__'  

class BoxProductForm1(ModelForm):
    r_name = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))
    woc_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    class Meta:
        model = box_product
        fields = ['r_name','b_name', 'b_slno', 'b_vscno','woc_date','set']
        labels = {
            'r_name': 'Custom Label for Field 1',
            'b_name': 'Custom Label for Field 2',
            'b_slno': 'Custom Label for Field 3',
            'b_vscno': 'Custom Label for Field 4',
            'woc_date': 'Custom Label for Field 5',
            'set': 'Custom Label for Field 6',
        } 

class BoxProductForm(ModelForm):
    r_name = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))
    class Meta:
        model = box_product
        fields = ['r_name','b_name', 'b_slno', 'b_vscno']
        labels = {
            'r_name': 'Custom Label for Field 1',
            'b_name': 'Custom Label for Field 2',
            'b_slno': 'Custom Label for Field 3',
            'b_vscno': 'Custom Label for Field 4',
        }      

    def clean(self):
        cleaned_data = super().clean()
        b_slno = cleaned_data.get('b_slno')
        b_vscno = cleaned_data.get('b_vscno')

        # Check if b_slno already exists
        if b_slno and box_product.objects.filter(b_slno=b_slno).exists():
            self.add_error('b_slno', 'This b_slno already exists.')

        # Check if b_vscno already exists
        if b_vscno and box_product.objects.filter(b_vscno=b_vscno).exists():
            self.add_error('b_vscno', 'This b_vscno already exists.')

        return cleaned_data  
        
class BoxProductForm2(ModelForm):
    r_name = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))
    class Meta:
        model = box_product
        fields = ['r_name','b_name', 'b_slno', 'b_vscno']
        labels = {
            'r_name': 'Custom Label for Field 1',
            'b_name': 'Custom Label for Field 2',
            'b_slno': 'Custom Label for Field 3',
            'b_vscno': 'Custom Label for Field 4',
        }

class adjust_form(ModelForm):
    retailer = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))
    class Meta:
        model = to_ret_product
        fields = ['retailer']
        labels = {
            'retailer': 'Custom Label for Field 1',
        }

class BoxRetailerForm(ModelForm):
    retailer = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))
    class Meta:
        model = box_retailer_master
        fields = ['retailer', 'b_vcsno', 'add_date', 'sl_date'] 

                   

class ProductForm(ModelForm):
    class Meta:
        model = product
        fields = ['cable', 'lnb', 'dish', 'kit']
        labels = {
            'cable': 'Custom Label for Field 1',
            'lnb': 'Custom Label for Field 2',
            'dish': 'Custom Label for Field 3',
            'kit': 'Custom Label for Field 4',
        }  

class to_ret_Form(ModelForm):
    retailer = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))
    class Meta:
        model = to_ret_product
        fields = ['retailer', 'cable2', 'lnb2', 'dish2', 'kit2',]   
        labels = {
            'retailer': 'Custom Label for Field 1',
            'cable2': 'Custom Label for Field 2',
            'lnb2': 'Custom Label for Field 3',
            'dish2': 'Custom Label for Field 4',
            'kit2': 'Custom Label for Field 5',
        } 

class to_ret_Form2(ModelForm):
    retailer1 = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))
    retailer2 = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))
    quantity = forms.IntegerField(label='Quantity')

    class Meta:
        model = ret_ret
        fields = ['retailer1', 'retailer2', 'quantity']  # Include 'retailer' field twice
        labels = {
            'retailer1': 'Custom Label for Field 1',
            'retailer2': 'Custom Label for Field 2',
            'quantity': 'Custom Label for Field 3',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['retailer1'].queryset = retailer_master.objects.all().order_by('r_name')
        self.fields['retailer2'].queryset = retailer_master.objects.all().order_by('r_name')


class sale_ProductForm(ModelForm):
    class Meta:
        sl_date3 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
        model = sale_product
        fields = ['cable3', 'lnb3', 'dish3', 'kit3','sl_date3']
        labels = {
            'cable3': 'Custom Label for Field 1',
            'lnb3': 'Custom Label for Field 2',
            'dish3': 'Custom Label for Field 3',
            'kit3': 'Custom Label for Field 4',
            'sl_date3': 'Custom Label for Field 5',
        } 
          

class sale_to_ret_Form(ModelForm):
    retailer4 = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))
    class Meta:
        sl_date4 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
        model = sale_to_ret_product
        fields = ['retailer4', 'cable4', 'lnb4', 'dish4', 'kit4','sl_date4']
        labels = {
            'retailer4': 'Custom Label for Field 1',
            'cable4': 'Custom Label for Field 2',
            'lnb4': 'Custom Label for Field 3',
            'dish4': 'Custom Label for Field 4',
            'kit4': 'Custom Label for Field 5',
            'sl_date4': 'Custom Label for Field 6',
        } 

class RetailerForm(forms.Form):
    r_name = forms.ModelChoiceField(queryset=retailer_master.objects.all().order_by('r_name'))

      