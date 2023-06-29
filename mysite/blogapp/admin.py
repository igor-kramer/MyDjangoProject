from django.contrib import admin

from blogapp.models import Author, Category, Tag, Article


@admin.register(Author)
class OrderAdmin(admin.ModelAdmin):
    list_display = "name", "bio",


@admin.register(Category)
class OrderAdmin(admin.ModelAdmin):
    list_display = "name",


@admin.register(Tag)
class OrderAdmin(admin.ModelAdmin):
    list_display = "name",


class TagInline(admin.StackedInline):
    model = Article.tags.through


@admin.register(Article)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]
    list_display = "title", "content", "author", "category",
