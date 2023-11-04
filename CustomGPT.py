import webbrowser

import gpt, voice, recognize
from tkinter import *
from tkinter import ttk, filedialog
import customtkinter
from PIL import Image
import os
import text_to_image
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import freegpt
from colorama import Fore, Back
# pip install -U g4f
apis=open('keys.apikey').read().split(', ')

root = customtkinter.CTk() # create CTk window like you do with the Tk window
root.title("CustomGPT v.2.2.1-GUI-RU-Release")
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark  # Themes: blue (default), dark-blue, green

root.geometry()

stability=PhotoImage(file="img/stability.png")
main_image=Image.open("img/image.png")
mega_image=PhotoImage(file="img/mega_img.png")
width_photo, height_photo = main_image.size
main_image = main_image.resize((int(width_photo//4.2), int(height_photo//4.2
                                                         ))) ## The (250, 250) is (height, width)

gitlogo=PhotoImage(file="img/img.png")
main_image.save('img/temp.png')
main_image = PhotoImage(file="img/temp.png")

#qrcode=PhotoImage(file="img/qr-code.png")
about="""    CustomGPT (КастомЖдиПиТи) является не 
    коммерческим проектом, основанный на языковой 
    модели ChatGPT 3.5 turbo, с графическим 
    интерфейсом CustomTkinter, озвучкой SileroTTS. 
    Пожалуйста не распростроняйте API-ключ, если по 
    каким-то причинам он остался в проекте."""

'''
image_text = """Поддерживается генерация изображений!
Для этого введите:
 /генерация_изображения [запрос] [РАЗМЕРxРАЗМЕР]
Например: /генерация_изображения кот 1024x1024"""
'''
# Use CTkButton instead of tkinter Button
#button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
#button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

active_voice = BooleanVar(value=False)

models=['stable-diffusion-v1',
'stable-diffusion-v1-5',
'stable-diffusion-512-v2-0',
'stable-diffusion-768-v2-0',
'stable-diffusion-512-v2-1',
'stable-diffusion-768-v2-1',
'stable-inpainting-v1-0',
'stable-inpainting-512-v2-0',
'esrgan-v1-x2plus',
'stable-diffusion-xl-beta-v2-2-2',
'stable-diffusion-xl-1024-v0-9',
'stable-diffusion-xl-1024-v1-0',
'stable-diffusion-x4-latent-upscaler',
]

samplers_list=['DDIM',
'PLMS',
'K_EULER',
'K_EULER_ANCESTRAL',
'K_HEUN',
'K_DPM_2',
'K_DPM_2_ANCESTRAL',
'K_DPMPP_2S_ANCESTRAL',
'K_DPMPP_2M',
'K_DPMPP_SDE']

sizes=[
'1024x1024',
'1152x896',
'896x1152',
'1216x832',
'832x1216',
'1344x768',
'768x1344',
'1536x640',
'640x1536',
'512x512'
]

gptmodel = ['gpt-3.5-turbo-16k',
'gpt-3.5-turbo-16k-0613',
'gpt-4-0613']

'''['palm',
'h2ogpt-gm-oasst1-en-2048-falcon-7b-v3',
'h2ogpt-gm-oasst1-en-2048-falcon-40b-v1',
'h2ogpt-gm-oasst1-en-2048-open-llama-13b',
'claude-instant-v1',
'claude-v1',
'claude-v2',
'command-light-nightly',
'command-nightly',
'gpt-neox-20b',
'oasst-sft-1-pythia-12b',
'oasst-sft-4-pythia-12b-epoch-3.5',
'santacoder',
'bloom',
'flan-t5-xxl',
'code-davinci-002',
'text-ada-001',
'text-babbage-001',
'text-curie-001',
'text-davinci-002',
'text-davinci-003',
'llama13b-v2-chat',
'llama7b-v2-chat']
'''
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
root.geometry()
root.option_add("*tearOff", FALSE)
root.resizable(False, False)
count_message=-1
voices=['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']
voice_var = StringVar(value=voices[1])
temp_var=DoubleVar(value=0.7)

free=BooleanVar(value=False)
def listen():
    global count_message
    count_message += 3
    slyx=recognize.recognize_speak()
    print(Fore.BLUE + 'You: ', slyx)
    print(Fore.WHITE)
    st.insert((str(count_message) + '.0'), os.getlogin()+': '+slyx+'\n\n')
    count_message += 3
    user_answer_entry.delete("0", "end")
    if free.get():
        ans= freegpt.freegpt(str(slyx), combobox_models.get(), temp_var.get())
    else:
        ans=gpt.answer(str(slyx), temp_var.get())
    st.insert((str(count_message) + '.0'), 'CustomGPT: '+ ans+'\n\n')
    print(Fore.GREEN + 'CustomGPT: ', ans)
    if active_voice.get() == True: voice.speak(ans, speaker=combobox.get())

def typing():
    global count_message
    ans=''
    count_message += 3
    print(Fore.BLUE + 'You: ', user_answer_entry.get())
    print(Fore.WHITE)
    st.insert((str(count_message) + '.0'), os.getlogin()+': '+user_answer_entry.get()+'\n\n')
    count_message += 3
    if free.get():
        ans= freegpt.freegpt(str(user_answer_entry.get()), combobox_models.get(), temp_var.get())
    else:
        ans=gpt.answer(str(user_answer_entry.get()), temp_var.get())
    user_answer_entry.delete("0", "end")
    st.insert((str(count_message) + '.0'), 'CustomGPT: ' + ans+'\n\n')
    print(Fore.GREEN + 'CustomGPT: ', ans)
    if active_voice.get() == True: voice.speak(ans, speaker=combobox.get())

