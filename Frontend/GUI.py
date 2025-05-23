import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
from dotenv import load_dotenv
import json
import requests
from io import BytesIO
import threading
import time
import pygame
import cv2
import numpy as np

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JarvisGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Assistant")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # Load environment variables
        load_dotenv()
        
        # Initialize variables
        self.is_mic_on = False
        self.current_frame = "main"
        self.user_info = {
            "username": os.getenv("USERNAME", "User"),
            "fullname": os.getenv("FULLNAME", "Full Name"),
            "profile_image": None
        }
        
        # Initialize pygame for audio
        pygame.mixer.init()
        
        # Create main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create different screens
        self.create_main_screen()
        self.create_chat_screen()
        self.create_settings_screen()
        
        # Show main screen by default
        self.show_screen("main")

    def create_sidebar(self):
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=("gray80", "gray20"))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # User profile section
        self.profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.profile_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Profile image
        self.profile_image = ctk.CTkImage(
            light_image=Image.new("RGB", (100, 100), "gray"),
            dark_image=Image.new("RGB", (100, 100), "gray"),
            size=(100, 100)
        )
        self.profile_label = ctk.CTkLabel(
            self.profile_frame,
            image=self.profile_image,
            text=""
        )
        self.profile_label.grid(row=0, column=0, padx=10, pady=10)
        
        # User info
        self.username_label = ctk.CTkLabel(
            self.profile_frame,
            text=self.user_info["username"],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.username_label.grid(row=1, column=0, padx=10, pady=(0, 5))
        
        self.fullname_label = ctk.CTkLabel(
            self.profile_frame,
            text=self.user_info["fullname"],
            font=ctk.CTkFont(size=14)
        )
        self.fullname_label.grid(row=2, column=0, padx=10, pady=(0, 10))
        
        # Navigation buttons
        self.chat_button = ctk.CTkButton(
            self.sidebar,
            text="Chat",
            command=lambda: self.show_screen("chat"),
            anchor="w"
        )
        self.chat_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.settings_button = ctk.CTkButton(
            self.sidebar,
            text="Settings",
            command=lambda: self.show_screen("settings")
        )
        self.settings_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Social media links
        self.social_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.social_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        
        social_links = [
            ("GitHub", "https://github.com"),
            ("LinkedIn", "https://linkedin.com"),
            ("Twitter", "https://twitter.com")
        ]
        
        for i, (name, url) in enumerate(social_links):
            link = ctk.CTkButton(
                self.social_frame,
                text=name,
                command=lambda u=url: self.open_url(u),
                anchor="w"
            )
            link.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

    def create_main_screen(self):
        self.main_screen = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.main_screen.grid(row=0, column=0, sticky="nsew")
        
        # Jarvis animation placeholder
        self.animation_label = ctk.CTkLabel(
            self.main_screen,
            text="",
            font=ctk.CTkFont(size=48, weight="bold")
        )
        self.animation_label.place(relx=0.5, rely=0.4, anchor="center")
        
        # Mic button
        self.mic_button = ctk.CTkButton(
            self.main_screen,
            text="🎤 Mic Off",
            command=self.toggle_mic,
            width=120,
            height=40
        )
        self.mic_button.place(relx=0.5, rely=0.6, anchor="center")

    def create_chat_screen(self):
        self.chat_screen = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.chat_screen.grid(row=0, column=0, sticky="nsew")
        self.chat_screen.grid_columnconfigure(0, weight=1)
        self.chat_screen.grid_rowconfigure(0, weight=1)
        
        # Chat display area
        self.chat_display = ctk.CTkTextbox(
            self.chat_screen,
            wrap="word",
            font=ctk.CTkFont(size=14)
        )
        self.chat_display.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        
        # Input area
        self.input_frame = ctk.CTkFrame(self.chat_screen)
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.message_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your message...",
            font=ctk.CTkFont(size=14)
        )
        self.message_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=100,
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1, padx=(0, 10))
        
        self.chat_mic_button = ctk.CTkButton(
            self.input_frame,
            text="🎤",
            width=50,
            command=self.toggle_mic
        )
        self.chat_mic_button.grid(row=0, column=2)

    def create_settings_screen(self):
        self.settings_screen = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.settings_screen.grid(row=0, column=0, sticky="nsew")
        self.settings_screen.grid_columnconfigure(0, weight=1)
        
        # Settings form
        self.settings_form = ctk.CTkFrame(self.settings_screen, fg_color="transparent")
        self.settings_form.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        
        # Username
        ctk.CTkLabel(
            self.settings_form,
            text="Username:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.username_entry = ctk.CTkEntry(
            self.settings_form,
            width=300,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        self.username_entry.insert(0, self.user_info["username"])
        
        # Full name
        ctk.CTkLabel(
            self.settings_form,
            text="Full Name:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.fullname_entry = ctk.CTkEntry(
            self.settings_form,
            width=300,
            font=ctk.CTkFont(size=14)
        )
        self.fullname_entry.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="w")
        self.fullname_entry.insert(0, self.user_info["fullname"])
        
        # API Keys
        ctk.CTkLabel(
            self.settings_form,
            text="API Keys:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=4, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.api_keys_text = ctk.CTkTextbox(
            self.settings_form,
            width=300,
            height=100,
            font=ctk.CTkFont(size=14)
        )
        self.api_keys_text.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="w")
        
        # Save button
        self.save_button = ctk.CTkButton(
            self.settings_form,
            text="Save Changes",
            command=self.save_settings
        )
        self.save_button.grid(row=6, column=0, padx=20, pady=20, sticky="w")

    def show_screen(self, screen_name):
        screens = {
            "main": self.main_screen,
            "chat": self.chat_screen,
            "settings": self.settings_screen
        }
        
        for screen in screens.values():
            screen.grid_remove()
        
        screens[screen_name].grid()

    def toggle_mic(self):
        self.is_mic_on = not self.is_mic_on
        mic_text = "🎤 Mic On" if self.is_mic_on else "🎤 Mic Off"
        self.mic_button.configure(text=mic_text)
        self.chat_mic_button.configure(text="🎤" if self.is_mic_on else "🎤")

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.chat_display.insert("end", f"You: {message}\n")
            self.message_entry.delete(0, "end")
            # Here you would typically process the message and get a response
            self.chat_display.insert("end", f"JARVIS: I received your message: {message}\n")

    def save_settings(self):
        # Update user info
        self.user_info["username"] = self.username_entry.get()
        self.user_info["fullname"] = self.fullname_entry.get()
        
        # Update labels
        self.username_label.configure(text=self.user_info["username"])
        self.fullname_label.configure(text=self.user_info["fullname"])
        
        # Save to .env file
        with open(".env", "w") as f:
            f.write(f"USERNAME={self.user_info['username']}\n")
            f.write(f"FULLNAME={self.user_info['fullname']}\n")
            f.write(self.api_keys_text.get("1.0", "end-1c"))

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    app = JarvisGUI()
    app.mainloop()
