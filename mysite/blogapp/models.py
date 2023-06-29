from django.db import models


class Author(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100)
    bio = models.TextField(null=False, blank=True)


class Category(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=40)


class Tag(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=20)


class Article(models.Model):

    class Meta:
        ordering = ["title"]

    title = models.CharField(max_length=200)
    content = models.TextField(null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="tags")
