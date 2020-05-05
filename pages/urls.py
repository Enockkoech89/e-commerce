from django.urls import path
from pages import views
from .views import (
	HomeView,
	ProductDetailView,
	add_to_cart,
	remove_from_cart,
	OrderSummaryView, 
	remove_single_item_from_cart,
	BillCheckoutView,
    PaymentView,
    Payment2View,
    payment_selector,
    PriView,
    SecView,
    FreePapersView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-single-item/<int:pk>/', remove_single_item_from_cart, name='remove-single-item'),
    path('checkout/', BillCheckoutView.as_view(), name='checkout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment2/', Payment2View.as_view(), name='payment2'),
    path('selector/', payment_selector, name='selector'),
    path('pri/', PriView.as_view(), name='pri-exam'),
    path('sec/', SecView.as_view(), name='sec-exam'),
    path('free-papers/', FreePapersView.as_view(), name='free-papers'),
    
]
