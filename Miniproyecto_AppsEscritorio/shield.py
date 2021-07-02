from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import StringProperty


Builder.load_file('mylayout.kv')
class MyLayout(Widget):
    out_text = StringProperty("")

    def cambio_texto(self, widget):
        print(widget.text)
        s = str(widget.text)

    def show_slider(self, widget):
        print(widget.value)
        clave = int(widget.value)

    def cifra(self):
        buff = []
        if int(self.clave.value) != 0:
            for c in self.s.text:
                num = ord(c)
                if 65 <= num < 91:
                    new_num = ((num - 65 + int(self.clave.value)) % 26) + 65
                    buff.append(str(chr(new_num)))
                elif 97 <= num < 123:
                    new_num = ((num - 97 + int(self.clave.value)) % 26) + 97
                    buff.append(str(chr(new_num)))
                else:
                    buff.append(c)
            text_output_text = ''.join(buff)
            self.out_text = f"{text_output_text}"
        else:
            text_output_text = "¡Cuidado, has seleccionado 0 como clave y tu mensaje no se cifrará!"
            self.out_text = f"{text_output_text}"
        return print(text_output_text)

class ShieldApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    ShieldApp().run()