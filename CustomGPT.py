import gpt, voice, recognize
from tkinter import *
from tkinter import ttk
import re
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import customtkinter
from PIL import Image
import os

root = customtkinter.CTk() # create CTk window like you do with the Tk window
root.title("CustomGPT")
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark  # Themes: blue (default), dark-blue, green

root.geometry()

about="""    CustomGPT (КастомЖдиПиТи) является не 
    коммерческим проектом, основанный на языковой 
    модели ChatGPT 3.5 turbo, с графическим 
    интерфейсом CustomTkinter, озвучкой SileroTTS. 
    Пожалуйста не распростроняйте API-ключ, если по 
    каким-то причинам он остался в проекте. Автор: 
    Никита Федосов (bolgaro4ka)"""

image_text = """Поддерживается генерация изображений!
Для этого введите:
 /генерация_изображения [запрос] [РАЗМЕРxРАЗМЕР]
Например: /генерация_изображения кот 1024x1024"""
# Use CTkButton instead of tkinter Button
#button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
#button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
root.geometry()
root.option_add("*tearOff", FALSE)
root.resizable(False, False)
count_message=-1
voices=['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']
voice_var = StringVar(value=voices[1])
temp_var=DoubleVar(value=0.7)
def listen():
    global count_message
    count_message += 3
    slyx=recognize.recognize_speak()
    st.insert((str(count_message) + '.0'), os.getlogin()+': '+slyx+'\n')
    count_message += 3
    user_answer_entry.delete("0", "end")
    ans=gpt.answer(str(slyx), temp_var.get())
    st.insert((str(count_message) + '.0'), 'CustomGPT: '+ ans+'\n')

    voice.speak(ans, speaker=combobox.get())
def typing():
    global count_message
    count_message += 3
    st.insert((str(count_message) + '.0'), os.getlogin()+': '+user_answer_entry.get()+'\n')
    count_message += 3
    ans=gpt.answer(str(user_answer_entry.get()), temp_var.get())
    user_answer_entry.delete("0", "end")
    st.insert((str(count_message) + '.0'), 'CustomGPT: ' + ans+'\n')
    voice.speak(ans, speaker=combobox.get())

def update_slider(*args):
    temp_var.set(round(temp_var.get(), 2))

st = customtkinter.CTkTextbox(root, wrap="word", width=600, height=400)
st.grid(column=0, row=0, columnspan=40, rowspan=30)

user_answer_entry = customtkinter.CTkEntry(root, width=600, placeholder_text="Введите запрос, и CustomGPT вам ответит!")
user_answer_entry.grid(row=31, column=0, columnspan=40)

user_answer_button = customtkinter.CTkButton(root, text="Отправить", width=300, command=typing)
user_answer_button.grid(row=32, column=0, columnspan=20)

mic_btn = customtkinter.CTkButton(root, text="Сказать", width=300, command=listen)
mic_btn.grid(row=32, column=21, columnspan=20)

my_image = customtkinter.CTkImage(light_image=Image.open("logo.png"),
                                  dark_image=Image.open("logo.png"),
                                  size=(187, 75))

image_label = customtkinter.CTkLabel(root, image=my_image, text="")
image_label.grid(row=0, column=45, columnspan=30)

about_text = customtkinter.CTkLabel(root, text=about, justify="left", text_color='#888888')
about_text.grid(row=1, column=45, columnspan=20, rowspan=12)

settings_text = customtkinter.CTkLabel(root, text=" Настройки:", justify="center", text_color='#DDDDDD', font=('Arial', 20))
settings_text.grid(row=13, column=45, columnspan=5, rowspan=5)

label = customtkinter.CTkLabel(root, text="Голос: ")
label.grid(row=18, column=45, columnspan=10)

combobox = customtkinter.CTkComboBox(root, values=voices, width=200)
combobox.grid(row=18, column=56, columnspan=20)

temp = customtkinter.CTkLabel(root, text="Температура: ")
temp.grid(row=20, column=45, columnspan=5)

slider = customtkinter.CTkSlider(root, from_=0, to=2, width=100, variable=temp_var, command=update_slider)
slider.grid(row=20, column=50, columnspan=10)

btn_temp=customtkinter.CTkButton(root, textvariable=temp_var)
btn_temp.grid(row=20, column=60, columnspan=20)

label = customtkinter.CTkLabel(root, text=image_text, justify="left", text_color='#888888')
label.grid(row=25, column=45, columnspan=30, rowspan=30)
root.mainloop()