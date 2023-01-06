import ctypes
import win32api, win32con
import search
import tkinter as tk
from tkinter import *
window =tk.Tk()
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
window.tk.call('tk', 'scaling', ScaleFactor/75)
window.config(background = "white")
window.iconphoto(False, tk.PhotoImage(file='图标.png'))
# 获取屏幕的分辨率
Pwidth = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
Pheight = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
window.minsize(Pwidth//3, Pheight//2)
window.title('古诗文')
window.geometry('{}x{}'.format(Pwidth//3+100,Pheight//2+50))

search_text=""
result_list_works=[]
result_list_author=[]
result_list=[]
search_type=0
page=[0,0]

def search_button_callback1():
    global result_list_author
    global result_list_works
    global search_text
    global search_type
    search_text=search_entry.get()
    result_list_author=[]
    result_list_works=[]
    [result_list_author,result_list_works]=search.search_author(search_text)
    page[1]=len(result_list_author)//8
    page[0]=0
    search_type=1
    show_result_list()

def search_button_callback2():
    global result_list_author
    global result_list_works
    global search_text
    global search_type
    search_text=search_entry.get()
    result_list_author=[]
    result_list_works=[]
    [result_list_author,result_list_works]=search.search_author(search_text)
    page[1]=len(result_list_works)//8
    page[0]=0
    search_type=2
    show_result_list()

def search_button_callback3():
    global result_list_works
    global result_list_author
    global search_text
    global search_type
    search_text=search_entry.get()
    result_list_author=[]
    result_list_works=[]
    result_list_works=search.search_work(search_text)
    page[1]=len(result_list_works)//8
    page[0]=0
    search_type=3
    show_result_list()

def select_button_callback(n):
    if n in result_list:
        show_frame.grid_forget()
        detailed_text1["state"]=NORMAL
        detailed_text2["state"]=NORMAL
        detailed_text1.delete("1.0","end")
        detailed_text2.delete("1.0","end")
        if search_type==1:
            search_entry.delete(0, last=END)
            search_entry.insert(END,result_list_author[n+page[0]*8]["Name"])
            search_button_callback2()
        else:
            detailed_frame.grid(row=1,column=0,sticky=(N,E,W,S))
            show_work(n+page[0]*8)
            page_button["text"]="返回"
    

def show_work(n):
    content=result_list_works[n]["Content"]
    if "诗" not in result_list_works[n]["Kind"]:
        nc=content.split('\r\n')
        content=""
        for c in nc:
            content=content+'   '+c+'\r\n'
    detailed_text1.insert("end",'\r\n'+result_list_works[n]["Title"]+'\r\n'+'['+result_list_works[n]["Dynasty"]+']  '+result_list_works[n]["Author"]+'\r\n'+content)
    detailed_text1.tag_add("title","2.0","2.end")
    detailed_text1.tag_add("author","3.0","3.end")
    if "诗" not in result_list_works[n]["Kind"]:
        detailed_text1.tag_add("contentci","4.0","end")
    else:
        detailed_text1.tag_add("content","4.0","end")
    try:
        detailed_text2.insert("end",'\r\n译文:')
        detailed_text2.insert("end",'\r\n'+result_list_works[n]["Translation"]+'\r\n')
    except:
        detailed_text2.insert("end","\r\n无")
    try:
        detailed_text2.insert("end",'\r\n\r\n注释:\r\n')
        detailed_text2.insert("end",result_list_works[n]["Annotation"]+'\r\n')
    except:
        detailed_text2.insert("end","无")
    try:
        detailed_text2.insert("end",'\r\n\r\n评析:\r\n')
        detailed_text2.insert("end",result_list_works[n]["Intro"]+'\r\n')
    except:
        detailed_text2.insert("end","无")
    try:
        detailed_text2.insert("end",'\r\n\r\n评论:')
        detailed_text2.insert("end",'\r\n'+result_list_works[n]["Comment"]+'\r\n')
    except:
        detailed_text2.insert("end","\r\n无")

    detailed_text1["state"]=DISABLED
    detailed_text2["state"]=DISABLED

def show_result_list_works():
    global result_list
    result_list=[]
    for i in range(0,8):
        if i+page[0]*8>=len(result_list_works):
            break
        result_list.append(i)
        result=result_list_works[i+page[0]*8]
        content=result["Content"]
        content=content.replace('\n','')
        content=content.replace('\r','')
        title=result["Title"]
        author=result["Author"]
        dynasty=result["Dynasty"]
        num0=title.find(search_text)
        num1=content.find(search_text)
        if search_type==2:
            if len(content)>=30:
                content=content[0:30]+'...'
        elif num1!=-1:
            dnum=num1-15
            con=''
            if dnum>=0:
                con='...'+content[dnum:num1]
                dnum=15
            else:
                con=content[0:num1]
            if len(content)>(num1+30-dnum):
                con=con+content[num1:num1+30-dnum]+'...'
            else:
                con=con+content[num1:]
            content=con
        else:
            if len(content)>=30:
                content=content[0:30]+'...'
 

        num1=content.find(search_text)

        text_list[i]["state"]=NORMAL
        text_list[i].delete("1.0","end")
        text_list[i].insert("end", title+ '\n['+dynasty+']  '+author+'\n'+content)
        text_list[i]["state"]=DISABLED
        text_list[i].tag_add("title","1.0","1.end")
        text_list[i].tag_add("author","2.0","2.end")
        if search_type==3:
            if num0!=-1:
                text_list[i].tag_add("title1","1."+str(num0),"1."+str(num0+len(search_text)))
            text_list[i].tag_add("content","3.0","end")
            if num1!=-1:
                text_list[i].tag_add("content1","3."+str(num1),"3."+str(num1+len(search_text)))

def show_result_list_author():
    global result_list
    result_list=[]
    for i in range(0,8):
        if i+page[0]*8>=len(result_list_author):
            break
        result_list.append(i)
        result=result_list_author[i+page[0]*8]
        name=result["Name"]
        dynasty=result["Dynasty"]
        birth_year=result["BirthYear"]
        death_year=result["DeathYear"]
        if result["Desc"]=='':
            desc='无简介'
        elif result["Desc"]!=None:
            desc=result["Desc"]
        else:
            desc='无简介'

        text_list[i]["state"]=NORMAL
        text_list[i].delete("1.0","end")
        text_list[i].insert("end", name+ '   ['+dynasty+'] '+birth_year+'-'+death_year+'\n'+desc)
        text_list[i]["state"]=DISABLED
        text_list[i].tag_add("author_M","1.0","1.end")
        text_list[i].tag_add("content","2.0","end")
    a=1

def show_result_list():
    for i in range(8):
        text_list[i]["state"]=NORMAL
        text_list[i].delete("1.0","end")
        text_list[i]["state"]=DISABLED
    detailed_frame.grid_forget()
    page_button["text"]=str(page[0]+1)+'/'+str(page[1]+1)
    if search_entry.get()=='':
        show_frame.grid_forget()
        page_button["text"]='搜索'
    else:
        show_frame.grid(row=1,column=0,sticky=(N,E,W,S))
    if search_type==1:
        show_result_list_author()
    else:
        show_result_list_works()
        

def previous_button_callback():
    global page
    if page[0]!=0:
        page[0]=page[0]-1
    else:
        page[0]=0
    show_result_list()
    page_button["text"]=str(page[0]+1)+'/'+str(page[1]+1)

def next_button_callback():
    global page
    if page[0]!=page[1]:
        page[0]=page[0]+1
    else:
        page[0]=page[1]
    show_result_list()
    page_button["text"]=str(page[0]+1)+'/'+str(page[1]+1)

def page_button_callback():
    if page_button["text"]=='返回':
        show_frame.grid(row=1,column=0,sticky=(N,E,W,S))
        detailed_frame.grid_forget()
        page_button["text"]=str(page[0]+1)+'/'+str(page[1]+1)

window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)

top_frame = Frame(window,relief='solid',bd=3,height=10,background = "white")
top_frame.grid(row=0,column=0,sticky=(N,E,W))
top_frame.rowconfigure(0, weight=1)
top_frame.columnconfigure(3, weight=1)

show_frame = Frame(window,relief='solid',bd=3,height=10,background = "white")
show_frame.rowconfigure([0,1,2,3,4,5,6,7], weight=1)
show_frame.columnconfigure(0, weight=1)

detailed_frame = Frame(window,relief='solid',bd=3,height=10,background = "white")
detailed_frame.rowconfigure(0, weight=1)
detailed_frame.columnconfigure([0,1], weight=1)

search_entry = Entry(top_frame,width=40,font=("KaiTi", 14),relief="solid",bd=2)
search_entry.grid(row=0,column=3,sticky=(N,E,W,S))

search_button1 = tk.Button(top_frame, text="人物", command=search_button_callback1,height=1,width=6,relief="solid",bd=2,background = "white",font=("KaiTi",12))
search_button1.grid(row=0,column=4,sticky=(N,E,W,S))
search_button2 = tk.Button(top_frame, text="作者", command=search_button_callback2,height=1,width=6,relief="solid",bd=2,background = "white",font=("KaiTi",12))
search_button2.grid(row=0,column=5,sticky=(N,E,W,S))
search_button3 = tk.Button(top_frame, text="作品", command=search_button_callback3,height=1,width=6,relief="solid",bd=2,background = "white",font=("KaiTi",12))
search_button3.grid(row=0,column=6,sticky=(N,E,W,S))

previous_button = tk.Button(top_frame, text="上一页", command=previous_button_callback,height=1,width=6,relief="solid",bd=2,background = "white",font=("KaiTi",12))
previous_button.grid(row=0,column=0,sticky=(N,E,W,S))
page_button = tk.Button(top_frame,text='搜索',command=page_button_callback,height=1,width=6,relief="solid",bd=2,background = "white",font=("KaiTi",12))
page_button.grid(row=0,column=2,sticky=(N,E,W,S))
next_button = tk.Button(top_frame, text="下一页", command=next_button_callback,height=1,width=6,relief="solid",bd=2,background = "white",font=("KaiTi",12))
next_button.grid(row=0,column=1,sticky=(N,E,W,S))


text_list=[]
for i in range(8):
    bt = eval("tk.Button(show_frame,width=7,command=lambda : select_button_callback("+str(i)+"),text='详情',relief='solid',bd=1,background = 'white',font=('KaiTi',10))")
    bt.grid(row=i,column=1,sticky=(N,E,W,S))
    te=tk.Text(show_frame,state=DISABLED,spacing3=2,spacing1=8,bd=1,wrap=None)
    te.grid(row=i,column=0,sticky=(N,E,W,S))
    te.tag_config("title",font=("KaiTi", 13,"bold"))
    te.tag_config("title1",font=("KaiTi", 13,"bold"),background='yellow')
    te.tag_config("author",font=("KaiTi", 10))
    te.tag_config("author_M",font=("KaiTi", 17,"bold"),foreground='red')
    te.tag_config("content",font=("KaiTi", 9))
    te.tag_config("content1",font=("KaiTi", 9),background='yellow')
    text_list.append(te)

detailed_text1=tk.Text(detailed_frame,state=DISABLED,spacing3=2,spacing1=8,relief="solid",bd=0)
detailed_text1.grid(row=0,column=0,sticky=(N,E,W,S),padx=20)

detailed_text2=tk.Text(detailed_frame,state=DISABLED,spacing3=2,spacing1=8,relief="solid",bd=1)
detailed_text2.grid(row=0,column=1,sticky=(N,E,W,S))
detailed_text1.tag_config("title",font=("KaiTi", 18,"bold"),justify='center')
detailed_text1.tag_config("author",font=("KaiTi", 13,"bold"),justify='center')
detailed_text1.tag_config("content",font=("KaiTi", 12,"bold"),justify='center')
detailed_text1.tag_config("contentci",font=("KaiTi", 12,"bold"))


window.mainloop()