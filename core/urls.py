from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('signup/', views.signup, name='signup'),

    path('login/', views.login_view, name='login'),

    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),

    path('buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),

    path('ngo_dashboard/', views.ngo_dashboard, name='ngo_dashboard'),

    path('add_food/', views.add_food, name='add_food'),

    path('my_listings/', views.my_listings, name='my_listings'),

    path('add_grocery/', views.add_grocery, name='add_grocery'),

    path('buy/<int:food_id>/', views.buy_food, name='buy_food'),

    path('marketplace/', views.marketplace, name='marketplace'),

    path('claim/<int:food_id>/', views.claim_food, name='claim_food'),

    path('marketplace/', views.marketplace, name='marketplace'),

    path('buy/<int:food_id>/', views.buy_food, name='buy_food'),

    path('claim/<int:food_id>/', views.claim_food, name='claim_food'),

    path('add-grocery/', views.add_grocery, name='add_grocery'),

    path('groceries/', views.grocery_list, name='grocery_list'),

    path('logout/', views.logout_view, name='logout'),

    path('my-groceries/', views.grocery_list, name='grocery_list'),

    path('register-ngo/', views.register_ngo, name='register_ngo'),

    path('ngo-pending/', views.ngo_pending, name='ngo_pending'),

    path("claim-food/<int:food_id>/", views.claim_food, name="claim_food"),

    path('ngo-register/', views.ngo_register, name='ngo_register'),

    path('claim-grocery/<int:id>/', views.claim_grocery, name='claim_grocery'),

    path('claim-food/<int:id>/', views.claim_food, name='claim_food'),

    path('request-food/<int:id>/', views.request_food, name='request_food'),
    
    path('approve_request/<int:claim_id>/', views.approve_request, name='approve_request'),

    path('request-food/<int:id>/', views.request_food, name='request_food'),

    path('approve-request/<int:claim_id>/', views.approve_request, name='approve_request'),

    path('reject-request/<int:claim_id>/', views.reject_request, name='reject_request'),

    path('buy-request/<int:food_id>/', views.buy_request, name='buy_request'),

    path('buy-request/<int:food_id>/',views.buy_request,name="buy_request"),

    path('marketplace/',views.marketplace,name="marketplace"),

    path("donor_history/",views.donor_history,name="donor_history"),

    path("buyer_history/",views.buyer_history,name="buyer_history"),

    path("ngo_history/",views.ngo_history,name="ngo_history"),

]