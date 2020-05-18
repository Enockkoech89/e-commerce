from django.contrib import messages
from django.conf import settings
import stripe
import requests
import base64
import json
from datetime import datetime
from django.core. exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, View
from .forms import PaymentForm, UserUpdateForm, ProfileUpdateForm
from django.utils import timezone
from .models import Item, OrderItem, Order, BillingAddress, Payment, Free, Sinema
from .credentials import business_shortcode, lipa_na_mpesa_passkey, my_consumer_key, my_consumer_secret, my_number
from requests.auth import HTTPBasicAuth
from .forms import UserRegisterForm




stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# Create your views here.

class HomeView(ListView):
	model = Item
	paginate_by = 80
	template_name = 'home.html'
	ordering = ['-id']


class ProductDetailView(DetailView):
	model = Item
	template_name = 'item_detail.html'
	ordered = ['-item.ordered_date']


class OrderSummaryView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):

		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			context = {
				'object': order
			}
			return render(self.request, 'order_summary.html', context)
		except ObjectDoesNotExist:
			messages.error(self.request, "You do not have an order")
			return redirect("/")
		return render(self.request, 'order_summary.html')



class BillCheckoutView(CreateView):
	model = BillingAddress
	success_url = '/selector/'
	template_name = 'checkout.html'
	fields = ['school', 'school_address', 'school_code']
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


def payment_selector(request):
	return render(request, 'select.html')
	

class PaymentView(LoginRequiredMixin, View):
	

	def get(self, *args, **kwargs):

		p_form = PaymentForm()
		order=Order.objects.get(user=self.request.user, ordered=False)
		context = {
			'p_form': p_form,
			'order':order
		}

		return render(self.request, 'payment.html', context)

	def post(self, *args, **kwargs):
		order=Order.objects.get(user=self.request.user, ordered=False)
		order_amount = order.get_total()
		p_form = PaymentForm(self.request.POST or None)
		if p_form.is_valid():
			my_phone=p_form.cleaned_data.get('my_phone')
			mpesa_name=p_form.cleaned_data.get('m_pesa_name')
			payment = Payment(
				user = self.request.user,
				name = mpesa_name,
				phone = my_phone,
				amount = order_amount
			)

			payment.save()
			order.payment=payment
			order.save()
			messages.success(self.request, 'Thank you for choosing SchoolFlyx. We have received your request and we are currently reviewing your payment. Once we are done, we will activate the order (within 5 min). Ordered materials can be access in "Purchases" tab in the nav bar.')
		return redirect('home')
			
		# try:
		# 	order = Order.objects.get(user=self.request.user, ordered=False)
			# consumer_key = my_consumer_key
			# consumer_secret = my_consumer_secret
			# api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
			# r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
			# json_response = r.json()
			# # my_access_token=json_response['my_access_token']
			# timestamp = datetime.now()
			# formated_time = timestamp.strftime('%Y%m%d%H%M%S')
			# password_token = business_shortcode + lipa_na_mpesa_passkey + formated_time
			# encode_password = base64.b64encode(password_token.encode())
			# decoded_password = encode_password.decode('utf-8')
			# order_amount = order.get_total()
			# # decoded_pass = encoded_str.decode('utf-8')
			# # consumer_key = "my_consumer_key"
			# # consumer_secret = "my_consumer_secret"
			# api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

			# # r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
			# responce = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)).json()
			# myaccesstoken = responce['access_token']
			# access_token = myaccesstoken
			# api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
			# headers = { "Authorization": "Bearer %s" % access_token }
			# request = {
			# 		"BusinessShortCode": 174379,
			# 		"Password": decoded_password,
			# 		"Timestamp": formated_time,
			# 		"TransactionType": "CustomerPayBillOnline",
			# 		"Amount": order_amount,
			# 		"PartyA": my_phone,
			# 		"PartyB": 174379,
			# 		"PhoneNumber": my_phone,
			# 		"CallBackURL": "https://skoolflyx.com",
			# 		"AccountReference": "2884321",
			# 		"TransactionDesc": "pay fees"
			# }

			# response = requests.post(api_url, json = request, headers=headers)
			#   	# print (response.text)
						
		# 	payment = Payment(
		# 		user = self.request.user,
		# 		name = mpesa_name,
		# 		phone = my_phone,
		# 		amount = order_amount
		# 	)

		# 	payment.save()
		# 	order.payment=payment
		# 	order.save()
		# 	messages.success(self.request, 'Kindly check your phone for pin-prompt and complete the order.Once you have done that, we will review your transaction and once we are done, we will activate the order and you will be able to access the materials at Purchases tab in the nav bar.')
		# 	return redirect('home')
		# except:
		# 	messages.warning(self.request, 'Invalid payment selected')
		# 	return redirect('order-summary')