def update_slider(*args):
    temp_var.set(round(temp_var.get(), 2))

def choise_dir():
    global pathimg
    pathimg = filedialog.askdirectory()
    save_btn.configure(fg_color="green")

def generate():
    global main_image
    (width, height) = (width_entry.get()).split('x')
    text_to_image.texttoimage(api=apis[2],
                prompt=user_answer_entry.get(),
                engine=model_combo.get(),
                width=int(width),
                height=int(height),
                sampler=exec('generation.SAMPLER_' + str(sampler_combo.get())),
                path=pathimg)

    main_image = Image.open(f"{pathimg}/{user_answer_entry.get()}.png")

    width_photo, height_photo = main_image.size
    main_image = main_image.resize((width_photo // 3, height_photo // 3))  ## The (250, 250) is (height, width)
    main_image.save('img/tempimg.png')
    main_image = PhotoImage(file="img/tempimg.png")
    image_mega.configure(image=main_image)

st = customtkinter.CTkTextbox(root, wrap="word", width=600, height=400)
st.grid(column=0, row=0, columnspan=40, rowspan=30)

user_answer_entry = customtkinter.CTkEntry(root, width=600, placeholder_text="Введите запрос, и CustomGPT вам ответит!")
user_answer_entry.grid(row=31, column=0, columnspan=40)

user_answer_button = customtkinter.CTkButton(root, text="Отправить", width=262, command=typing)
user_answer_button.grid(row=32, column=0, columnspan=18)

mic_btn = customtkinter.CTkButton(root, text="Сказать", width=150, command=listen)
mic_btn.grid(row=32, column=19, columnspan=10)

mic_btn = customtkinter.CTkButton(root, text="Сгенерировать изображение", width=150, command=generate)
mic_btn.grid(row=32, column=29, columnspan=12)


image_label = customtkinter.CTkLabel(root, image=mega_image, text="")
image_label.grid(row=0, column=45, columnspan=90, rowspan=1)

about_text = customtkinter.CTkLabel(root, text=about, justify="left", text_color='#888888')
about_text.grid(row=1, column=45, columnspan=20, rowspan=12)

settings_text = customtkinter.CTkLabel(root, text=" Настройки:", justify="center", text_color='#DDDDDD', font=('Arial', 20))
settings_text.grid(row=13, column=45, columnspan=5, rowspan=5)

label = customtkinter.CTkLabel(root, text="Голос: ")
label.grid(row=18, column=45, columnspan=3)

combobox = customtkinter.CTkComboBox(root, values=voices, width=320)
combobox.grid(row=18, column=50, columnspan=20)

temp = customtkinter.CTkLabel(root, text="Температура: ")
temp.grid(row=20, column=45, columnspan=5)

slider = customtkinter.CTkSlider(root, from_=0, to=2, width=170, variable=temp_var, command=update_slider)
slider.grid(row=20, column=50, columnspan=10)

btn_temp=customtkinter.CTkButton(root, textvariable=temp_var)
btn_temp.grid(row=20, column=60, columnspan=20)

voice_active = customtkinter.CTkSwitch(root, text="Озвучка текста", variable=active_voice)
voice_active.grid(row= 22, column=45, columnspan=8)

free_switch = customtkinter.CTkSwitch(root, text="Бесплатный ChatGPT", variable=free)
free_switch.grid(row= 28, column=45, columnspan=10)

label = customtkinter.CTkLabel(root, text="Модель (бесп. ChatGPT): ")
label.grid(row=31, column=45, columnspan=9)

combobox_models = customtkinter.CTkComboBox(root, values=gptmodel, width=200)
combobox_models.grid(row=31, column=56, columnspan=20)

author=customtkinter.CTkButton(root, text="Сделано Bolgaro4ka", width=415, fg_color="black", text_color="white", image= gitlogo, command=lambda: webbrowser.open('https://github.com/bolgaro4ka'))
author.grid(row=32, column=45, columnspan=30)
#gitbutton=customtkinter.CTkButton(root, width=240, fg_color="black", text_color="white", text="Проект на GitHub")
#gitbutton.grid(row=22, column=45, columnspan=6, rowspan=30)

#qrcodelabel=customtkinter.CTkLabel(root, text="", image=qrcode)
#qrcodelabel.grid(row=22, column=55, columnspan=30, rowspan=30)

####################################STABILITY AI################2.0###############################################

#image_label=customtkinter.CTkLabel(root, text="", image=stability, justify=LEFT)
#image_label.grid(column=85, row=0, columnspan=50)

###
label_model=customtkinter.CTkLabel(root, text='             Модель: ', justify=LEFT)
label_model.grid(column=85, row=5)

model_combo = customtkinter.CTkComboBox(root, values=models, width=180, height=27)
model_combo.grid(column=90, row=5)

label_width=customtkinter.CTkLabel(root, text=' Размер: ', justify=LEFT)
label_width.grid(column=100, row=5)

width_entry = customtkinter.CTkComboBox(root, values=sizes, width=180, height=27)
width_entry.grid(column=105, row=5)


label_sampler=customtkinter.CTkLabel(root, text='           Семплер: ', justify=LEFT)
label_sampler.grid(column=85, row=7)

sampler_combo = customtkinter.CTkComboBox(root, values=samplers_list, width=180, height=27)
sampler_combo.grid(column=90, row=7)

save_btn = customtkinter.CTkButton(root, text="Сохранить в...", width=180, height=30, command=choise_dir, fg_color="blue")
save_btn.grid(column=105, row=7)

image_mega=customtkinter.CTkLabel(root, text="", image=main_image)
image_mega.grid(column=85, row=8, columnspan=100, rowspan=100)
root.mainloop()