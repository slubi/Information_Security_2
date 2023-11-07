import tkinter as tk
import s_aes
import binascii
from tkinter import *
from tkinter import messagebox
import time

# 暴力破解函数
def password(e):
    start = time.time()
    p = entry1.get()
    c = entry3.get()
    output = ''
    key = 0
    for i in range(65536):
        key1 = s_aes.tenTotwo(key, bit=16)
        ciphertext = s_aes.encrypt(p, key1)
        if ciphertext == c:
            output += key1 + ' '
            key = key + 1
        else:
            key = key + 1
    print('密钥有', output)
    entry2.delete(0, END)
    entry2.icursor(0)
    entry2.insert(0, str(key))
    end = time.time()
    messagebox.askyesno('成功破解', '密钥为： ' + str(key)+' 耗时为' + str(end - start)+'s')

# 加密函数
def button_callback(e):
    p = entry1.get()
    key = entry2.get()
    # 对明文进行加密
    ciphertext = s_aes.encrypt(p, key)
    # 将密文显示在输出框中
    entry3.delete(0, END)
    entry3.icursor(0)
    entry3.insert(0, str(ciphertext))
    messagebox.askyesno('成功加密', '密文为： ' + str(ciphertext))

# 解密函数
def button_back(e):
    p = entry3.get()
    key = entry2.get()

    # 对密文进行解密
    plaintext = s_aes.decrypt(p, key)
    entry1.delete(0, END)
    entry1.icursor(0)
    entry1.insert(0, str(plaintext))
    messagebox.askyesno('成功解密', '解密明文为： ' + str(plaintext))

def button_double_encryption(e):
    p = entry1.get()
    key = entry2.get()
    key1 = key[0:16:1]
    key2 = key[16:32:1]
    # 对明文进行加密
    ciphertext = s_aes.encrypt(p, key1)
    ciphertext = s_aes.encrypt(ciphertext, key2)
    # 将密文显示在输出框中
    entry3.delete(0, END)
    entry3.icursor(0)
    entry3.insert(0, str(ciphertext))
    messagebox.askyesno('成功加密', '密文为： ' + str(ciphertext))

def button_double_encryption_b(e):
    p = entry3.get()
    key = entry2.get()
    key1 = key[0:16:1]
    key2 = key[16:32:1]
    # 对密文进行解密
    plaintext = s_aes.decrypt(p, key2)
    plaintext = s_aes.decrypt(plaintext, key1)
    entry1.delete(0, END)
    entry1.icursor(0)
    entry1.insert(0, str(plaintext))
    messagebox.askyesno('成功解密', '解密明文为： ' + str(plaintext))

def button_triple_encryption(e):
    p = entry1.get()
    key = entry2.get()
    # 对明文进行加密
    key1 = key[0:16:1]
    key2 = key[16:32:1]
    key3 = key[32:48:1]
    # 对明文进行加密
    ciphertext = s_aes.encrypt(p, key1)
    ciphertext = s_aes.encrypt(ciphertext, key2)
    ciphertext = s_aes.encrypt(ciphertext, key3)
    # 将密文显示在输出框中
    entry3.delete(0, END)
    entry3.icursor(0)
    entry3.insert(0, str(ciphertext))
    messagebox.askyesno('成功加密', '密文为： ' + str(ciphertext))

def button_triple_encryption_b(e):
    p = entry3.get()
    key = entry2.get()
    key1 = key[0:16:1]
    key2 = key[16:32:1]
    key3 = key[32:48:1]
    # 对密文进行解密
    plaintext = s_aes.decrypt(p, key3)
    plaintext = s_aes.decrypt(plaintext, key2)
    plaintext = s_aes.decrypt(plaintext, key1)

    entry1.delete(0, END)
    entry1.icursor(0)
    entry1.insert(0, str(plaintext))
    messagebox.askyesno('成功解密', '解密明文为： ' + str(plaintext))

# 字符模式函数
def button_ascll(e):
    p = entry1.get()
    key = entry2.get()

    text = p
    b_text = text.encode('utf-8')
    list_b_text = list(b_text)
    re = []
    for num in list_b_text:
        re.append(bin(num)[2:].zfill(8))
    ciphertext = ""
    print(re)
    if len(re) % 2 != 0:
        re.append("00000000")
    for i in range(int(len(re) / 2)):
        temp = re[2 * i + 1] + re[2 * i]
        var2 = s_aes.encrypt(temp, key)
        print(var2)
        var2_1 = var2[0:8:1]
        var2_2 = var2[8:16:1]
        var2_1 = int(var2_1, 2)
        var2_2 = int(var2_2, 2)
        char2 = chr(var2_2)
        ciphertext += char2
        char1 = chr(var2_1)
        ciphertext += char1
    entry3.delete(0, END)
    entry3.icursor(0)
    entry3.insert(0, ciphertext)
    messagebox.askyesno('成功加密', '密文为： ' + str(ciphertext))

