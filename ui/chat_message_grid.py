from wx import FlexGridSizer, StaticText, TextCtrl, Button, ComboBox, EXPAND, EVT_BUTTON, Font, OK, ICON_ERROR, MessageBox, ID_ANY, TE_MULTILINE, TE_READONLY, DEFAULT, NORMAL, CallAfter, RED, BLUE
from utils.utils import model_choices
import threading
from service.api_client import ApiClient
from wx.richtext import RichTextAttr, RichTextCtrl


class ChatMessageGrid(FlexGridSizer):
    def __init__(self, panel):
        super().__init__(6, 2, 9, 25)
        
        chat_message_apikey_label = StaticText(panel, label="API key")
        chat_message_apikey_input = TextCtrl(panel)

        chat_message_historic_label = StaticText(panel, label="Chat", pos=(1, 0))
        chat_message_historic_input = RichTextCtrl(panel, ID_ANY, style=TE_MULTILINE|TE_READONLY)

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
                (chat_message_historic_label, 1, EXPAND),
                (chat_message_historic_input, 1, EXPAND),
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
                chat_message_historic_input,
                chat_message_text,
                model_choice_box,
                chat_message_button
            ),
        )
        
    def completeRequest(self, messages, model, apiKey, chatMessageHistoricInput, message, button):
        # call the service
        client = ApiClient(apiKey)
        answer = client.complete(messages, model=model)

        messages.append({"role": "assistant", "content": answer})

        blue_font = Font(12, DEFAULT, NORMAL, NORMAL, False)
        blue_text_attr = RichTextAttr()
        blue_text_attr.SetTextColour(BLUE)
        blue_text_attr.SetFont(blue_font)
        
        red_font = Font(12, DEFAULT, NORMAL, NORMAL, False)
        red_text_attr = RichTextAttr()
        red_text_attr.SetTextColour(RED)
        red_text_attr.SetFont(red_font)
        
        # update the UI
        CallAfter(chatMessageHistoricInput.BeginStyle, blue_text_attr)
        CallAfter(chatMessageHistoricInput.WriteText, "User: " + message + "\n")
        CallAfter(chatMessageHistoricInput.EndStyle)
        
        CallAfter(chatMessageHistoricInput.BeginStyle, red_text_attr)
        CallAfter(chatMessageHistoricInput.WriteText, "Assistant: " + answer + "\n")
        CallAfter(chatMessageHistoricInput.EndStyle)
        CallAfter(chatMessageHistoricInput.ShowPosition, chatMessageHistoricInput.GetLastPosition())
        
        button.Enable()

    def onClick(
        self,
        event,
        chatMessageSystemInput: TextCtrl,
        chatMessageApiKeyInput: TextCtrl,
        chatMessageHistoricInput: RichTextCtrl,
        chatMessageText: TextCtrl,
        modelChoiceBox: ComboBox,
        button: Button
    ):
        if not len(chatMessageApiKeyInput.GetValue().strip()):
            MessageBox("API key is empty!", "Error", OK | ICON_ERROR)
        elif not len(chatMessageText.GetValue().strip()):
            MessageBox("type something please!", "Error", OK | ICON_ERROR)
        else:
            apiKey = chatMessageApiKeyInput.GetValue().strip()
            message = chatMessageText.GetValue().strip()

            messages = [
                {
                    "role": "system",
                    "content": chatMessageSystemInput.GetValue().strip(),
                },
            ]
            messages.append({"role": "user", "content": message})


            button.Disable()

            # create a thread to run the API call
            t = threading.Thread(target=self.completeRequest, args=(messages, modelChoiceBox.GetValue(), apiKey, chatMessageHistoricInput, message, button))
            t.start()