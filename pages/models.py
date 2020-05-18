from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField
from embed_video.fields import EmbedVideoField


class Free(models.Model):
	title = models.CharField(max_length=100)
	link_url = models.URLField(null=False, blank=False)
	


class Item(models.Model):
	Exam_Type = (
		('PR', 'Pri'),
		('SR', 'Sec')
	)

	LABEL_CHOICES = (
		('P', 'primary'),
		('S', 'secondary')
	)
	title = models.CharField(max_length=100)
	image1 = models.ImageField(upload_to='sample_image', blank=True)
	image2 = models.ImageField(upload_to='sample_image', blank=True)
	image3 = models.ImageField(upload_to='sample_image', blank=True)
	image4 = models.ImageField(upload_to='sample_image', blank=True)
	image5 = models.ImageField(upload_to='sample_image', blank=True)
	image6 = models.ImageField(upload_to='sample_image', blank=True)
	image7 = models.ImageField(upload_to='sample_image', blank=True)
	image8 = models.ImageField(upload_to='sample_image', blank=True)
	image9 = models.ImageField(upload_to='sample_image', blank=True)
	image10 = models.ImageField(upload_to='sample_image', blank=True)
	image11 = models.ImageField(upload_to='sample_image', blank=True)
	image12 = models.ImageField(upload_to='sample_image', blank=True)
	link_url1 = models.URLField(null=True, blank=True)
	link_url2 = models.URLField(null=True, blank=True)
	link_url3 = models.URLField(null=True, blank=True)
	link_url4 = models.URLField(null=True, blank=True)
	link_url5 = models.URLField(null=True, blank=True)
	link_url6 = models.URLField(null=True, blank=True)
	link_url7 = models.URLField(null=True, blank=True)
	link_url8 = models.URLField(null=True, blank=True)
	link_url9 = models.URLField(null=True, blank=True)
	link_url10 = models.URLField(null=True, blank=True)
	link_url11 = models.URLField(null=True, blank=True)
	link_url12 = models.URLField(null=True, blank=True)
	originalprice = models.FloatField()
	discountedprice = models.FloatField(blank=True, null=True)
	description = models.CharField(max_length=250)
	label = models.CharField(choices=LABEL_CHOICES, max_length=1)
	exam = models.CharField(choices=Exam_Type, max_length=2)
	video = EmbedVideoField(blank=True)
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse ("product-detail", kwargs={'pk': self.pk})

	def get_add_to_cart_url(self):
		return reverse ("add-to-cart", kwargs={'pk': self.pk})

	def get_remove_cart_url(self):
		return reverse ("remove-from-cart", kwargs={'pk': self.pk})

		
class OrderItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	ordered = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.quantity} of {self.item.title}"

	def get_total_discounted_price(self):
		return self.quantity * self.item.discountedprice


	def get_total_original_price(self):
		return self.quantity * self.item.originalprice

	# def get_amount_saved(self):
	# 	return self.get_total_original_price() - self.get_total_original_price()
	def get_total_final_price(self):
		if self.item.discountedprice:
			return self.get_total_discounted_price()
		return self.get_total_original_price()




class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False) 
	billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
	payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)


	def __str__(self):
		return self.user.username

	def get_total(self):
		 total = 0
		 for order_item in self.items.all():
		 	total += order_item.get_total_final_price()
		 return total
	def dollar_total(self):
		return self.get_total()/100

class BillingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	school = models.CharField(max_length=100)
	school_address = models.CharField(max_length=100)
	school_code = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.user.username} BillingAddress'
	


class Payment(models.Model):
	stripe_charge_id = models.CharField(blank=True, null=True, max_length=100)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	name = models.CharField(blank=True, null=True, max_length=100)
	phone = models.IntegerField(blank=True, null=True)
	amount = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username} Payment'


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_image = models.ImageField(default='default.JPG', upload_to='prof_pics')
	
	

	def __str__(self):
		return f'{self.user.username} Profile'



	