def button_ascllb(e):
    p = entry3.get()
    key = entry2.get()
    text = p
    b_text = text.encode()
    list_b_text = list(b_text)
    list_b_text.remove(194)
    print(list_b_text)
    re = []
    for num in list_b_text:
        re.append(bin(num)[2:].zfill(8))
    result = ""
    print(re)
    for i in range(int(len(re) / 2)):
        temp = re[2 * i + 1] + re[2 * i]
        print(temp)
        var2 = s_aes.decrypt(temp, key)
        print(var2)
        var2_1 = var2[0:8:1]
        var2_2 = var2[8:16:1]
        var2_1 = int(var2_1, 2)
        var2_2 = int(var2_2, 2)
        char2 = chr(var2_2)
        result += char2
        char1 = chr(var2_1)
        result += char1
        print(char1)
        print(char2)
    entry1.delete(0, END)
    entry1.icursor(0)
    entry1.insert(0, result)
    messagebox.askyesno('成功解密', '明文为： ' + str(result))

# 创建主窗口
root = tk.Tk()
root.title('S-AES')
root.geometry("450x300+600+280")  # (宽度x高度)+(x轴+y轴)
# 标签
label1 = tk.Label(root, text='明文:', width=10, height=2, font=25)# 明文
label2 = tk.Label(root, text='密钥:', width=10, height=2, font=25)# 密钥
label3 = tk.Label(root, text='密文:', width=10, height=2, font=25)# 密文
label1.place(x=90, y=40)
label2.place(x=90, y=80)
label3.place(x=90, y=120)

# 文本框
entry1 = tk.Entry(root)# 明文框
entry2 = tk.Entry(root)# 密钥框
entry1.place(x=190, y=53)
entry2.place(x=190, y=93)

entry3 = tk.Entry(root)# 密文框
entry3.place(x=190, y=133)

# 按钮
# 加密按钮
btn1 = tk.Button(root,width=5, height=1, bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn1["text"] = "加密"
btn1.place(x=100, y=168)  # 按钮在窗口里面的定位
btn1.bind("<Button-1>", button_callback)
# 双重加密按钮
btn6 = tk.Button(root,width=5, height=1, bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn6["text"] = "双重加密"
btn6.place(x=100, y=200)  # 按钮在窗口里面的定位
btn6.bind("<Button-1>", button_double_encryption)
# 三重加密按钮
btn7 = tk.Button(root,width=5, height=1, bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn7["text"] = "三重加密"
btn7.place(x=200, y=200)  # 按钮在窗口里面的定位
btn7.bind("<Button-1>", button_triple_encryption)
# 解密按钮
btn2 = tk.Button(root,width=5, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn2["text"] = "解密"
btn2.place(x=150, y=168)  # 按钮在窗口里面的定位
btn2.bind("<Button-1>", button_back)
# 双重解密按钮
btn8 = tk.Button(root,width=5, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn8["text"] = "双重解密"
btn8.place(x=150, y=200)  # 按钮在窗口里面的定位
btn8.bind("<Button-1>", button_double_encryption_b)
# 三重解密按钮
btn9 = tk.Button(root,width=5, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn9["text"] = "三重解密"
btn9.place(x=250, y=200)  # 按钮在窗口里面的定位
btn9.bind("<Button-1>", button_triple_encryption_b)
# Ascll按钮
btn3 = tk.Button(root,width=7, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn3["text"] = "Ascll字符"
btn3.place(x=200, y=168)  # 按钮在窗口里面的定位
btn3.bind("<Button-1>", button_ascll)
# Ascll解密按钮
btn5 = tk.Button(root,width=7, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn5["text"] = "A-解密"
btn5.place(x=265, y=168)  # 按钮在窗口里面的定位
btn5.bind("<Button-1>", button_ascllb)
# 破解按钮
btn4 = tk.Button(root,width=5, height=1,  bg='#7CCD7C', activeforeground="blue", activebackground="yellow")
btn4["text"] = "破解"
btn4.place(x=330, y=168)  # 按钮在窗口里面的定位
btn4.bind("<Button-1>", password)

root.mainloop()