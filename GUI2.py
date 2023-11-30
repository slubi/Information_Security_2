import tkinter as tk
from tkinter import messagebox
from S_AES import *
import tkinter as tk
from tkinter import messagebox
from time import time
result="error"#默认返回结果
state="encrypt"#默认为加密模式
input_mode="bits"#默认为二进制数输入模式
num_keys=1
Locked_Correct_key:bool=False
work_mode="ECB"
init_vec="1001110011100010"
all_mingwen:list[str]=[]#存储破解模式中接收到的明文组
all_miwen:list[str]=[]#存储破解模式中接收到的密文组
possible_key:list[str]=[]#存储可能的密钥
def multi_keys():
    global num_keys
    num_keys=num_keys+1
    if num_keys==4:
        num_keys=1
    messagebox.showinfo("提示",'现在有{}重密码,请按顺序输入所有的密码'.format(num_keys))
def change_word_mode():
     global work_mode
     if work_mode=="ECB":
        work_mode="CBC"
        messagebox.showinfo("提示","现在是CBC模式")
     else:
        work_mode="ECB"
        messagebox.showinfo("提示","现在是ECB模式")
def clear_records():
    global all_mingwen,all_miwen
    all_miwen.clear()
    all_mingwen.clear()
    possible_key.clear()
    print(all_mingwen,all_mingwen)
    tk.Tk().withdraw()
    messagebox.showinfo("提示","已经清除所有信息")
def Save_info(event,mingwen,miwen):
    global all_mingwen
    global all_miwen
    #print("获取到的明文",mingwen)
    #print("获取到的密文",miwen)
    all_mingwen.append(mingwen)
    all_miwen.append(miwen)
    messagebox.showinfo("提示","保存成功")
def Convert():
    global state
    if state=="encrypt":
        state="decrypt"
        tk.Tk().withdraw()
        messagebox.showinfo("提示","现在是解密模式")
    else:
        state="encrypt"
        tk.Tk().withdraw()
        messagebox.showinfo("提示","现在是加密模式")
def Change_input_mode():
    global input_mode
    if input_mode=="bits":
        input_mode="ASCII"
        tk.Tk().withdraw()
        messagebox.showinfo("提示","现在是字符模式")
    else:
        input_mode="bits"
        tk.Tk().withdraw()
        messagebox.showinfo("提示","现在是二进制模式")
def get_result():#获得转换后的结果
    key=entry1.get()
    info=entry2.get()
    global result
    times=len(key)/16
    if times!=num_keys:
        messagebox.showinfo("提示","密码长度不正确，请检查输入")
    if input_mode=='bits':#二进制模式
        if state=="encrypt":
            if times==1:
                result=Encrypt(info,key[0:16])
            elif times==2:
                result=Encrypt(info,key[0:16])
                result=Encrypt(result,key[16:32])
            elif times==3:
                result=Encrypt(info,key[0:16])
                result=Encrypt(result,key[16:32])
                result=Encrypt(result,key[32:48])
        else:
            if times==1:
                result=Decrypt(info,key)
            elif times==2:
                result=Decrypt(result,key[16:32])
                result=Decrypt(result,key[0:16])
            elif times==3:
                result=Decrypt(info,key[32:48])
                result=Decrypt(result,key[16:32])
                result=Decrypt(result,key[0:16])
    elif input_mode=="ASCII":#字符串模式
        if len(info)%2==1:
            messagebox.showinfo("提示","请输入偶数个字符")
            return None
        info_bit=AsciiToBit(info)#先将字符输入转换为二进制输入
        if work_mode=="CBC":
            info_bit_CBC=[]
            info_bit_CBC_p=""
            for i in range(16):
                info_bit_CBC_p+=str(int(init_vec[i])^int(info_bit[0][i]))
            info_bit_CBC.append(info_bit_CBC_p)
            for i in range(1,len(info_bit)):
                info_bit_CBC_p=""
                for j in range(16):
                    info_bit_CBC_p+=str(int(info_bit_CBC[i-1][j])^int(info_bit[i][j]))
                info_bit_CBC.append(info_bit_CBC_p)
        #print(init_vec,info_bit)
        #print(info_bit_CBC)
            for i in range(len(info_bit)):
                info_bit[i]=info_bit_CBC[i]
        result_bit:list[str]=[]
        for item in info_bit:
            if state=="encrypt":
                if times==1:
                    result_bit_part=Encrypt(item,key[0:16])
                elif times==2:
                    result=Encrypt(item,key[0:16])
                    result_bit_part=Encrypt(result,key[16:32])
                elif times==3:
                    result=Encrypt(item,key[0:16])
                    result=Encrypt(result,key[16:32])
                    result_bit_part=Encrypt(result,key[32:48])
            else:
                if times==1:
                    result_bit_part=Decrypt(item,key)
                elif times==2:
                    result=Decrypt(item,key[16:32])
                    result_bit_part=Decrypt(result,key[0:16])
                elif times==3:
                    result=Decrypt(item,key[32:48])
                    result=Decrypt(result,key[16:32])
                    result_bit_part=Decrypt(result,key[0:16])
            result_bit.append(result_bit_part)
        result=BitToAscii(result_bit)#将二进制的转换结果还原为对应的字符
    result_.set(result)#在文本框中显示结果

