from django import forms
from django.shortcuts import render, reverse, redirect

from django.core.validators import MinLengthValidator

from .models import CUSTOMER, states, county, payam

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django.forms import utils

my_default_errors = {
    'required': 'This field is required',
    'invalid': 'Enter a valid value'
}


class MSISDNForm(forms.Form):
    msisdn = forms.CharField(min_length=12, max_length=12, help_text="Example: 211912399501",
                             error_messages=my_default_errors,
                             widget=forms.TextInput(attrs={'placeholder': '211912399501'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column('msisdn', css_class='form-group col-3 text-black-50 font-weight-bold mt-5 ml-5'),
            Submit('submit', 'Get One-Time-Password (OTP)',
                   css_class='form-group font-weight-bold col-sm-6 col-md-4 col-lg-4'),
        )


class OTPFORM(forms.Form):
    msisdn = forms.CharField(max_length=12,
                             required=False)
    # otp1 = forms.CharField(max_length=6)
    otp = forms.CharField(max_length=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column('msisdn',
                   css_class='form-group  col mx -3 mt-3 mb-5 text-center text-light card-body bg-success bg.gradient'),
            Column('otp', css_class='form-group col-4 mx-3 mb-5 text-black-50 font-weight-bold mt-5 ml-5'),
            Row(
                Submit('submit', 'Validate and Give Details', css_class='form-group col mt-3 mx-3 font-weight-bold '),
            ),
            Row(
                Submit('cancel', 'CANCEL', css_class='form-group mt-3 mx-3 col btn-warning ',
                       onclick="window.location.href = '{}';".format(reverse('cancel'))
                       ),
            ),
        )


import datetime


class CustomerForm(forms.ModelForm):
    """Form definition for MODELNAME."""
    confirmed = forms.BooleanField(help_text="I confirm all details provided are true", required=True)
    ID_PROOF = forms.ImageField()
    ID_PROOF.widget.attrs.update({'accept': 'image/*'})
    ID_NUMBER = forms.CharField(min_length=6, max_length=12, error_messages=my_default_errors)
    DOB = forms.DateField(widget=forms.SelectDateWidget(
        years=list(range(datetime.datetime.today().year - 95, datetime.datetime.today().year - 18))))

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = CUSTOMER
        fields = "__all__"
        widgets = {
            'gender': forms.RadioSelect,
            # 'DOB': forms.DateInput(format=('%d/%b/%Y'),
            #                                  attrs={'class': 'form-control', 'placeholder': 'Select a date',
            #                                         'type': 'date'}),
            'MOBILE_NUMBER': forms.HiddenInput,
            # 'ID_PROOF':attrs={'accept':'image/*'},
        }

    def form_save(self, msisdn):
        print(' IN SAVE')
        self.fields['MOBILE_NUMBER'] = msisdn

        return super(CustomerForm, self).save()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # id_field = self.fields['ID_NUMBER']
        # id_field.validators.append(MinLengthValidator(limit_value=6,message="ID number length should be minimum 6 Characters"))
        # print('INTIAL')
        # print (msisdn)
        self.helper.labels_uppercase = True
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-2'
        self.helper.layout = Layout(
            Column('MOBILE_NUMBER'),
            Row(
                Column('LAST_NAME', css_class='form-group col mb-4 mt-3 text-black-50 font-weight-bold'),
            ),
            Row(
                Column('FIRST_NAME', css_class='form-group col mb-4 mt-3 text-black-50 font-weight-bold'),
                Column('SECOND_NAME', css_class='form-group col mb-4 mt-3 text-black-50 font-weight-bold'),
                Column('THIRD_NAME', css_class='form-group col mb-4 mt-3 text-black-50 font-weight-bold'),

                css_class='form-row  '
            ),
            Row(
                Column('ID_TYPE', css_class='form-group col mb-4 mt-3  text-black-50 font-weight-bold'),
                Column('ID_NUMBER', css_class='form-group col  mb-4 mt-3 text-black-50 font-weight-bold'),
                Column(css_class='form-group col  mb-4 mt-3 text-black-50 font-weight-bold'),
                css_class='form-row '
            ),
            Row(
                Column('STATE', css_class='form-group col-md-4 mb-4 mt-3  text-black-50 font-weight-bold'),
                Column('COUNTY', css_class='form-group col-md-4 mb-4 mt-3  text-black-50 font-weight-bold'),
                Column('PAYAM', css_class='form-group col-md-4 mb-4 mt-3  text-black-50 font-weight-bold'),
                css_class='form-row '
            ),
            Row(
                Column('CITY', css_class='form-group col-md-4 mb-4 mt-3  text-black-50 font-weight-bold'),
                Column('BOMA', css_class='form-group col-md-4 mb-4 mt-3  text-black-50 font-weight-bold'),
                Column('ADDRESS', css_class='form-group col-md-4 mb-4  mt-3 text-black-50 font-weight-bold'),
                css_class='form-row '
            ),
            Row(
                Column('gender', css_class='form-group col-md-4 mb-4 mt-3  text-black-50 font-weight-bold'),
                Column('DOB', css_class='form-group col-md-4  mb-4 mt-3  text-black-50 font-weight-bold'),
                Column(css_class='form-group col-md-4  mb-4 mt-3  text-black-50 font-weight-bold'),
            ),
            Row(
                Column('COUNTRY', css_class='form-group col-sm mt-3 text-black-50 font-weight-bold'),
                Column('ID_PROOF', css_class='form-group col-sm mt-3 text-black-50 font-weight-bold'),
                Column('confirmed', css_class='form-group col-sm mt-3 mb-5 text-black-50 font-weight-bold'),
                css_class='form-row '
            ),

            Row(
                Submit('submit', 'SUBMIT', css_class='form-group my-3 col mx-3 bg-success font-weight-bold'),
            ),
            Row(
                Submit('cancel', 'CANCEL', css_class='form-group my-3 col mx-3 bg-warning  font-weight-bold',
                       onclick="window.location.href = '{}';".format(reverse('cancel'))
                       ), css_class='row g-3'),
        )
        self.fields['COUNTY'].queryset = county.objects.none()
        self.fields['PAYAM'].queryset = payam.objects.none()
        self.fields['STATE'].queryset = states.objects.all()

        if 'STATE' in self.data:
            try:
                STATE = int(self.data.get('STATE'))
                # print('STATE IS ' + str(STATE))
                self.fields['COUNTY'].queryset = county.objects.filter(states=STATE).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['COUNTY'].queryset = self.instance.states.county_set.order_by('name')
        if 'COUNTY' in self.data:
            try:
                COUNTY = self.data.get('COUNTY')
                STATE = self.data.get('STATE')
                self.fields['PAYAM'].queryset = payam.objects.filter(county=COUNTY).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['PAYAM'].queryset = self.instance.county.payam_set.order_by('name').order_by('name')
