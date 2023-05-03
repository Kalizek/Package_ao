import segno, os
import csv
import pandas as pd
from PIL import Image
from PIL import Image, ImageDraw, ImageFont
from tabulate import tabulate
from playsound import playsound


global n, scanned
n = 1
scanned = []
columns = ['№', 'Номер ФН', 'Тикет', 'Проект']

def out_red(text):
    print("\033[31m {}" .format(text))

def out_green(text):
    print("\033[32m {}" .format(text))

def out_white(text):
    print("\033[37m {}" .format(text))

# def qr_box():
#     global scanned
#     qr_box_arrey = []
#     # for i in range(len(scanned)):
#     qr_box_arrey = scanned[]
#     print(qr_box_arrey)
#     qrcode_box = segno.make_qr(qr_box_arrey)
#     qrcode_box.save("qr_box.png", dark="black", border=10, scale=5)
#     qr_box = Image.open("qr_box.png")
#     img_box = Image.new('RGB', (1000, 400), 'white')

#     qr1 = qr_box.resize((300,300))
#     img_box.paste(qr1,(400, 100))

#     img_box.save("FN/qr_box.png")


def history():
    global scanned
    with open("history.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r\n")
        for i in range(len(scanned)):
            file_writer.writerow(scanned[i])
            



def qr(fn,tik,pr):
    global n,scanned
    # Создание QR
    text_qr = ([fn + "\t" + tik])
    text_p = fn + "\n    " + tik + "  " + pr
    qrcode = segno.make_qr(text_qr)
    # цвет - #2980B9, граница - 8, масштабирование - в 5 раз
    qrcode.save("temp_qr.png", dark="black", border=10, scale=5)

    qr = Image.open("temp_qr.png")
    img = Image.new('RGB', (1000, 400), 'white')

    qr1 = qr.resize((190,190))

    img.paste(qr1,(530, 100))

    font = ImageFont.truetype("arial.ttf", 28, encoding="unic")
    draw_text = ImageDraw.Draw(img)
    draw_text.text(
        (430, 250),
        text_p,
        # Добавляем шрифт к изображению
        font=font,
        fill='#1C0606')
    scanned.append([str(n),str(fn),str(tik),str(pr)])
    img.save('FN/'+ str(n) + ".jpg")
    n += 1
    qr.close()
    img.close()
    os.remove("temp_qr.png")

def d_scanned():
    temp_scanned = []
    for i in range(len(scanned)):
        if i % 10 == 0:
            d = i // 10
            temp_scanned.append(["===","Столбец - " + str(d+1), "===","==="])
            temp_scanned.append(scanned[i])
        else:
            temp_scanned.append(scanned[i])
    print(tabulate(temp_scanned, headers=columns))



def scann_run():
    entrance = "-1"
    out_white("0. Выход из режима")
    entrance = str(input())
    while entrance != "0":
        FN_temp = entrance.split(";")[0]
        FN_temp = FN_temp.split("ж")[0]
        if int(FN_temp) in FN:
            for i in range(nfn):
                if FN_temp == str(FN[i]):
                    if flag_arrey[i] == False:
                        clear()
                        qr(str(FN[i]),str(TIK[i]),str(PR[i]))
                        flag_arrey[i] = True
                        out_white("0. Выход из режима")
                        d_scanned()
                    else:
                        clear()
                        out_white("0. Выход из режима")
                        out_red("ФН уже отсканирован")
                        playsound("temp/20031.mp3")
                        out_white("\n")
                        d_scanned()
        else:
            clear()
            print("ФН нет в списке")
            playsound("temp/20031.mp3")
        entrance = str(input())
    clear()

FN = []
TIK = []
PR = []
clear = lambda: os.system('cls')
clear()
file_name = "day.xlsx"
new = pd.read_excel(file_name)
for i in range(len(new)):
    FN.append(new["Текущий номер ФН"][i])
    TIK.append(new["Тикет"][i])
    PR.append(new["Атол/АО"][i])
flag_arrey = [False]*len(PR)
nfn = (len(FN))
print("Найдено " + str(nfn) + " ФН")
p = 0


delete = os.listdir("FN")
for d in range(len(delete)):
    os.remove("FN/" + str(delete[d]))

while p != "0":
    print("1. Войти в режим сканирования\n2. Посмотреть список ФН\n0. Выйти")
    p = str(input())
    if p == "2":
        clear()
        d_scanned()
    elif p == "1":
        clear()
        scann_run()
clear()
    # elif p == "3":
    #     clear()
    #     qr_box()
