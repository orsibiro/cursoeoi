from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import StringProperty


Builder.load_file('mylayout.kv')
class MyLayout(Widget):

    def cambio_texto(self, widget):
        s = widget.text
        print(widget.text)


    def show_slider(self, widget):
        clave = widget.value
        print(widget.value)

    def cifra(s, clave=3):
        buff = []
        for c in s:
            num = ord(c)
            if 65 <= num < 91:
                new_num = ((num - 65 + clave) % 26) + 65
                buff.append(str(chr(new_num)))
            elif 97 <= num < 123:
                new_num = ((num - 97 + clave) % 26) + 97
                buff.append(str(chr(new_num)))
            else:
                buff.append(c)
        return ''.join(buff)


class ShieldApp(App):
    def build(self):
        return MyLayout()
    


# def main():
#     app = ShieldApp() 
#     app.run()


if __name__ == '__main__':
    ShieldApp().run()