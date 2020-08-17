from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from streams.blocks import (
    TitleAndTextBlock,
    RichTextBlock,
    SimpleRichTextBlock,
    CardBlock,
    CTABlock
)


class FlexPage(Page):
    """Flexible page bage"""

    content = StreamField(
        [
            ("title_and_text", TitleAndTextBlock()),
            ("full_richtext", RichTextBlock()),
            ("simple_richtext", SimpleRichTextBlock()),
            ("cards", CardBlock()),
            ("cta", CTABlock())
        ],
        null=True,
        blank=True,
    )
    subtitle = models.CharField(max_length=100, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content"),
    ]
