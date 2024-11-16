from tkinter import *
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import pygame # Play audio using pygame mixer
from PIL import Image, ImageTk  # For resizing the icon

# Initialize Translator
translator = Translator()

# Initialize pygame mixer for TTS playback
pygame.mixer.init()

def FunTranslate():
    text_to_translate = entry_window.get("1.0", END).strip()
    language_code = drop_down.get()
    target_lang = ""

    lang_dict = {
        "Hindi": "hi",
        "English": "en",
        "Spanish": "es",
        "German": "de",
        "French": "fr"
    }
    target_lang = lang_dict.get(language_code, "en")  # Default English if none selected

    try:
        translated_text = translator.translate(text_to_translate, dest=target_lang)
        translated_text = translated_text.text
        output_window.delete("1.0", END)
        output_window.insert(END, translated_text)
    except Exception as e:
        output_window.delete("1.0", END)
        output_window.insert(END, "Translation Error")

def text_to_speech(text_widget):
    text = text_widget.get("1.0", END).strip()
    language_code = drop_down.get()
    target_lang = ""

    lang_dict = {
        "Hindi": "hi",
        "English": "en",
        "Spanish": "es",
        "German": "de",
        "French": "fr"
    }
    target_lang = lang_dict.get(language_code, "en")  # Default English if none selected

    try:
        tts = gTTS(text=text, lang=target_lang, slow=False)
        speech_audio = BytesIO()
        tts.write_to_fp(speech_audio)
        speech_audio.seek(0)

        pygame.mixer.music.load(speech_audio, "mp3")
        pygame.mixer.music.play()
    except Exception as e:
        output_window.delete("1.0", END)
        output_window.insert(END, "Error in playing audio")

# GUI setup
tk_window = Tk()
tk_window.title("Language Translator")
tk_window.state("zoomed")  # Fullscreen window

# Frame setup for border and content layout
border_frame = Frame(tk_window, bg="#2C3E50", padx=20, pady=20)
border_frame.pack(expand=True, fill=BOTH)

# Language selection and Translate button at the top
top_frame = Frame(border_frame, bg="#2C3E50")
top_frame.pack(fill=X, pady=(0, 10))

lang_Options = ["English", "Hindi", "Spanish", "German", "French"]
drop_down = StringVar()
drop_down.set("Select Language")
list_lang = OptionMenu(top_frame, drop_down, *lang_Options)
list_lang.config(bg="#3498DB", fg="white", font=("Arial", 12, "bold"))
list_lang.pack(side=LEFT, padx=(0, 10))

Btntranslate = Button(top_frame, text="Translate", bg="#27AE60", fg="white", font=("Arial", 16, "bold"), command=FunTranslate)
Btntranslate.pack(side=LEFT)

# Load and resize speaker icon
original_icon = Image.open("speaker_icon.png")
resized_icon = original_icon.resize((30, 30), Image.Resampling.LANCZOS)  # Correct attribute for resizing
speaker_icon = ImageTk.PhotoImage(resized_icon)

# Input and Output Frames side-by-side
io_frame = Frame(border_frame, bg="#2C3E50")
io_frame.pack(expand=True, fill=BOTH)

# Input Frame
input_frame = Frame(io_frame, bg="white", relief=SOLID, bd=2)
input_frame.pack(side=LEFT, expand=True, fill=BOTH, padx=10, pady=10)

input_scrollbar = Scrollbar(input_frame)
input_scrollbar.pack(side=RIGHT, fill=Y)

entry_window = Text(input_frame, bg="white", fg="black", font=("Arial", 14), wrap=WORD, yscrollcommand=input_scrollbar.set)
entry_window.pack(expand=True, fill=BOTH, padx=10, pady=10)
input_scrollbar.config(command=entry_window.yview)

input_speaker_btn = Button(input_frame, image=speaker_icon, bg="white", command=lambda: text_to_speech(entry_window))
input_speaker_btn.place(relx=0.93, rely=0.015)

output_frame = Frame(io_frame, bg="white", relief=SOLID, bd=2)
output_frame.pack(side=RIGHT, expand=True, fill=BOTH, padx=10, pady=10)

output_scrollbar = Scrollbar(output_frame)
output_scrollbar.pack(side=RIGHT, fill=Y)

output_window = Text(output_frame, bg="white", fg="black", font=("Arial", 14), wrap=WORD, yscrollcommand=output_scrollbar.set)
output_window.pack(expand=True, fill=BOTH, padx=10, pady=10)
output_scrollbar.config(command=output_window.yview)

output_speaker_btn = Button(output_frame, image=speaker_icon, bg="white", command=lambda: text_to_speech(output_window))
output_speaker_btn.place(relx=0.88, rely=0.015)

# Run the application
tk_window.mainloop()
