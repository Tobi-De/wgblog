from django import forms
from django.db import models
from django.shortcuts import render
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from streams.blocks import (
    TitleAndTextBlock,
    CTABlock,
    RichTextBlock,
    SimpleRichTextBlock,
    CardBlock,
)


class BlogAuthorOrderable(Orderable):
    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey("blog.BlogAuthor", on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel("author"),
    ]


class BlogAuthor(models.Model):
    name = models.CharField(max_length=120)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey("wagtailimages.Image", null=True, related_name="+", on_delete=models.SET_NULL)

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            ImageChooserPanel("image")
        ], heading="Name and Image"),
        MultiFieldPanel([
            FieldPanel("website")
        ], heading="Links")
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Authors"


register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=["name"])

    panels = [
        FieldPanel("name")
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]


register_snippet(BlogCategory)


class BlogListingPage(RoutablePageMixin, Page):
    custom_title = models.CharField(max_length=100)

    content_panels = Page.content_panels + [FieldPanel("custom_title")]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().public()
        # context["categories"] = context
        return context

    @route(r"^latest/$", name="latest")
    def latest_blog_post(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request=None):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append({
            "location": self.full_url + self.reverse_subpage("latest"),
            "lastmod": (self.last_published_at or self.latest_revision_created_at)
        })
        return sitemap


class BlogDetailPage(Page):
    custom_title = models.CharField(max_length=100)
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    content = StreamField(
        [
            ("title_and_text", TitleAndTextBlock()),
            ("full_richtext", RichTextBlock()),
            ("simple_richtext", SimpleRichTextBlock()),
            ("cards", CardBlock()),
            ("cta", CTABlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
        ], heading="Author(s)"),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
        ], heading="Categories"),
        StreamFieldPanel("content")
    ]
