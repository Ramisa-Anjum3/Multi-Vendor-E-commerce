from django.contrib import admin
from .models import Category, Product

# Customizing the Product admin interface
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'total_quantity', 'availability', 'date_created')  # Fields to display in the list view
    search_fields = ('title', 'category__title')  # Searchable fields
    list_filter = ('category', 'availability', 'date_created')  # Filters on the sidebar
    prepopulated_fields = {'slug': ('title',)}  # Auto-fill slug based on the title

    # Organizing the form fields (removed `date_created` from the form)
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'image', 'title', 'description', 'price', 'slug')
        }),
        ('Inventory', {
            'fields': ('total_quantity', 'availability')
        }),
    )

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
