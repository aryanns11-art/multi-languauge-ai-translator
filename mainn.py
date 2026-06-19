import customtkinter as ctk
from PIL import Image, ImageDraw
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import threading
import pygame
import os
import time

pygame.mixer.init()

def make_circle(img_path, size=(40, 40)):
    img = Image.open(img_path).convert("RGBA")
    img = img.resize(size)

    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    result = Image.new("RGBA", size)
    result.paste(img, (0, 0), mask)

    return result

LANGUAGES = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN",
    "Hindi": "hi",
    "Arabic": "ar",
    "Russian": "ru"
}

class MultiLanguageTranslator(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Multi Language Translator")
        self.geometry("950x800")
        self.resizable(False, False)

        self.create_ui()

#----------------------------------------------------------------------------------------

    def create_output_card(self, title, command_factory):
        frame = ctk.CTkFrame(self.main_frame, corner_radius=12)
        frame.pack(fill="x", pady=8)

        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=(10, 0))

        speaker_img = ctk.CTkImage(light_image=make_circle("download.png"), size=(30, 30))
        
        speaker_btn = ctk.CTkButton(top_frame, image=speaker_img, text="", width=35, height=35, fg_color="transparent", command=command_factory)
        speaker_btn.pack(side="left", padx=(0, 8))
        speaker_btn.image = speaker_img

        heading = ctk.CTkLabel(top_frame, text=title, font=("Segoe UI", 18, "bold"))
        heading.pack(side="left")

        output = ctk.CTkLabel(frame, text="Translation will appear here...", wraplength=850, justify="left", font=("Segoe UI", 15))
        output.pack(anchor="w", padx=15, pady=(5, 12))

        return frame, heading, output
    
#----------------------------------------------------------------------------------------

    def create_ui(self):
        # ================= HEADER =================
        self.header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#3B82F6")
        self.header_frame.pack(fill="x")

        self.title_label = ctk.CTkLabel(self.header_frame, text="Multi Language Translator", font=("Segoe UI", 30, "bold"), text_color="white")
        self.title_label.pack(pady=(10, 0))

        self.subtitle = ctk.CTkLabel(self.header_frame, text="Translate into 3 languages at a time", font=("Segoe UI", 15), text_color="white")
        self.subtitle.pack()

        # ------------------- MAIN ---------------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # -------------------- TOP SECTION -----------------------
        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=120)
        self.top_frame.pack(fill="x", padx=15, pady=15)

        # LEFT SIDE : TEXT INPUT
        self.left_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

        self.input_label = ctk.CTkLabel(self.left_frame, text="Enter Text (Auto-Detecting Language)", font=("Segoe UI", 16, "bold"))
        self.input_label.pack(anchor="w")

        self.input_box = ctk.CTkTextbox(self.left_frame, height=100, width=500, font=("Segoe UI", 15), corner_radius=10, fg_color="#F5F7FA", border_width=2, border_color="#3B82F6")
        self.input_box.pack(anchor='nw', pady=(8, 0))

        self.right_frame = ctk.CTkFrame(self.top_frame, width=100, fg_color="transparent")
        self.right_frame.pack(side="right", fill="y", padx=(20, 0))
        
        self.img2 = ctk.CTkImage(light_image=make_circle("mic.png"), size=(50, 50))

        self.speak_btn = ctk.CTkButton(self.right_frame, image=self.img2, text="", fg_color="transparent", width=50, height=50, command=lambda: threading.Thread(target=self.speak_text, daemon=True).start())
        self.speak_btn.pack(pady=(30, 0))

        self.target_lang_frame = ctk.CTkFrame(self.main_frame, height=80)
        self.target_lang_frame.pack(fill='x', pady=5)

        ctk.CTkLabel(self.target_lang_frame, text="Select 3 Target Languages", font=("Segoe UI", 16, "bold")).pack(anchor="w")

        self.lang1_var = ctk.StringVar(value="Select Language")
        self.lang2_var = ctk.StringVar(value="Select Language")
        self.lang3_var = ctk.StringVar(value="Select Language")

        self.lang1_menu = ctk.CTkOptionMenu(self.target_lang_frame, values=["Select Language"] + list(LANGUAGES.keys()), variable=self.lang1_var, width=220)
        self.lang2_menu = ctk.CTkOptionMenu(self.target_lang_frame, values=["Select Language"] + list(LANGUAGES.keys()), variable=self.lang2_var, width=220)
        self.lang3_menu = ctk.CTkOptionMenu(self.target_lang_frame, values=["Select Language"] + list(LANGUAGES.keys()), variable=self.lang3_var, width=220)

        self.lang1_menu.pack(side='left', pady=10, padx=30)
        self.lang2_menu.pack(side='left', pady=10, padx=30)
        self.lang3_menu.pack(side='left', pady=10, padx=30)

        # ================= BUTTON =================
        self.button = ctk.CTkButton(self.main_frame, text="Translate", width=240, height=45, font=("Segoe UI", 16, "bold"), command=self.translate)
        self.button.pack(pady=20)

        # ================= OUTPUT CARDS =================
        self.frame1, self.title1, self.output1 = self.create_output_card("Language 1", lambda: threading.Thread(target=self.speak_translation, args=(self.output1.cget("text"), self.lang1_var.get()), daemon=True).start())
        self.frame2, self.title2, self.output2 = self.create_output_card("Language 2", lambda: threading.Thread(target=self.speak_translation, args=(self.output2.cget("text"), self.lang2_var.get()), daemon=True).start())
        self.frame3, self.title3, self.output3 = self.create_output_card("Language 3", lambda: threading.Thread(target=self.speak_translation, args=(self.output3.cget("text"), self.lang3_var.get()), daemon=True).start())

#----------------------------------------------------------------------------------------

    def translate(self):
        text = self.input_box.get("0.0", "end").strip()
        if not text:
            return

        languages = [
            (self.lang1_var, self.output1, self.title1),
            (self.lang2_var, self.output2, self.title2),
            (self.lang3_var, self.output3, self.title3)
        ]

        for lang_var, output_label, title_label in languages:
            language = lang_var.get()
            if language == "Select Language":
                continue

            code = LANGUAGES[language]
        
            translated = GoogleTranslator(source="auto", target=code).translate(text)

            title_label.configure(text=language)
            output_label.configure(text=translated)

#----------------------------------------------------------------------------------------

    def speak_text(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

            text = recognizer.recognize_google(audio)
            self.input_box.delete("0.0", "end")
            self.input_box.insert("0.0", text)

        except sr.WaitTimeoutError:
            print("You didn't start speaking.")
        except sr.UnknownValueError:
            print("Could not understand.")
        except Exception as e:
            print(e)

#-------------------------------------------------------------------------------------------------

    def speak_translation(self, text, language):
        if not text or text == "Translation will appear here..." or language == "Select Language":
            return

        try:
            code = LANGUAGES[language]
            tts = gTTS(text=text, lang=code) #Creates a Google Text-to-Speech object.
            filename = f"speech_{int(time.time())}.mp3"  # Creates a temporary filename. Using the current timestamp ensures that each filename is unique.
            tts.save(filename)

            pygame.mixer.music.load(filename)  # Loads the MP3 file into Pygame's music player.  
            pygame.mixer.music.play()       # Starts playing the audio.

            while pygame.mixer.music.get_busy():  # get_busy returns -> True or False(audio still playing or not)
                time.sleep(0.1)

            pygame.mixer.music.unload()  #Unloads the MP3 file from Pygame.
            os.remove(filename)

        except Exception as e:
            print(e)            

if __name__ == "__main__":
    app = MultiLanguageTranslator()
    app.mainloop()