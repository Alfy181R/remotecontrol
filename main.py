from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import paramiko
import threading

class ConexionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text='Control Remoto', font_size=24))

        self.host = TextInput(hint_text='IP del ordenador', multiline=False)
        self.usuario = TextInput(hint_text='Usuario', multiline=False)
        self.password = TextInput(hint_text='Contraseña', password=True, multiline=False)

        btn = Button(text='Conectar', size_hint_y=None, height=50)
        btn.bind(on_press=self.conectar)

        self.estado = Label(text='')

        layout.add_widget(self.host)
        layout.add_widget(self.usuario)
        layout.add_widget(self.password)
        layout.add_widget(btn)
        layout.add_widget(self.estado)
        self.add_widget(layout)

    def conectar(self, instance):
        self.estado.text = 'Conectando...'
        threading.Thread(target=self._conectar_ssh).start()

    def _conectar_ssh(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host.text, username=self.usuario.text, password=self.password.text)
            self.estado.text = '✅ Conectado a ' + self.host.text
        except Exception as e:
            self.estado.text = '❌ Error: ' + str(e)

class RemoteApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ConexionScreen(name='conexion'))
        return sm

if __name__ == '__main__':
    RemoteApp().run()