def AsciiToBit(string:str):
    string_bit:list[str]=[]
    for i in range(0,len(string),2):
        char_byte1=bin(ord(string[i]))
        char_byte1=char_byte1[2:]#去标志位"0b"
        char_byte1=(8-len(char_byte1))*"0"+char_byte1#补零
        char_byte2=bin(ord(string[i+1]))
        char_byte2=char_byte2[2:]#去标志位"0b"
        char_byte2=(8-len(char_byte2))*"0"+char_byte2#补零
        string_bit.append(char_byte1+char_byte2)
    return string_bit

def BitToAscii(string_bit:list[str]):
    string=""
    string_bit_new=[]
    for item in string_bit:
        string_bit_new.append(item[0:8])
        string_bit_new.append(item[8:16])
    for byte in string_bit_new:
        char=chr(int(byte,2))
        string+=char
    return string
def Violent_Crack():
    global Locked_Correct_key
    Locked_Correct_key=False
    print("获取到的明文列表",all_mingwen)
    print("获取到的密文列表",all_miwen)
    start_time=time()
    for k in range(len(all_mingwen)):
        if Locked_Correct_key==False:
            test_mingwen=all_mingwen[k]
            test_miwen=all_miwen[k]
            print(f"正在对第{k+1}对明密文进行破解")
            find_possbile_key(test_mingwen,test_miwen)
            print("现在可能的密钥有",possible_key)
    end_time=time()
    run_time=end_time-start_time
    #print(len(possible_key))
    if len(possible_key)==1:
        messagebox.showinfo("提示","破解用时{}\n密钥为{}".format(run_time,possible_key))
    elif len(possible_key)==0:
        messagebox.showinfo("提示","没有找到合理密钥,请检查输入")
    else:#输入较少时可能用多个密钥符合要求
        str1="密钥为"+possible_key[0]
        for i in range(len(possible_key)-1):
            str1=str1+"或"+possible_key[i+1]
        tk.Tk().withdraw()
        messagebox.showinfo("提示",str1+f"\n破解用时{run_time}")
    possible_key.clear()
def find_possbile_key(mingwen,miwen):
    global Locked_Correct_key
    i=0
    global possible_key
    while i<65536:#最大的16位二进制数转换为十进制即为65536
        test_key=bin(i)
        test_key=test_key[2:]#去标志位"0b"
        length=len(test_key)
        gap=16-length
        test_key=gap*"0"+test_key#补零
        if Encrypt(mingwen,test_key)==miwen:
            #print(f"发现密钥{test_key}满足条件")
            if test_key not in possible_key:#样本较少时可能有多个密钥满足条件
                possible_key.append(test_key)
            else:#一旦出现重复即可确定唯一正确的密钥
                possible_key.clear()
                possible_key.append(test_key)
                print("已经锁定唯一正确的密钥",test_key)
                Locked_Correct_key=True
                break
        i+=1
