from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django import forms

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from . models import User
from . forms import RegistrationForm, CustomerSignUpForm
from . decorators import customer_required, employee_required, admin_required


# Create your views here.

class RegistrationView(CreateView):
	template_name = 'registration/register.html'
	form_class = RegistrationForm

	def get_context_data(self, *args, **kwargs):
		context = super(RegistrationView, self).get_context_data(*args, **kwargs)
		context['next'] = self.request.GET.get('next')
		return context

	def get_success_url(self):
		next_url = self.request.POST.get('next')
		success_url = reverse('login')
		if next_url:
			success_url += '?next={}'.format(next_url)

		return success_url


@login_required
@customer_required
def customer_home(request):
	context = {}
	return render(request, 'accounts/customer_home.html', context)


class CustomerSignUpView(CreateView):
	model = User
	form_class = CustomerSignUpForm
	template_name = 'accounts/customer_signup.html'

	def get_context_data(self, **kwargs):
		kwargs['status'] = 'customer'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('customer-home')	



