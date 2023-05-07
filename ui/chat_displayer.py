from wx import Font, ID_ANY, TE_MULTILINE, TE_READONLY, DEFAULT, NORMAL, WHITE, Colour, BLACK, BORDER_DOUBLE, ALPHA_TRANSPARENT
from wx.richtext import RichTextAttr, RichTextCtrl, TextBoxAttr, TextAttrDimension

class ChatDisplayer(RichTextCtrl):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def addMessage(self, message, red, green, blue):
        font = Font(12, DEFAULT, NORMAL, NORMAL, False)
        text_attr = RichTextAttr()
        text_attr.SetTextColour(WHITE)
        text_attr.SetFont(font)
        bg_color = Colour(red=red, green=green, blue=blue, alpha=125)
        text_attr.SetBackgroundColour(bg_color)

        self.BeginStyle(text_attr)
        self.WriteText(message)
        self.EndStyle()