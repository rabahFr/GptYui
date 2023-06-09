from wx import FlexGridSizer, StaticText, TextCtrl, Button, ComboBox, EXPAND, EVT_BUTTON, Font, OK, ICON_ERROR, MessageBox, ID_ANY, TE_MULTILINE, TE_READONLY, DEFAULT, NORMAL, CallAfter, WHITE, Colour, BLACK, BORDER_DOUBLE
from utils.utils import model_choices
from ui.chat_displayer import ChatDisplayer
import threading
from service.api_client import ApiClient
from wx.richtext import RichTextAttr, TextBoxAttr, TextAttrDimension


class ChatMessageGrid(FlexGridSizer):
    def __init__(self, panel):
        super().__init__(6, 2, 9, 25)
        
        chat_message_apikey_label = StaticText(panel, label="API key")
        chat_message_apikey_input = TextCtrl(panel)

        chat_displayer_label = StaticText(panel, label="Chat", pos=(1, 0))
        chat_displayer_input = ChatDisplayer(panel, ID_ANY, style=TE_MULTILINE|TE_READONLY)

        chat_message_system_label = StaticText(panel, label="System")
        chat_message_system_input = TextCtrl(panel)

        chat_message_label = StaticText(panel, label="your message")
        chat_message_text = TextCtrl(panel, style=TE_MULTILINE)
        chat_message_button = Button(panel, label="send")

        model_choice_label = StaticText(panel, label="model")
        model_choice_box = ComboBox(panel, value="gpt-4", choices=model_choices)

        self.AddMany(
            [
                chat_message_apikey_label,
                (chat_message_apikey_input, 1, EXPAND),
                chat_message_system_label,
                (chat_message_system_input, 1, EXPAND),
                (chat_displayer_label, 1, EXPAND),
                (chat_displayer_input, 1, EXPAND),
                (chat_message_label, EXPAND),
                (chat_message_text, 1, EXPAND),
                (model_choice_label, EXPAND),
                (model_choice_box, EXPAND),
                (chat_message_button, EXPAND),
            ]
        )

        self.AddGrowableRow(2, 1)
        self.AddGrowableRow(3, 1)
        self.AddGrowableCol(1, 1)

        chat_message_button.Bind(
            EVT_BUTTON,
            lambda event: self.onClick(
                event,
                chat_message_system_input,
                chat_message_apikey_input,
                chat_displayer_input,
                chat_message_text,
                model_choice_box,
                chat_message_button
            ),
        )
        
    def completeRequest(self, messages, model, apiKey, chat_displayer_input, message, button):
        # call the service
        client = ApiClient(apiKey)
        answer = client.complete(messages, model=model)

        messages.append({"role": "assistant", "content": answer})

        userMessage = "User: " + message + "\n"
        aiMessage = "Assistant: " + answer + "\n"

        # update the UI
        CallAfter(chat_displayer_input.addMessage, userMessage, 176, 210, 167)
        CallAfter(chat_displayer_input.addMessage, aiMessage, 52, 62, 66)

        # re enable the button
        button.Enable()

    def onClick(
        self,
        event,
        chat_message_system_input: TextCtrl,
        chat_message_apikey_input: TextCtrl,
        chat_message_historic_input: ChatDisplayer,
        chat_message_text: TextCtrl,
        model_choice_box: ComboBox,
        button: Button
    ):
        if not len(chat_message_apikey_input.GetValue().strip()):
            MessageBox("API key is empty!", "Error", OK | ICON_ERROR)
        elif not len(chat_message_text.GetValue().strip()):
            MessageBox("type something please!", "Error", OK | ICON_ERROR)
        else:
            apiKey = chat_message_apikey_input.GetValue().strip()
            message = chat_message_text.GetValue().strip()

            messages = [
                {
                    "role": "system",
                    "content": chat_message_system_input.GetValue().strip(),
                },
            ]
            messages.append({"role": "user", "content": message})


            button.Disable()

            # create a thread to run the API call
            t = threading.Thread(target=self.completeRequest, args=(messages, model_choice_box.GetValue(), apiKey, chat_message_historic_input, message, button))
            t.start()