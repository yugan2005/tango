from django.contrib import admin

# Register your models here.
from rango.models import Category, Page, UserProfile


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class PageInline(admin.TabularInline):
    model = Page
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = [PageInline]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
