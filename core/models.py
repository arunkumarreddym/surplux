from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (
        ('donor', 'Donor'),
        ('buyer', 'Buyer'),
        ('ngo', 'NGO'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # new fields
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Food(models.Model):

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('donated', 'Donated'),
    )

    STORAGE_CHOICES = (
        ('room', 'Room Temperature'),
        ('fridge', 'Refrigerated'),
        ('frozen', 'Frozen'),
    )

    name = models.CharField(max_length=100)
    storage = models.CharField(max_length=20, choices=STORAGE_CHOICES)

    prep_hour = models.IntegerField()
    temp = models.IntegerField()
    humidity = models.IntegerField()
    category = models.CharField(max_length=50, default="Cooked")

    quantity = models.IntegerField()
    price = models.FloatField()
    shelf_life = models.FloatField()

    # ⭐ donor info
    pickup_location = models.CharField(max_length=255, blank=True, null=True)
    donor_phone = models.CharField(max_length=15, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    is_claimed = models.BooleanField(default=False)

    claimed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="claimed_food"
    )

    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="food_donated"
    )

    def __str__(self):
        return self.name

class Grocery(models.Model):
    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="groceries_donated"
    )

    image = models.ImageField(upload_to="grocery_images/")
    expiry_date = models.DateField()

    mrp = models.FloatField()
    days_left = models.IntegerField()
    discount_percent = models.IntegerField()
    final_price = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    claimed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="groceries_claimed"
    )

    is_claimed = models.BooleanField(default=False)

    def __str__(self):
        return f"Grocery Item {self.id}"


class NGO(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=200)
    certificate = models.ImageField(upload_to='ngo_certificates/')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.org_name


class FoodClaim(models.Model):

    STATUS_CHOICES = (
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    )

    food = models.ForeignKey(Food,on_delete=models.CASCADE,related_name="claims")

    ngo = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ngo_requests",
        null=True,
        blank=True
    )

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="buyer_requests",
        null=True,
        blank=True
    )

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending")

    requested_at = models.DateTimeField(auto_now_add=True)