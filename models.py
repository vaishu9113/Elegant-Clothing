from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class UserLogin(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    login_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Login History"
        verbose_name_plural = "User Login Histories"
        ordering = ['-login_at']

    def __str__(self):
        return f"{self.username} ({self.email}) at {self.login_at}"

@receiver(user_logged_in)
def save_user_login(sender, request, user, **kwargs):
    UserLogin.objects.create(username=user.username, email=user.email)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, default='M')

    def __str__(self):
        return f"{self.user.username}'s Cart - Product {self.product_id} (Size {self.size}) x{self.quantity}"

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product_id = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_id')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username}'s Wishlist - Product {self.product_id}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Shipped', 'Shipped'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50, default='Credit / Debit Card')
    payment_reference = models.CharField(max_length=100, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.status})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, default='M')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.product_id} in Order #{self.order.id}"
