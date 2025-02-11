import sqlite3
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import requests
import threading

KV = '''
ScreenManager:
    MenuScreen:
    LoginScreen:
    HomeScreen:

<MenuScreen>:
    name: "menu"
    MDBoxLayout:
        orientation: 'vertical'
        spacing: "20dp"
        padding: "30dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        
        MDLabel:
            text: "Bienvenue"
            theme_text_color: "Primary"
            halign: "center"
            font_style: "H4"

        MDRaisedButton:
            text: "Se connecter"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.show_login("login")
        
        MDRaisedButton:
            text: "Créer un compte"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.show_login("signup")

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        padding: "30dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        
        MDLabel:
            id: title_label
            text: ""
            theme_text_color: "Primary"
            halign: "center"
            font_style: "H5"

        MDTextField:
            id: username
            hint_text: "Nom d'utilisateur"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}

        MDTextField:
            id: password
            hint_text: "Mot de passe"
            password: True
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            text: "Valider"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.validate_login()

        MDRaisedButton:
            text: "Retour"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.return_to_menu()

<HomeScreen>:
    name: "home"
    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        padding: "30dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDLabel:
            id: welcome_label
            text: "Bienvenue !"
            theme_text_color: "Primary"
            halign: "center"
            font_style: "H4"

        MDRaisedButton:
            text: "Déconnexion"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.return_to_menu()
'''

import sqlite3
import threading
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import requests

KV = '''
ScreenManager:
    MenuScreen:
    LoginScreen:
    HomeScreen:

<MenuScreen>:
    name: "menu"
    MDBoxLayout:
        orientation: 'vertical'
        spacing: "20dp"
        padding: "30dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        
        MDLabel:
            text: "Bienvenue"
            theme_text_color: "Primary"
            halign: "center"
            font_style: "H4"

        MDRaisedButton:
            text: "Se connecter"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.show_login("login")
        
        MDRaisedButton:
            text: "Créer un compte"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.show_login("signup")

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        padding: "30dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        
        MDLabel:
            id: title_label
            text: ""
            theme_text_color: "Primary"
            halign: "center"
            font_style: "H5"

        MDTextField:
            id: username
            hint_text: "Nom d'utilisateur"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}

        MDTextField:
            id: password
            hint_text: "Mot de passe"
            password: True
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            text: "Valider"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.validate_login()

        MDRaisedButton:
            text: "Retour"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.return_to_menu()

<HomeScreen>:
    name: "home"
    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        padding: "30dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDLabel:
            id: welcome_label
            text: "Bienvenue !"
            theme_text_color: "Primary"
            halign: "center"
            font_style: "H4"

        MDRaisedButton:
            text: "Déconnexion"
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            on_release: app.return_to_menu()
'''

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Créer la table des utilisateurs si elle n'existe pas."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def register_user(self, username, password):
        """Enregistre un nouvel utilisateur."""
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        """Vérifie si un utilisateur existe avec ce mot de passe."""
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None

    def close(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()

class MenuScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class LoginApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.db = DatabaseManager()  # Initialisation de la base de données
        return Builder.load_string(KV)

    def on_stop(self):
        """Ferme la connexion à la base de données lors de la fermeture de l'application."""
        self.db.close()

    def show_login(self, action):
        """Affiche l'écran de connexion ou d'inscription avec un titre différent."""
        login_screen = self.root.get_screen("login")
        login_screen.ids.title_label.text = "Se connecter" if action == "login" else "Créer un compte"
        self.current_action = action  # Stocke l'action actuelle
        self.root.current = "login"

    def validate_login(self):
        """Gère la connexion et l'inscription selon l'action choisie."""
        username = self.root.get_screen("login").ids.username.text.strip()
        password = self.root.get_screen("login").ids.password.text.strip()

        if not username or not password:
            self.show_dialog("Erreur", "Veuillez remplir tous les champs.")
            return

        url = "http://127.0.0.1:5001/login" if self.current_action == "login" else "http://127.0.0.1:5001/register"
        data = {"username": username, "password": password}

        def make_request():
            try:
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    # Utilisez Clock pour mettre à jour l'UI dans le thread principal
                    Clock.schedule_once(lambda dt: self.show_dialog("Succès", response.json()["message"]))
                    Clock.schedule_once(lambda dt: setattr(self.root, "current", "home" if self.current_action == "login" else "menu"))
                else:
                    Clock.schedule_once(lambda dt: self.show_dialog("Erreur", response.json()["message"]))
            except requests.exceptions.RequestException as e:
                Clock.schedule_once(lambda dt, e=e: self.show_dialog("Erreur", f"Erreur de connexion: {str(e)}"))

        threading.Thread(target=make_request).start()

    def return_to_menu(self):
        """Retour au menu principal."""
        self.root.current = "menu"

    def show_dialog(self, title, message):
        """Affiche une boîte de dialogue avec un message."""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

if __name__ == '__main__':
    LoginApp().run()
