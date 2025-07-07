from django.contrib import admin

from Ims.models import Course, Lesson, Subscription


@admin.register(Course)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('name',)


@admin.register(Lesson)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