class Payment2View(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		
		return render(self.request, 'payment2.html')

	def post(self, *args, **kwargs):

		order = Order.objects.get(user=self.request.user, ordered=False)
		token = self.request.POST.get('stripeToken')
		amount_1 = int(order.dollar_total() * 100)
	

		try:
			charge = stripe.Charge.create(
		 		amount=amount_1,
		 		currency="usd",
		 		source=token,
		 		description="Payment from clients",
	 		)
			payment = Payment()
			payment.stripe_charge_id = charge['id']
			payment.user = self.request.user
			payment.amount = order.get_total()
			payment.save()

			order_items = order.items.all()
			order_items.update(ordered=True)
			for item in order_items:
				item.save()

			order.ordered = True
			order.payment = payment
			order.save()
			messages.success(self.request, 'Your have successfully placed an order. You can download the materials from the Purchases tab in the nav bar')
			return redirect('/')


		except stripe.error.CardError as e:
			body = e.json_body
			err  = body.get('error', {})
			messages.error(self.request, f"{err.get('message')}")
			return redirect('selector')
		except stripe.error.RateLimitError as e:
			messages.error(self.request, "Rate Limit Error")
			return redirect('selector')

		except stripe.error.InvalidRequestError as e:
			messages.error(self.request, "Invalid Parameters")
			return redirect('selector')
		  # Invalid parameters were supplied to Stripe's API
		  	
		except stripe.error.AuthenticationError as e:
			messages.error(self.request, "Not Authenticated")
			return redirect('selector')
		  # Authentication with Stripe's API failed
		  # (maybe you changed API keys recently)
		  	
		except stripe.error.APIConnectionError as e:
			messages.error(self.request, "Network Error")
			return redirect('selector')
		  # Network communication with Stripe failed
		  	
		except stripe.error.StripeError as e:
			messages.error(self.request, "Something went wrong. You were not charged. Please try again")
			return redirect('selector')
		  # Display a very generic error to the user, and maybe send
		  # yourself an email
		  	
		except Exception as e:
			messages.error(self.request, "A serious error occured. we have been notified")
			return redirect('selector')
		  # Something else happened, completely unrelated to Stripe
		  	
		
			
@login_required
def add_to_cart(request, pk):

	item = get_object_or_404(Item, pk=pk)
	order_item, created = OrderItem.objects.get_or_create(
		item = item,
		user = request.user,
		ordered = False
	)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order=order_qs[0]
		if order.items.filter(item__pk=item.pk).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, 'This item quantity was updated')
		else:
			messages.info(request, 'This item was added to your cart')
			order.items.add(order_item)
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(
			user = request.user,
			ordered_date = ordered_date
		)
		order.items.add(order_item)
		messages.info(request, 'This item was added to your cart')
	return redirect('order-summary')

@login_required
def remove_from_cart(request, pk):

	item = get_object_or_404(Item, pk=pk)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order=order_qs[0]
		if order.items.filter(item__pk=item.pk).exists():
			order_item = OrderItem.objects.filter(
				item = item,
				user = request.user,
				ordered = False,
			)[0]
			order.items.remove(order_item)
			messages.info(request, 'This item was removed from your cart')
			return redirect('order-summary')
			
		else:
			messages.info(request, 'This item was not in your cart')
			return redirect('order-summary')
	else:
		messages.info(request, 'You do not have an active order')
		return redirect('order-summary')


@login_required
def remove_single_item_from_cart(request, pk):

	item = get_object_or_404(Item, pk=pk)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order=order_qs[0]
		if order.items.filter(item__pk=item.pk).exists():
			order_item = OrderItem.objects.filter(
				item = item,
				user = request.user,
				ordered = False,
			)[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order.items.remove(order_item)
			
			messages.info(request, 'Item qty has been updated')
			return redirect('order-summary')
			
		else:
			messages.info(request, 'This item was not in your cart')
			return redirect('order-summary', pk=pk)
	else:
		messages.info(request, 'You do not have an active order')
		return redirect('order-summary', pk=pk)
	
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()			
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created successfully. Log in here')
			return redirect('login')
	else:
		form = UserRegisterForm()

	return render(request, 'register.html', {'form':form})


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()

		messages.success(request, f'Your profile has been updated')
		return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form':u_form,
		'p_form':p_form
	}
	return render(request, 'profile.html', context)

def about(request):
	return render(request, 'about.html', {})


class PriView(ListView):
	model = Item
	template_name = 'pri.html'

class SecView(ListView):
	model = Item
	template_name = 'sec.html'
	ordering = ['-id']
	paginate_by = 10

class FreePapersView(ListView):
	model = Free
	template_name = 'freepapers.html'

		

class CompletedOrderView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):

		try:
			order = OrderItem.objects.filter(user=self.request.user, ordered=True)
			context = {
				'object': order
			}
			return render(self.request, 'complete.html', context)
		except ObjectDoesNotExist:
			
			messages.error(self.request, "You can only acesss orders with completed payment status. Continue shopping or proceed to checkout")
			return redirect("order_summary.html")
		return render(self.request, 'complete.html')



class VideoView(ListView):
	model = Sinema
	paginate_by = 12
	template_name = 'vids.html'
	ordering = ['-id']

# def vids(request):
# 	context = {
# 		'videos': Sinema.objects.all()
# 	}

# 	return render(request, 'vids.html', context)

	



	