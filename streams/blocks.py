from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="add your title")
    text = blocks.TextBlock(required=True, help_text="add additional text")

    class Meta:
        icon = "edit"
        label = "Title & Text"


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="add your title")
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                (
                    "button_url",
                    blocks.URLBlock(
                        required=False,
                        help_text="If the button page above is selected, that will be used",
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "edit"
        label = "Card Decks"


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        icon = "doc-full"
        label = "Full Reach Text"


class SimpleRichTextBlock(blocks.RichTextBlock):
    class Meta:
        icon = "edit"
        label = "Simple Reach Text"

    def __init__(
        self,
        required=True,
        help_text=None,
        editor="default",
        features=None,
        validators=(),
        **kwargs
    ):
        super().__init__(
            required=required,
            help_text=help_text,
            editor=editor,
            features=features,
            validators=validators,
            **kwargs
        )
        self.features = ["bold", "italic", "link"]


class CTABlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default="Learn More")

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"


class LinkStructValue(blocks.StructValue):
    def url(self):
        button_page = self.get("button_page")
        button_url = self.get("button_url")
        return button_page if button_page else button_url

    # def latests(self):
    #     return BlogDetailPage.objects.live().public()[:3]


class ButtonBlock(blocks.StructBlock):
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context["latest"] = BlogDetailPage.objects.live().public()[:3]
    #     return context

    class Meta:
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue
