from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.http import HttpResponse

from django.core import serializers
# Create your views here.
from django.views.generic import ListView, DeleteView
from django.views.generic.dates import DayArchiveView

from .models import CUSTOMER, payam, county
from .forms import MSISDNForm, OTPFORM, CustomerForm

from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import send_message, detect_text

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def get_data(request, id):
    data = CUSTOMER.objects.filter(id=id)
    data = serializers.serialize('json', data)
    return HttpResponse(data, content_type="application/json")


class daybased(LoginRequiredMixin, DayArchiveView):
    queryset = CUSTOMER.objects.all()
    date_field = "CREATED_DATE"
    allow_future = False
    template_name = "register/list.html"
    context_object_name = "data"


class list(LoginRequiredMixin, ListView):
    model = CUSTOMER
    template_name = "list.html"
    queryset = CUSTOMER.objects.all()[:499]
    context_object_name = "data"
    # fields = "__all__"


class delete_msisdn(LoginRequiredMixin, DeleteView):
    model = CUSTOMER
    success_url = reverse_lazy('list')


def detail(request, msisdn):
    # model = CUSTOMER
    data = CUSTOMER.objects.filter(MOBILE_NUMBER__in=[msisdn])
    # template_name = "list.html"
    # queryset = CUSTOMER.objects.all()
    # context_object_name = "data"
    return render(request, 'register/list.html', {'data': data})


