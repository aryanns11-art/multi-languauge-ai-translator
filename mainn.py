import customtkinter as ctk

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

        self.create_ui()

    def create_output_card(self, title):

        frame = ctk.CTkFrame(self.main_frame,corner_radius=12)
        frame.pack(fill="x", pady=8)

        heading = ctk.CTkLabel(frame,text=title,font=("Segoe UI", 18, "bold"))
        heading.pack(anchor="w", padx=15, pady=(10, 0))

        output = ctk.CTkLabel(frame,text="Translation will appear here...",wraplength=850,justify="left",font=("Segoe UI", 15))
        output.pack(anchor="w", padx=15, pady=(5, 12))

        return frame, heading, output

    def create_ui(self):

        # ================= HEADER =================

        self.header_frame = ctk.CTkFrame(self,height=90,corner_radius=0,fg_color="#3B82F6")
        self.header_frame.pack(fill="x")

        self.title_label = ctk.CTkLabel(self.header_frame,text="Multi Language Translator",font=("Segoe UI", 30, "bold"),text_color="white")
        self.title_label.pack(pady=(10, 0))

        self.subtitle = ctk.CTkLabel(self.header_frame,text="Translate into 3 languages at a time",font=("Segoe UI", 15),text_color="white")
        self.subtitle.pack()

        # ------------------- MAIN ---------------------------

        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # -------------------- TOP SECTION -----------------------

        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent",height=120)
        self.top_frame.pack(fill="x", padx=15, pady=15)

        # -------------------------------------------------
        # LEFT SIDE : TEXT INPUT
        # -------------------------------------------------

        self.left_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

        self.input_label = ctk.CTkLabel(self.left_frame,text="Enter Text",font=("Segoe UI", 16, "bold"))
        self.input_label.pack(anchor="w")

        self.input_box = ctk.CTkTextbox(self.left_frame,height=100,width=500,font=("Segoe UI", 15),corner_radius=10,fg_color="#F5F7FA",border_width=2,border_color="#3B82F6")
        self.input_box.pack(anchor='nw',pady=(8, 0))

        # -------------------------------------------------
        # RIGHT SIDE : LANGUAGE OPTIONS
        # -------------------------------------------------

        self.right_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        self.right_frame.pack(side="right", fill="y")

        # Source Language
        ctk.CTkLabel(self.right_frame,text="Source Language",font=("Segoe UI", 16, "bold")).pack(anchor="w")

        self.source_var = ctk.StringVar(value="Select Language")

        self.source_menu = ctk.CTkOptionMenu(self.right_frame,values=["Select Language"] + list(LANGUAGES.keys()),variable=self.source_var,width=220,height=30)
        self.source_menu.pack(pady=(8, 20))

        # Target Languages
        self.target_lang_frame = ctk.CTkFrame(self.main_frame,height=80)
        self.target_lang_frame.pack(fill='x',pady=5)

        ctk.CTkLabel(self.target_lang_frame,text="Select 3 Target Languages",font=("Segoe UI", 16, "bold")).pack(anchor="w")

        self.lang1_var = ctk.StringVar(value="Select Language")
        self.lang2_var = ctk.StringVar(value="Select Language")
        self.lang3_var = ctk.StringVar(value="Select Language")

        self.lang1_menu = ctk.CTkOptionMenu(self.target_lang_frame,values=["Select Language"] + list(LANGUAGES.keys()),variable=self.lang1_var,width=220)

        self.lang2_menu = ctk.CTkOptionMenu(self.target_lang_frame,values=["Select Language"] + list(LANGUAGES.keys()),variable=self.lang2_var,width=220)

        self.lang3_menu = ctk.CTkOptionMenu(self.target_lang_frame,values=["Select Language"] + list(LANGUAGES.keys()),variable=self.lang3_var,width=220)

        self.lang1_menu.pack(side='left',pady=10,padx=30)
        self.lang2_menu.pack(side='left',pady=10,padx=30)
        self.lang3_menu.pack(side='left',pady=10,padx=30)

        # ================= BUTTON =================

        self.button = ctk.CTkButton(self.main_frame,text="Translate",width=240,height=45,font=("Segoe UI", 16, "bold"))
        self.button.pack(pady=20)

        # ================= OUTPUT =================

        self.frame1, self.title1, self.output1 = self.create_output_card("Language 1")

        self.frame2, self.title2, self.output2 = self.create_output_card("Language 2")

        self.frame3, self.title3, self.output3 = self.create_output_card("Language 3")


if __name__ == "__main__":
    app = MultiLanguageTranslator()
    app.mainloop()