from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Food, Grocery, Profile, NGO, FoodClaim
from .utils import calculate_discount
from .ml_predict import predict_shelf_life


# ---------------- HOME ----------------

def home(request):
    return render(request, "core/home.html")


# ---------------- AUTH ----------------
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile


def signup(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        phone = request.POST.get('phone')
        location = request.POST.get('location')

        # check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # create profile
        Profile.objects.create(
            user=user,
            role=role,
            phone=phone,
            location=location
        )

        messages.success(request, "Account created successfully!")

        return redirect("login")

    return render(request, "core/signup.html")

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            role = user.profile.role

            if role == "donor":
                return redirect("donor_dashboard")
            elif role == "buyer":
                return redirect("buyer_dashboard")
            elif role == "ngo":
                return redirect("ngo_dashboard")

    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- DONOR ----------------

@login_required
def donor_dashboard(request):

    foods = Food.objects.filter(donor=request.user)
    groceries = Grocery.objects.filter(donor=request.user)

    # get pending requests from NGO or Buyer
    requests = FoodClaim.objects.filter(food__donor=request.user, status="pending")

    return render(request, "core/donor_dashboard.html", {
        "foods": foods,
        "groceries": groceries,
        "requests": requests
    })

@login_required
def add_food(request):
    if request.method == "POST":
        name = request.POST.get("name")
        storage = request.POST.get("storage")
        prep_hour = int(request.POST.get("prep_hour"))
        temp = int(request.POST.get("temp"))
        humidity = int(request.POST.get("humidity"))
        quantity = int(request.POST.get("quantity"))
        price = float(request.POST.get("price"))
        category = request.POST.get("category")

        pickup_location = request.POST.get("pickup_location")
        donor_phone = request.POST.get("donor_phone")

        predicted_hours = predict_shelf_life(category, storage, prep_hour, temp, humidity, quantity)
        remaining_hours = max(0, predicted_hours - prep_hour)

        Food.objects.create(
            name=name,
            category=category,
            storage=storage,
            prep_hour=prep_hour,
            temp=temp,
            humidity=humidity,
            quantity=quantity,
            price=price,
            shelf_life=remaining_hours,
            pickup_location=pickup_location,
            donor_phone=donor_phone,
            donor=request.user,
            status="available"
        )

        messages.success(request, "Food added successfully!")
        return redirect("donor_dashboard")

    return render(request, "core/add_food.html")

@login_required
def add_grocery(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        expiry = request.POST.get("expiry_date")
        mrp = float(request.POST.get("mrp"))

        days_left, discount, final_price = calculate_discount(mrp, expiry)

        Grocery.objects.create(
            donor=request.user,
            image=image,
            expiry_date=expiry,
            mrp=mrp,
            days_left=days_left,
            discount_percent=discount,
            final_price=final_price
        )

        messages.success(request, "Grocery added successfully!")
        return redirect("donor_dashboard")

    return render(request, "core/add_grocery.html")


# ---------------- BUYER ----------------

@login_required
def buyer_dashboard(request):

    requests = FoodClaim.objects.filter(buyer=request.user)

    return render(request,"core/buyer_dashboard.html",{
        "requests":requests
    })


@login_required
def buy_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.status = "sold"
    food.save()
    messages.success(request, "Food purchased successfully!")
    return redirect("buyer_dashboard")


# ---------------- NGO ----------------

@login_required
def ngo_register(request):
    if request.method == "POST":
        if NGO.objects.filter(user=request.user).exists():
            messages.error(request, "You already registered an NGO.")
            return redirect("ngo_dashboard")

        NGO.objects.create(
            user=request.user,
            org_name=request.POST.get("org_name"),
            certificate=request.FILES.get("certificate"),
            is_approved=False
        )

        messages.success(request, "Registration submitted for approval.")
        return redirect("ngo_dashboard")

    return render(request, "core/ngo_register.html")


@login_required
def ngo_dashboard(request):

    try:
        ngo = NGO.objects.get(user=request.user)

    except NGO.DoesNotExist:
        return redirect("register_ngo")   # FIX HERE

    if not ngo.is_approved:
        return render(request, "core/ngo_pending.html")

    groceries = Grocery.objects.filter(is_claimed=False)

    foods = Food.objects.filter(
        status="available"
    ) | Food.objects.filter(
        claims__ngo=request.user,
        claims__status="approved"
    )

    return render(request, "core/ngo_dashboard.html", {
        "groceries": groceries,
        "foods": foods
    })


@login_required
def claim_grocery(request, id):
    item = get_object_or_404(Grocery, id=id)
    item.claimed_by = request.user
    item.is_claimed = True
    item.save()

    messages.success(request, "Grocery claimed successfully!")
    return redirect("ngo_dashboard")




@login_required
def my_listings(request):
    foods = Food.objects.filter(
    status="available"
) | Food.objects.filter(
    claims__ngo=request.user,
    claims__status="approved"
)
    return render(request, "core/my_listings.html", {"foods": foods})

def marketplace(request):

    foods = Food.objects.filter(status="available")

    return render(request,"core/marketplace.html",{
        "foods":foods
    })
@login_required
def claim_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.claimed_by = request.user
    food.is_claimed = True
    food.status = "donated"
    food.save()
    return redirect('ngo_dashboard')
@login_required
def grocery_list(request):
    groceries = Grocery.objects.filter(donor=request.user).order_by('-created_at')
    return render(request, 'core/grocery_list.html', {'groceries': groceries})
@login_required
def register_ngo(request):
    if request.method == "POST":
        NGO.objects.create(
            user=request.user,
            org_name=request.POST.get("organization_name"),
            certificate=request.FILES.get("certificate"),
            is_approved=False
        )
        return redirect("ngo_pending")

    return render(request, "core/register_ngo.html")
@login_required
def ngo_pending(request):
    return render(request, "core/ngo_pending.html")
@login_required
def claim_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.claimed_by = request.user
    food.is_claimed = True
    food.status = "donated"
    food.save()
    return redirect('ngo_dashboard')
from django.contrib import messages

@login_required
def request_food(request, id):
    food = get_object_or_404(Food, id=id)

    if not FoodClaim.objects.filter(food=food, ngo=request.user).exists():
        FoodClaim.objects.create(food=food, ngo=request.user)
        messages.success(request, "✅ Food request sent to donor!")
    else:
        messages.info(request, "ℹ️ You already requested this food.")

    return redirect('ngo_dashboard')
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FoodClaim


@login_required
def approve_request(request, claim_id):

    claim = get_object_or_404(FoodClaim,id=claim_id)

    claim.status = "approved"
    claim.save()

    food = claim.food

    if claim.ngo:
        food.status = "donated"
        food.claimed_by = claim.ngo

    if claim.buyer:
        food.status = "sold"
        food.claimed_by = claim.buyer

    food.save()

    messages.success(request,"Request approved")

    return redirect("donor_dashboard")


@login_required
def reject_request(request, claim_id):

    claim = get_object_or_404(FoodClaim, id=claim_id)

    claim.status = "rejected"
    claim.save()

    messages.error(request, "Request rejected")

    return redirect("donor_dashboard")
@login_required
def buy_request(request, food_id):

    food = get_object_or_404(Food, id=food_id)

    if not FoodClaim.objects.filter(food=food, buyer=request.user).exists():

        FoodClaim.objects.create(
            food=food,
            buyer=request.user
        )

        messages.success(request, "Purchase request sent to donor")

    else:
        messages.info(request, "You already requested this item")

    return redirect("buyer_dashboard")

@login_required
def donor_history(request):

    donated_food = Food.objects.filter(
        donor=request.user,
        status__in=["sold", "donated"]
    )

    return render(request,"core/donor_history.html",{
        "foods": donated_food
    })

@login_required
def buyer_history(request):

    foods = Food.objects.filter(
        claimed_by=request.user,
        status="sold"
    )

    return render(request,"core/buyer_history.html",{
        "foods":foods
    })

@login_required
def ngo_history(request):

    foods = Food.objects.filter(
        claimed_by=request.user,
        status="donated"
    )

    return render(request,"core/ngo_history.html",{
        "foods":foods
    })
