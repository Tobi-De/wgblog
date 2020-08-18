from django.db import models
from django.shortcuts import render
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from streams.blocks import (
    TitleAndTextBlock,
    CTABlock,
    RichTextBlock,
    SimpleRichTextBlock,
    CardBlock,
)


class BlogListingPage(RoutablePageMixin, Page):
    custom_title = models.CharField(max_length=100)

    content_panels = Page.content_panels + [FieldPanel("custom_title")]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().public()
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
        StreamFieldPanel("content")
    ]