def create_new_windows():
    new_window=tk.Toplevel(root)
    new_window.title("破解模式")
    new_window.geometry('400x200+500+500')
    mingwen_va=tk.StringVar()#明文文本框中的字符串变量
    miwen_va=tk.StringVar()#密文文本框中的字符串变量
    entry_mingwen=tk.Entry(new_window,textvariable=mingwen_va)
    entry_miwen=tk.Entry(new_window,textvariable=miwen_va)
    entry_mingwen.place(relx=0.05,rely=0.05,width=200,height=20)
    entry_miwen.place(relx=0.05,rely=0.15,width=200,height=20)
    tk.Label(new_window,text="此处输入明文",font=('Simhei.ttf',10)).place(relx=0.6,rely=0.05,width=100,height=20)
    tk.Label(new_window,text="此处输入密文",font=('Simhei.ttf',10)).place(relx=0.6,rely=0.15,width=100,height=20)
    button5=tk.Button(new_window,text="开始破解",fg="black",font=("SimHei.ttf",10),command=Violent_Crack)
    button5.place(relx=0.05,rely=0.35,width=100,height=20)
    button6=tk.Button(new_window,text="保存并继续添加",fg="black",font=("SimHei.ttf",10))
    button6.place(relx=0.05,rely=0.22,width=100,height=20)
    button6.bind("<Button-1>",lambda event:Save_info(event,entry_mingwen.get(),entry_miwen.get()))#使用lambda方法来传入Save_info函数需要的参数
    button7=tk.Button(new_window,text="清除保存的信息",fg="black",font=("SimHei.ttf",10),command=clear_records)
    button7.place(relx=0.05,rely=0.45,width=100,height=20)
root=tk.Tk()
root.title("S-AES算法演示")
root.geometry("640x360+200+200")
info_va=tk.StringVar()#待转换信息文本框中的字符串变量
key_va=tk.StringVar()#密钥文本框中的字符串变量
result_=tk.StringVar()#结果文本框中的字符串变量
entry1=tk.Entry(root,textvariable=key_va,width=350)
entry2=tk.Entry(root,textvariable=info_va,width=200)
entry3=tk.Entry(root,state='readonly',text=result_,width=200)
entry1.place(relx=0.1,rely=0.1,width=350,height=20)
entry2.place(relx=0.1,rely=0.2,width=200,height=20)
entry3.place(relx=0.1,rely=0.3,width=200,height=20)
tk.Label(root,text="此处输入密钥",font=('Simhei.ttf',10)).place(relx=0.7,rely=0.1,width=100,height=20)
tk.Label(root,text="此处输入明文/密文",font=('Simhei.ttf',10)).place(relx=0.4,rely=0.2,width=120,height=20)
tk.Label(root,text="转换后的结果",font=('Simhei.ttf',10)).place(relx=0.4,rely=0.3,width=100,height=20)
Button_fun1=tk.Button(root,text="转换加密/解密模式",fg="black",font=("SimHei.ttf",10),command=Convert)
Button_fun1.place(relx=0.25,rely=0.4,width=125,height=20)
Button_fun2=tk.Button(root,text="开始计算",fg="black",font=("SimHei.ttf",10),command=get_result)
Button_fun2.place(relx=0.1,rely=0.4,width=75,height=20)
Button_fun3=tk.Button(root,text="转换输入模式",fg='black',font=("SimHei.ttf",10),command=Change_input_mode)
Button_fun3.place(relx=0.1,rely=0.5,width=100,height=20)
Button_fun4=tk.Button(root,text="进入破解模式",fg="black",font=("SimHei.ttf",10),command=create_new_windows)
Button_fun4.place(relx=0.28,rely=0.5,width=100,height=20)
Button_fun5=tk.Button(root,text="转换多重密码",font=("SimHei.ttf",10),command=multi_keys)
Button_fun5.place(relx=0.1,rely=0.6,width=100,height=20)
Button_fun6=tk.Button(root,text="转换工作模式",font=("SimHei.ttf",10),command=change_word_mode)
Button_fun6.place(relx=0.28,rely=0.6,width=100,height=20)
root.mainloop()
