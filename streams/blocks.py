from wagtail.core import blocks


class TitleAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="add your title")
    text = blocks.TextBlock(required=True, help_text="add additional text")

    class Meta:
        icon = "edit"
        label = "Title & Text"


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
