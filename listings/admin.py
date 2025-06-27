from django.contrib import admin
from .models import Listing, ListingImage, Cart

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'location', 'created_at')
    search_fields = ('title', 'category', 'location')
    list_filter = ('category', 'location')

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'image')
    search_fields = ('listing',)
    list_filter = ('listing',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'quantity')
    search_fields = ('user', 'listing')
    list_filter = ('user', 'listing')