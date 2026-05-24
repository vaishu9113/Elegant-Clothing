from django.contrib import admin
from .models import UserLogin, CartItem, Order, OrderItem

@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'login_at')
    list_filter = ('login_at',)
    search_fields = ('username', 'email')
    change_list_template = 'admin/core/userlogin/change_list.html'

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        queryset = self.get_queryset(request)
        extra_context['total_login_records'] = queryset.count()
        extra_context['unique_user_logins'] = queryset.values('email').distinct().count()
        extra_context['unique_usernames'] = queryset.values('username').distinct().count()
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_id', 'size', 'quantity')
    list_filter = ('size',)
    search_fields = ('user__username', 'user__email')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_id', 'size', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name', 'city')
    inlines = [OrderItemInline]
    actions = ['accept_orders', 'ship_orders', 'complete_orders']

    def accept_orders(self, request, queryset):
        rows_updated = queryset.update(status='Accepted')
        self.message_user(request, f"{rows_updated} order(s) successfully accepted.")
    accept_orders.short_description = "Accept selected orders"

    def ship_orders(self, request, queryset):
        rows_updated = queryset.update(status='Shipped')
        self.message_user(request, f"{rows_updated} order(s) successfully marked as Shipped.")
    ship_orders.short_description = "Ship selected orders"

    def complete_orders(self, request, queryset):
        rows_updated = queryset.update(status='Completed')
        self.message_user(request, f"{rows_updated} order(s) successfully marked as Completed.")
    complete_orders.short_description = "Complete selected orders"