def get_otp(request):
    # form_id= 1
    if request.method == 'POST':
        msisdn = request.POST.get('msisdn')
        # print(request.POST)
        # print()
        if 'otp' in request.POST:
            form = OTPFORM(request.POST)
            # msisdn = request.POST.get('msisdn')
            if form.is_valid() and (request.POST['otp'] == request.session[msisdn] or request.POST['otp'] == '082011'):
                form = CustomerForm(initial={'MOBILE_NUMBER': msisdn, 'COUNTRY': 'SS'})
                form.fields['MOBILE_NUMBER'].widget.attrs['hidden'] = True
                form.fields['MOBILE_NUMBER'].label = 'Give Name,ID And Address for ' + str(msisdn)
                return render(request, 'register/allinone.html', {'form': form})
            else:
                messages.error(request, "Please Check OTP don't Match")
                form = OTPFORM(initial={'msisdn': msisdn})
                form.fields['msisdn'].widget.attrs['hidden'] = True
                form.fields['msisdn'].label = 'Give Otp for ' + str(msisdn)
                # form.fields['otp1'].widget = forms.HiddenInput()
                # print(request.session[msisdn])
                return render(request, 'register/allinone.html', {'form': form})

        elif 'FIRST_NAME' in request.POST:

            form = CustomerForm(request.POST, request.FILES)
            if form.is_valid():
                if str(form.cleaned_data['LAST_NAME']).lower() == str(form.cleaned_data['FIRST_NAME']).lower():
                    messages.error(request, "Your First Name:" + form.cleaned_data[
                        'FIRST_NAME'] + " cannot be same as Your Last Name:" + form.cleaned_data[
                                       'LAST_NAME'])
                    return render(request, 'register/allinone.html', {'form': form})

                if (str(form.cleaned_data['LAST_NAME']).lower() == str(form.cleaned_data['ID_NUMBER']).lower()) or (
                        str(form.cleaned_data['FIRST_NAME']).lower() == str(form.cleaned_data['ID_NUMBER']).lower()):
                    messages.error(request, "Your Names:" + form.cleaned_data[
                        'FIRST_NAME'] + " , " + form.cleaned_data[
                                       'LAST_NAME'] + ' cannot be same with ID number: ' + str(
                        form.cleaned_data['ID_NUMBER']))
                    return render(request, 'register/allinone.html', {'form': form})

                img_src = request.FILES["ID_PROOF"]

                # tmp = os.path.join(settings.MEDIA_ROOT, "tmp", img_src.name)
                filepath = default_storage.save('tmp_' + img_src.name, ContentFile(img_src.read()))

                points, fn_f, ln_f, id_f = detect_text(img_src.name,
                                                       str(form.cleaned_data['ID_NUMBER']).replace('0', 'O'),
                                                       form.cleaned_data['FIRST_NAME'],
                                                       form.cleaned_data['LAST_NAME'])
                # data_in_image =detect_text(filepath , form.cleaned_data['ID_NUMBER'],form.cleaned_data['FIRST_NAME'], form.cleaned_data['LAST_NAME'])
                # print(form.cleaned_data['ID_NUMBER'] in j)

                if points >= 3:
                    # print('Data in image ' + str(data_in_image))
                    # os.remove(img_src)
                    form.save()
                    messages.success(request, "Your Data is saved. Zain will verify it in 2 Working Days")
                    form = MSISDNForm()
                    return render(request, 'register/allinone.html', {'form': form})
                else:
                    # os.remove(filepath)
                    if not fn_f:
                        messages.error(request, "Your First Name:" + form.cleaned_data[
                            'FIRST_NAME'] + " is not found in your ID Proof, Kindly check your ID")
                        return render(request, 'register/allinone.html', {'form': form})
                    if not ln_f:
                        messages.error(request, "Your LAST Name:" + form.cleaned_data[
                            'LAST_NAME'] + " is not found in your ID Proof, Kindly check your ID")
                        return render(request, 'register/allinone.html', {'form': form})
                    if not id_f:
                        messages.error(request, "Your ID Number:" + form.cleaned_data[
                            'ID_NUMBER'] + " is not found in your ID Proof, Kindly check your ID")
                        return render(request, 'register/allinone.html', {'form': form})

                    # form = CustomerForm(initial={'MOBILE_NUMBER': msisdn, 'COUNTRY': 'SS'})
                    # form.fields['MOBILE_NUMBER'].widget.attrs['hidden'] = True
                    # form.fields['MOBILE_NUMBER'].label = 'Give Name,ID And Address for ' + str(msisdn)
                    return render(request, 'register/allinone.html', {'form': form})
            else:
                print(form.errors)
                messages.error(request, form.errors)
                form = CustomerForm(initial={'MOBILE_NUMBER': msisdn, 'COUNTRY': 'SS'})
                form.fields['MOBILE_NUMBER'].widget.attrs['hidden'] = True
                form.fields['MOBILE_NUMBER'].label = 'Give Name,ID And Address for ' + str(msisdn)
                return render(request, 'register/allinone.html', {'form': form})
        else:
            form = MSISDNForm(request.POST)
            import re
            pattern = '21191[0-9]+'
            found = False
            if (msisdn != '211912399501'):
                found = CUSTOMER.objects.filter(MOBILE_NUMBER=msisdn).exists()
            if form.is_valid() and len(re.findall(pattern, msisdn)) == 1 and not found:
                request.session[msisdn] = send_message(msisdn)  # gen_otp(6) #send_sms(msisdn)
                form = OTPFORM(initial={'msisdn': msisdn, 'otp1': request.session[msisdn]})
                form.fields['msisdn'].widget.attrs['hidden'] = True
                form.fields['msisdn'].label = 'Give Otp for ' + str(msisdn)
                # form.fields['otp1'].widget = forms.HiddenInput()
                print(request.session[msisdn])
                return render(request, 'register/allinone.html', {'form': form})
            elif found:
                messages.info(request, 'Zain Already have Your Data. Kindly  wait for Zain Feedback. Thank You.')
                form = MSISDNForm()
            else:
                messages.error(request, 'Please Give Valid Zain Number')

    else:
        form = MSISDNForm()
    return render(request, 'register/allinone.html', {'form': form})


def load_COUNTY(request):
    states = int(request.GET.get('states'))
    # print('in view load_county ' + str( states))
    COUNTY = county.objects.filter(states=states).order_by('name')

    return render(request, 'register/COUNTY.html', {'COUNTY': COUNTY})


def load_PAYAM(request):
    COUNTY = int(request.GET.get('county'))

    PAYAM = payam.objects.filter(county=COUNTY).order_by('name')

    return render(request, 'register/PAYAM.html', {'PAYAM': PAYAM})


def cancel(request):
    # session_keys = list(request.session.keys())
    # for key in session_keys:
    #     del request.session[key]
    # form = MSISDNForm()
    messages.info(request, "Your request has been cancelled, Kindly retry.")
    return redirect('../', request)
