from tkinter import *
from tkinter import ttk,filedialog,font,messagebox,simpledialog
import os
import pyperclip
from PIL import Image,ImageTk
import datetime,webbrowser,re,time
from bs4 import BeautifulSoup
import threading,imageio
class MultiEditor:
    def __init__(self):
        try:
            self.FileURL=""
            self.FileName=""
            self.FileExtension=""
            self.DirURL=""
            self.WinIcon="C:\\Users\\admin\\Desktop\\ICONS\\notebook.ico"
            self.img_multiplier=1
            self.img_rotate=[0,90,180,270]
            self.img_angle=0
            self.delta=0.75
            self.GIF_delta=0.90
            self.GIF_divider=1
            self.Font_Face="arial"
            self.Font_Size=14
            self.Font_Style="none"
            self.title="MultiNote - Untitled"
            self.Total_Tabs=1
            self.no=1
            self.Tab_name=f"Untitled-{self.no}"
            self.img_list=[".jpg",".png",".ico",".jpeg",".bmp",".tif",".tiff",".pxr"]
            self.Highlights="yellow"
            self.Option_check_color="white"
            self.Tabs_Space=40

            self.WordWrap=True
            self.FullScreen=False
            self.Folder_Show=True
            self.Status_Show=True
            self.ToolBar_Show=True
            self.Scrollbars_show=True
            self.FileDetials_show=True
            self.Open_RightClick_Window=False
        except:
            pass
        pass
    # new file
    def New_File(self,*args):
        try:
            self.no=self.no+1
            self.Tab_name=f"Untitled-{self.no}"
            f1=Frame(NoteBox)
            t1=Text(f1,font=(App.Font_Face,App.Font_Size),borderwidth=1,relief=SOLID,wrap='none',undo=True,tabs=self.Tabs_Space)
            t1.pack(fill=BOTH,expand=True)
            Label(f1,text="LB",bg="yellow").pack_forget()
            Button(f1,text="saved").pack_forget()
            f1.pack(fill=BOTH,expand=True)
            NoteBox.add(f1,text=self.Tab_name,padding=(-1, -1, -3, -3))
            NoteBox.select(NoteBox.index(END)-1)
            self.Total_Tabs=self.Total_Tabs+1
            t1.focus()
            self.Theme_Func()
        except:
            pass
        pass
    # open file
    def Open_File(self,*args):
        try:
            fileurl=filedialog.askopenfilename(title="Open",defaultextension="*.txt",filetypes=[("All Files","*.*"),("Text Document","*.txt"),("Python","*.py"),("Python (No Console)","*.pyw"),("HTML","*.html"),("CSS","*.css"),("JavaScript","*.js"),("JSON","*.json"),("PHP","*.php"),("Java","*.java")])
            if fileurl=="":
                pass
            else:
                self.FileURL=fileurl
                self.FileName=os.path.basename(self.FileURL).strip()
                self.FileExtension=os.path.splitext(self.FileName)[1].strip()
                # create a new tab
                f1=Frame(NoteBox)
                Label(f1,text=self.FileURL,bg="yellow").pack_forget()
                t1=Text(f1,font=(App.Font_Face,App.Font_Size),borderwidth=1,relief=SOLID,wrap='none',undo=True,tabs=self.Tabs_Space)
                t1.pack(fill=BOTH,expand=True)
                Button(f1,text="saved").pack_forget()
                
                f1.pack(fill=BOTH,expand=True)
                NoteBox.add(f1,text=self.FileName,padding=(-1, -1, -3, -3))
                t1.delete(0.0,END)
                NoteBox.select(NoteBox.index(END)-1)
                self.Total_Tabs=self.Total_Tabs+1
                t1.focus()
                # checks for file extension
                if self.FileExtension in self.img_list:
                    img=Image.open(self.FileURL)
                    img=ImageTk.PhotoImage(image=img)
                    t1.image_create(END,image=img)
                    t1.image=img
                    t1.config(cursor="arrow")
                    t1.config(state=DISABLED)
                    pass
                elif self.FileExtension==".gif":
                    threading.Thread(target=self.Open_GIF_Image_Func,daemon=True).start()
                    pass
                else:
                    f=open(self.FileURL,"r+")
                    try:
                        data=f.read()
                        t1.insert(END,data)
                    except:
                        t1.insert(END,f"Unable to open this {self.FileExtension} file")
                        t1.config(state=DISABLED)
                    f.close()
                curr=NoteBox.index(CURRENT)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if index==curr:
                        if isinstance(i,Frame):
                            secondrow=i.winfo_children()
                            for j in secondrow:
                                if isinstance(j,Text):
                                    j.edit_modified(False)
                                if isinstance(j,Button):
                                    j.config(text="saved")
                                    Saved_Label.config(text="")
                self.Theme_Func()
                t1.focus()
        except:
            pass
        pass
    # opening with key binding
    def Open_File_Key_Bind(self,*args):
        curr=NoteBox.index(CURRENT)
        firstrow=NoteBox.winfo_children()
        for index,i in enumerate(firstrow):
            if index==curr:
                if isinstance(i,Frame):
                    secondrow=i.winfo_children()
                    for j in secondrow:
                        if isinstance(j,Text):
                            j.edit_modified(False)
                        if isinstance(j,Button):
                            j.config(text="saved")
                            Saved_Label.config(text="")
        self.Open_File()
        pass
    # for gif image
    def Open_GIF_Image_Func(self,*args):
        try:
            new_image=self.FileURL
            no_frames=len(imageio.get_reader(new_image))
            duration_list=[]
            img=Image.open(new_image)
            for i in range(no_frames):
                img.seek(i)
                duration_list.append(float(img.info["duration"]/1000))
                pass
            # increment duration
            gif_tell=0
            forwards=True
            # for the display
            video=imageio.get_reader(new_image)
            GIFH,GIFW=img.size
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.config(cursor="arrow")
                                while(forwards):
                                    for image in video.iter_data():
                                        # display image
                                        frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize((int(GIFH/self.GIF_divider),int(GIFW/self.GIF_divider))))
                                        j.delete(0.0,END)
                                        j.image_create(END,image=frame_image)
                                        time.sleep(duration_list[gif_tell])
                                        # looping
                                        if gif_tell<len(duration_list)-1:
                                            gif_tell=gif_tell+1
                                        else:
                                            gif_tell=0
                                pass
        except:
            pass
        pass
    # Change Tab
    def Change_Tabs_Func(self,*args):
        try:
            self.img_multiplier=1
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if curr==index:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Label):
                                txt=j.cget("text")
                                if txt=="LB":
                                    self.title=f"MultiNote - Untitled"
                                    root.title(self.title)
                                    self.FileURL=""
                                    self.FileExtension=""
                                    self.FileName=""
                                    pass
                                else:
                                    self.FileURL=txt
                                    self.FileName=os.path.basename(self.FileURL)
                                    self.FileExtension=os.path.splitext(self.FileName)[1]
                                    self.title=f"MultiNote - {self.FileName}"
                                    root.title(self.title)
                            if isinstance(j,Text):
                                j.config(xscrollcommand=HorizontalScroll.set)
                                j.config(yscrollcommand=VerticalScroll.set)
                                HorizontalScroll.config(command=j.xview)
                                VerticalScroll.config(command=j.yview)
                                j.bind("<ButtonPress-3>",App.Open_RightWin_Func)
            self.Status_Data_func()
            self.Modified_text()
            self.File_Details_Func()
        except:
            pass
        pass
    # Remove a Tab
    def Remove_Tab(self,*args):
        try:
            if self.Total_Tabs>1:
                self.Total_Tabs=self.Total_Tabs-1
                curr=NoteBox.index(CURRENT)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if index==curr:
                        i.destroy()
                self.FileURL=""
                self.FileExtension=""
                self.FileName=""
            else:
                messagebox.showwarning("Warning","There Should be atleast one Tab Open")
        except:
            pass
        pass
    # Remove All Tabs
    def Remove_AllTabs(self,*args):
        try:
            # create a new tab
            if self.Total_Tabs>1:
                self.no=1
                self.Tab_name=f"Untitled-{self.no}"
                f1=Frame(NoteBox)
                t1=Text(f1,font=(App.Font_Face,App.Font_Size),borderwidth=1,relief=SOLID,wrap='none',undo=True,tabs=self.Tabs_Space)
                t1.pack(fill=BOTH,expand=True)
                Label(f1,text="LB",bg="yellow").pack_forget()
                Button(f1,text="saved").pack_forget()
                f1.pack(fill=BOTH,expand=True)
                NoteBox.add(f1,text=self.Tab_name,padding=(-1, -1, -3, -3))
                NoteBox.select(NoteBox.index(END)-1)
                self.Total_Tabs=1
                t1.focus()
                x=NoteBox.winfo_children()
                x.pop()
                for i in x:
                    i.destroy()
                self.Theme_Func()
        except:
            pass
        pass
    # Save File
    def Save_File(self,*args):
        try:
            if self.FileURL!="":
                curr=NoteBox.index(CURRENT)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if index==curr:
                        if isinstance(i,Frame):
                            secondrow=i.winfo_children()
                            for j in secondrow:
                                if isinstance(j,Text):
                                    f=open(self.FileURL,"r+")
                                    f.write(j.get(0.0,END).lstrip())
                                    f.close()
                                if isinstance(j,Button):
                                    j.config(text="saved")
                                    Saved_Label.config(text="")
                    pass
                pass
            else:
                fileurl=filedialog.asksaveasfilename(title="Save",defaultextension="*.txt",filetypes=[("All Files","*.*"),("Text Document","*.txt"),("Python","*.py"),("Python (No Console)","*.pyw"),("HTML","*.html"),("CSS","*.css"),("JavaScript","*.js"),("JSON","*.json"),("PHP","*.php"),("Java","*.java")])
                if fileurl=="":
                    pass
                else:
                    self.FileURL=fileurl
                    self.FileName=os.path.basename(self.FileURL)
                    self.FileExtension=os.path.splitext(self.FileName)[1]
                    self.title=f"MultiNote - {self.FileName}"
                    root.title(self.title)

                    curr=NoteBox.index(CURRENT)
                    firstrow=NoteBox.winfo_children()
                    for index,i in enumerate(firstrow):
                        if index==curr:
                            NoteBox.tab(index,text=self.FileName)
                            if isinstance(i,Frame):
                                secondrow=i.winfo_children()
                                for j in secondrow:
                                    if isinstance(j,Text):
                                        f=open(self.FileURL,"w+",encoding='utf8')
                                        f.write(j.get(0.0,END).lstrip())
                                        f.close()
                                    if isinstance(j,Label):
                                        j.config(text=self.FileURL)
                                    if isinstance(j,Button):
                                        j.config(text="saved")
                                        Saved_Label.config(text="")
                pass
        except:
            pass
        pass
    def SaveAs_File(self,*args):
        try:
            fileurl=filedialog.asksaveasfilename(title="Save As",defaultextension="*.txt",filetypes=[("All Files","*.*"),("Text Document","*.txt"),("Python","*.py"),("Python (No Console)","*.pyw"),("HTML","*.html"),("CSS","*.css"),("JavaScript","*.js"),("JSON","*.json"),("PHP","*.php"),("Java","*.java")])
            if fileurl=="":
                pass
            else:
                self.FileURL=fileurl
                self.FileName=os.path.basename(self.FileURL)
                self.FileExtension=os.path.splitext(self.FileName)[1]
                self.title=f"MultiNote - {self.FileName}"
                root.title(self.title)

                curr=NoteBox.index(CURRENT)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if index==curr:
                        NoteBox.tab(index,text=self.FileName)
                        if isinstance(i,Frame):
                            secondrow=i.winfo_children()
                            for j in secondrow:
                                if isinstance(j,Text):
                                    f=open(self.FileURL,"w+",encoding='utf8')
                                    f.write(j.get(0.0,END))
                                    f.close()
                                if isinstance(j,Label):
                                    j.config(text=self.FileURL)
                                if isinstance(j,Button):
                                    j.config(text="saved")
                                    Saved_Label.config(text="")
        except:
            pass
        pass
    def Open_Folder_Func(self,*args):
        try:
            x=filedialog.askdirectory()
            if x=="":
                pass
            else:
                self.DirURL=x
                os.chdir(self.DirURL)
                self.DirList=os.listdir()
                File_List.delete(0,END)
                Folder_name.config(text=self.DirURL)
                for i in self.DirList:
                    if os.path.splitext(i)[1]=="" and os.path.isdir(i):
                        File_List.insert(END,f"=>{i}")
                    elif os.path.splitext(i)[1]==".exe" or os.path.splitext(i)[1]==".lnk" or os.path.splitext(i)[1]==".ini":
                        pass
                    else:
                        File_List.insert(END,f"{i}")
        except:
            pass
        pass
    def OpenFile_Folder_Func(self,*args):
        try:
            if self.DirURL:
                # to get the tab names
                Tabs=[]
                for i in NoteBox.tabs():
                    Tabs.append(NoteBox.tab(i,"text"))
                # to get the cursor
                datas=File_List.get(File_List.curselection())
                strs=f"{datas}"
                # if folder
                if strs.startswith("=>"):
                    fold=strs.replace("=>","")
                    new_path=f"{self.DirURL}/{fold}".replace("//","/")
                    self.Close_Folder_Func()
                    self.DirURL=new_path
                    os.chdir(self.DirURL)
                    self.DirList=os.listdir()
                    File_List.delete(0,END)
                    Folder_name.config(text=self.DirURL)
                    for i in self.DirList:
                        if os.path.splitext(i)[1]=="" and os.path.isdir(i):
                            File_List.insert(END,f"=>{i}")
                        else:
                            File_List.insert(END,f"{i}")
                    pass
                # if file
                else:
                    if datas in Tabs:
                        ide=Tabs.index(datas)
                        NoteBox.select(ide)
                    else:
                        self.FileURL=os.path.abspath(datas)
                        self.FileName=os.path.basename(self.FileURL).strip()
                        self.FileExtension=os.path.splitext(self.FileName)[1].strip()
                        # create a new tab
                        f1=Frame(NoteBox)
                        Label(f1,text=self.FileURL,bg="yellow").pack_forget()
                        t1=Text(f1,font=(App.Font_Face,App.Font_Size),borderwidth=1,relief=SOLID,wrap='none',undo=True,tabs=self.Tabs_Space)
                        t1.pack(fill=BOTH,expand=True)
                        Button(f1,text="saved").pack_forget()
                        
                        f1.pack(fill=BOTH,expand=True)
                        NoteBox.add(f1,text=self.FileName,padding=(-1, -1, -3, -3))
                        t1.delete(0.0,END)
                        NoteBox.select(NoteBox.index(END)-1)
                        self.Total_Tabs=self.Total_Tabs+1
                        t1.focus()
                        # checks for file extension
                        if self.FileExtension in self.img_list:
                            img=Image.open(self.FileURL)
                            img=ImageTk.PhotoImage(image=img)
                            t1.image_create(END,image=img)
                            t1.image=img
                            t1.config(cursor="arrow")
                            t1.config(state=DISABLED)
                            pass
                        elif self.FileExtension==".gif":
                            threading.Thread(target=self.Open_GIF_Image_Func,daemon=True).start()
                            pass
                        else:
                            f=open(self.FileURL,"r+")
                            try:
                                data=f.read()
                                t1.insert(END,data)
                            except:
                                t1.insert(END,f"Unable to open this {self.FileExtension} file")
                                t1.config(state=DISABLED)
                            f.close()
                        curr=NoteBox.index(CURRENT)
                        firstrow=NoteBox.winfo_children()
                        for index,i in enumerate(firstrow):
                            if index==curr:
                                NoteBox.tab(index,text=self.FileName)
                                if isinstance(i,Frame):
                                    secondrow=i.winfo_children()
                                    for j in secondrow:
                                        if isinstance(j,Text):
                                            j.edit_modified(False)
                                        if isinstance(j,Button):
                                            j.config(text="saved")
                                            Saved_Label.config(text="")
                    self.Theme_Func()
        except:
            pass
        pass
    # close folder
    def Close_Folder_Func(self,*args):
        try:
            Folder_name.configure(text="Open Folder")
            self.DirURL=""
            self.DirList=[]
            File_List.delete(0,END)
        except:
            pass
        pass
    # go back folder
    def Go_Back_Folder_Func(self,*args):
        try:
            if self.DirURL:
                path_parent=os.path.dirname(self.DirURL)
                self.Close_Folder_Func()
                self.DirURL=path_parent
                os.chdir(self.DirURL)
                self.DirList=os.listdir()
                File_List.delete(0,END)
                Folder_name.config(text=self.DirURL)
                for i in self.DirList:
                    if os.path.splitext(i)[1]=="" and os.path.isdir(i):
                        File_List.insert(END,f"=>{i}")
                    else:
                        File_List.insert(END,f"{i}")
        except:
            pass
        pass
    # zooming text
    def Zooming(self,e):
        try:
            if self.FileExtension not in self.img_list:
                curr=NoteBox.index(CURRENT)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if index==curr:
                        if isinstance(i,Frame):
                            secondrow=i.winfo_children()
                            for j in secondrow:
                                if isinstance(j,Text):
                                    if e.delta==120:
                                        self.Font_Size=self.Font_Size+1
                                    if e.delta==-120:
                                        self.Font_Size=self.Font_Size-1
                                    if self.Font_Style=="none":
                                        j.config(font=(self.Font_Face,self.Font_Size))
                                    else:
                                        j.config(font=(self.Font_Face,self.Font_Size,self.Font_Style))
                                    pass
        except:
            pass
    # zooming image
    def Zooming_img(self,e):
        try:
            if self.FileExtension in self.img_list:
                curr=NoteBox.index(CURRENT)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if index==curr:
                        if isinstance(i,Frame):
                            secondrow=i.winfo_children()
                            for j in secondrow:
                                if isinstance(j,Text):
                                    if e.delta==-120:
                                        self.img_multiplier*=self.delta
                                    if e.delta==120:
                                        self.img_multiplier/=self.delta
                                    j.config(state=NORMAL)
                                    j.delete(0.0,END)
                                    j.focus()
                                    img=Image.open(self.FileURL)
                                    H,W=img.size
                                    resized=(int(H*self.img_multiplier),int(W*self.img_multiplier))
                                    img=ImageTk.PhotoImage(image=img.resize(resized).rotate(self.img_rotate[self.img_angle],Image.NEAREST,expand=1))
                                    j.image_create(END,image=img)
                                    j.image=img
                                    j.config(cursor="arrow")
                                    j.config(state=DISABLED)
                                    pass
            elif self.FileExtension==".gif":
                if e.delta==120:
                    self.GIF_divider*=self.GIF_delta
                if e.delta==-120:
                    self.GIF_divider/=self.GIF_delta
                pass
        except:
            pass
        pass
    # Rotate image
    def Rotate_img(self,e):
        try:
            if self.FileExtension in self.img_list:
                curr=NoteBox.index(CURRENT)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if index==curr:
                        if isinstance(i,Frame):
                            secondrow=i.winfo_children()
                            for j in secondrow:
                                if isinstance(j,Text):
                                    if e.delta==-120:
                                        if self.img_angle>0:
                                            self.img_angle=self.img_angle-1
                                    if e.delta==120:
                                        if self.img_angle<3:
                                            self.img_angle=self.img_angle+1
                                    j.config(state=NORMAL)
                                    j.focus()
                                    j.delete(0.0,END)
                                    img=Image.open(self.FileURL)
                                    H,W=img.size
                                    resized=(int(H*self.img_multiplier),int(W*self.img_multiplier))
                                    img=ImageTk.PhotoImage(image=img.resize(resized).rotate(self.img_rotate[self.img_angle],Image.NEAREST,expand=1))
                                    j.image_create(END,image=img)
                                    j.image=img
                                    j.config(cursor="arrow")
                                    j.config(state=DISABLED)
                                    pass
        except:
            pass
        pass
    # Cut copy paste undo redo
    def Cuts(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.event_generate("<<Cut>>")
        except:
            pass
        pass
    def Copys(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.event_generate("<<Copy>>")
        except:
            pass
        pass
    def Pastes(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.event_generate("<<Paste>>")
        except:
            pass
        pass
    def Undos(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.event_generate("<<Undo>>")
        except:
            pass
        pass
    def Redos(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.event_generate("<<Redo>>")
        except:
            pass
        pass
    def SelectAll(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.tag_add(SEL,0.0,END)
        except:
            pass
        pass
    def ClearAll(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.delete(0.0,END)
        except:
            pass
        pass
    def Dateandtime_Func(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                x=datetime.datetime.now()
                                j.insert(END,f"{x.strftime('%I')}:{x.strftime('%M')} {x.strftime('%p')} {x.strftime('%x')}")
        except:
            pass
        pass
    def CopyPaths(self,*args):
        try:
            x=filedialog.askopenfilename()
            if x=="":
                pass
            else:
                pyperclip.copy(x)
        except:
            pass
        pass
    # word wrap
    def WordWrap_Func(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                ww=j.cget("wrap")
                                if ww=="none":
                                    j.config(wrap=WORD)
                                else:
                                    j.config(wrap="none")
        except:
            pass
        pass
    # show status
    def Show_Status_Func(self,*args):
        try:
            if self.Status_Show==True:
                self.Status_Show=False
                Status_Frame.grid_forget()
            elif self.Status_Show==False:
                self.Status_Show=True
                Status_Frame.grid(row=2,column=0,columnspan=3,sticky="nswe")
        except:
            pass
        pass
    # status data
    def Status_Data_func(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                words=len(j.get(0.0,END).split())
                                Letters=len(j.get(0.0,END).replace(" ",""))-1
                                pos=j.index(INSERT)
                                row,col=pos.split(".")
                                blank=" "*150
                                StatusBar.config(text=f"Words {words} Letters {Letters}{blank}Ln {row},Col {col}")
                                pass
            StatusBar.after(200,self.Status_Data_func)
        except:
            pass
        pass
    # show Folder
    def Show_Folder_Func(self,*args):
        try:
            if self.Folder_Show==True:
                self.Folder_Show=False
                FolderFrame.grid_forget()
                Panels.forget(FolderFrame)
                Folder_Var.set(0)
            elif self.Folder_Show==False:
                self.Folder_Show=True
                FolderFrame.grid(row=0,column=0,sticky="nswe")
                Panels.forget(NoteboxPanel)
                Panels.add(FolderFrame)
                Panels.add(NoteboxPanel)
                Folder_Var.set(1)
                folder_side.set(0)
        except:
            pass
        pass
    # show scrollbars
    def Show_Scrollbars_Func(self,*args):
        try:
            if self.Scrollbars_show==True:
                self.Scrollbars_show=False
                VerticalScroll.grid_forget()
                HorizontalScroll.grid_forget()
                Scroll_var.set(0)
            elif self.Scrollbars_show==False:
                self.Scrollbars_show=True
                VerticalScroll.grid(row=0,column=2,rowspan=2,sticky="nswe")
                HorizontalScroll.grid(row=1,column=1,sticky="nswe")
                Scroll_var.set(1)
        except:
            pass
        pass
    # show folder at the left side
    def Show_Folder_Left_func(self,*args):
        try:
            self.Folder_Show=True
            Folder_Var.set(1)
            FolderFrame.grid_forget()
            NoteboxPanel.grid_forget()
            Panels.forget(FolderFrame)
            Panels.forget(NoteboxPanel)
            FolderFrame.grid(row=0,column=0,sticky="nswe")
            NoteboxPanel.grid(row=0,column=1,sticky="nswe",padx=0,pady=0)
            Panels.add(FolderFrame)
            Panels.add(NoteboxPanel)
            folder_side.set(0)
        except:
            pass
        pass
    # show folder at th right side
    def Show_Folder_Right_func(self,*args):
        try:
            self.Folder_Show=True
            Folder_Var.set(1)
            FolderFrame.grid_forget()
            NoteboxPanel.grid_forget()
            Panels.forget(FolderFrame)
            Panels.forget(NoteboxPanel)
            NoteboxPanel.grid(row=0,column=0,sticky="nswe",padx=0,pady=0)
            FolderFrame.grid(row=0,column=1,sticky="nswe")
            Panels.add(NoteboxPanel)
            Panels.add(FolderFrame)
            Panels.paneconfigure(NoteboxPanel,width=int(root.winfo_screenwidth()/1.25))
            folder_side.set(1)
        except:
            pass
        pass
    # full screen
    def FullScreen_Func(self,*args):
        try:
            if self.FullScreen==True:
                self.FullScreen=False
                root.focus()
                root.wm_attributes("-fullscreen",False)
                FullScreen_Var.set(0)
            elif self.FullScreen==False:
                self.FullScreen=True
                root.focus()
                root.wm_attributes("-fullscreen",True)
                FullScreen_Var.set(1)
        except:
            pass
        pass
    # Show Tool bar 
    def Show_ToolBar_Func(self,*args):
        try:
            if self.ToolBar_Show==True:
                self.ToolBar_Show=False
                ToolBar.grid_forget()
                File_Show_button.grid(row=3,column=0,columnspan=3,sticky="nswe")
                Tool_var.set(0)
            elif self.ToolBar_Show==False:
                self.ToolBar_Show=True
                ToolBar.grid(row=0,column=0,rowspan=2,sticky="nswe")
                File_Show_button.grid_forget()
                Tool_var.set(1)
        except:
            pass
        pass
    # Themes
    def Theme_Func(self,*args):
        try:
            x=Theme_value.get()
            if x==0:
                ToolBar.config(bg="#444444")
                FileButton.config(bg="#444444",fg="white",activebackground="#646464",activeforeground="white")
                EditButton.config(bg="#444444",fg="white",activebackground="#646464",activeforeground="white")
                ViewButton.config(bg="#444444",fg="white",activebackground="#646464",activeforeground="white")
                HelpButton.config(bg="#444444",fg="white",activebackground="#646464",activeforeground="white")
                filemenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                editmenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                viewmenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                themeMenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                folder_side_menu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                helpMenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                StatusBar.config(bg="#444444",fg="white")
                Close_Button.config(bg="#252526",fg="white")
                Test_details.config(bg="#444444",fg="white")
                Panels.config(bg="#444444")
                FolderFrame.config(bg="#252526")
                Folder_name.config(bg="#252526",fg="white")
                File_Show_button.config(bg="#646464",fg="white")
                File_List.config(bg="white",fg="black",selectbackground="#a0a0a0",selectforeground="black")
                Add_File.config(bg="#a0a0a0",fg="black")
                back_Folder.config(bg="#a0a0a0",fg="black")
                Saved_Label.config(bg="#a0a0a0",fg="black")
                self.Option_check_color="white"
                viewmenu.config(selectcolor=App.Option_check_color)
                themeMenu.config(selectcolor=App.Option_check_color)
                folder_side_menu.config(selectcolor=App.Option_check_color)
                s.configure("TNotebook.Tab",font=("arial",11),background="#252526",foreground="white")
                s.configure("Horizontal.TScrollbar", gripcount=0, background="#a0a0a0",troughcolor='#444444', borderwidth=0,bordercolor='#252526', lightcolor='#444444', darkcolor='#444444',arrowsize=12)
                s.configure("Vertical.TScrollbar", gripcount=0, background="#a0a0a0",troughcolor='#444444', borderwidth=0,bordercolor='#252526', lightcolor='#444444', darkcolor='#444444',arrowsize=12)
                s.configure("TNotebook",background="#444444")
                # text box
                firstrow=NoteBox.winfo_children()
                for i in firstrow:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.config(bg="white",fg="black",insertbackground="black")
                pass
            elif x==1:
                ToolBar.config(bg="#252526")
                FileButton.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                EditButton.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                ViewButton.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                HelpButton.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                filemenu.config(bg="#a0a0a0",fg="black",activebackground="#252526",activeforeground="white")
                editmenu.config(bg="#a0a0a0",fg="black",activebackground="#252526",activeforeground="white")
                viewmenu.config(bg="#a0a0a0",fg="black",activebackground="#252526",activeforeground="white")
                themeMenu.config(bg="#a0a0a0",fg="black",activebackground="#252526",activeforeground="white")
                folder_side_menu.config(bg="#a0a0a0",fg="black",activebackground="#252526",activeforeground="white")
                helpMenu.config(bg="#a0a0a0",fg="black",activebackground="#252526",activeforeground="white")
                StatusBar.config(bg="#252526",fg="white")
                Close_Button.config(bg="#a0a0a0",fg="black")
                Test_details.config(bg="#252526",fg="white")
                Panels.config(bg="#252526")
                FolderFrame.config(bg="#a0a0a0")
                Folder_name.config(bg="#a0a0a0",fg="black")
                File_Show_button.config(bg="#a0a0a0",fg="black")
                File_List.config(bg="#1e1e1e",fg="white",selectbackground="#a0a0a0",selectforeground="black")
                Add_File.config(bg="#a0a0a0",fg="black")
                back_Folder.config(bg="#a0a0a0",fg="black")
                Saved_Label.config(bg="#a0a0a0",fg="black")
                self.Option_check_color="black"
                viewmenu.config(selectcolor=App.Option_check_color)
                themeMenu.config(selectcolor=App.Option_check_color)
                folder_side_menu.config(selectcolor=App.Option_check_color)
                s.configure("TNotebook.Tab",font=("arial",11),background="#a0a0a0",foreground="black")
                s.configure("Horizontal.TScrollbar", gripcount=0, background="#1e1e1e",troughcolor='#252526', borderwidth=0,bordercolor='#a0a0a0', lightcolor='#252526', darkcolor='#252526',arrowsize=12)
                s.configure("Vertical.TScrollbar", gripcount=0, background="#1e1e1e",troughcolor='#252526', borderwidth=0,bordercolor='#a0a0a0', lightcolor='#252526', darkcolor='#252526',arrowsize=12)
                s.configure("TNotebook",background="#252526")
                # text box
                firstrow=NoteBox.winfo_children()
                for i in firstrow:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.config(bg="#1e1e1e",fg="white",insertbackground="white")
                pass
            elif x==2:
                ToolBar.config(bg="black")
                FileButton.config(bg="black",fg="white",activebackground="#252526",activeforeground="white")
                EditButton.config(bg="black",fg="white",activebackground="#252526",activeforeground="white")
                ViewButton.config(bg="black",fg="white",activebackground="#252526",activeforeground="white")
                HelpButton.config(bg="black",fg="white",activebackground="#252526",activeforeground="white")
                filemenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                editmenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                viewmenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                themeMenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                folder_side_menu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                helpMenu.config(bg="#252526",fg="white",activebackground="#a0a0a0",activeforeground="black")
                StatusBar.config(bg="black",fg="white")
                Close_Button.config(bg="#252526",fg="white")
                Test_details.config(bg="black",fg="white")
                Panels.config(bg="black")
                FolderFrame.config(bg="#252526")
                Folder_name.config(bg="#252526",fg="white")
                File_Show_button.config(bg="#a0a0a0",fg="black")
                File_List.config(bg="#a0a0a0",fg="black",selectbackground="#3f3f3f",selectforeground="white")
                Add_File.config(bg="#3f3f3f",fg="white")
                back_Folder.config(bg="#3f3f3f",fg="white")
                Saved_Label.config(bg="#3f3f3f",fg="white")
                self.Option_check_color="white"
                viewmenu.config(selectcolor=App.Option_check_color)
                themeMenu.config(selectcolor=App.Option_check_color)
                folder_side_menu.config(selectcolor=App.Option_check_color)
                s.configure("TNotebook.Tab",font=("arial",11),background="#252526",foreground="white")
                s.configure("Horizontal.TScrollbar", gripcount=0, background="#a0a0a0",troughcolor='black', borderwidth=0,bordercolor='#252526', lightcolor='black', darkcolor='black',arrowsize=12)
                s.configure("Vertical.TScrollbar", gripcount=0, background="#a0a0a0",troughcolor='black', borderwidth=0,bordercolor='#252526', lightcolor='black', darkcolor='black',arrowsize=12)
                s.configure("TNotebook",background="black")
                # text box
                firstrow=NoteBox.winfo_children()
                for i in firstrow:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.config(bg="#a0a0a0",fg="black",insertbackground="black")
                pass
            elif x==3:
                ToolBar.config(bg="#580000")
                FileButton.config(bg="#580000",fg="white",activebackground="#770000",activeforeground="white")
                EditButton.config(bg="#580000",fg="white",activebackground="#770000",activeforeground="white")
                ViewButton.config(bg="#580000",fg="white",activebackground="#770000",activeforeground="white")
                HelpButton.config(bg="#580000",fg="white",activebackground="#770000",activeforeground="white")
                filemenu.config(bg="#770000",fg="white",activebackground="#580000",activeforeground="white")
                editmenu.config(bg="#770000",fg="white",activebackground="#580000",activeforeground="white")
                viewmenu.config(bg="#770000",fg="white",activebackground="#580000",activeforeground="white")
                themeMenu.config(bg="#770000",fg="white",activebackground="#580000",activeforeground="white")
                folder_side_menu.config(bg="#770000",fg="white",activebackground="#580000",activeforeground="white")
                helpMenu.config(bg="#770000",fg="white",activebackground="#580000",activeforeground="white")
                StatusBar.config(bg="#580000",fg="white")
                Close_Button.config(bg="#770000",fg="white")
                Test_details.config(bg="#580000",fg="white")
                Panels.config(bg="#580000")
                FolderFrame.config(bg="red")
                Folder_name.config(bg="red",fg="white")
                File_Show_button.config(bg="red",fg="white")
                File_List.config(bg="#770000",fg="white",selectbackground="#580000",selectforeground="white")
                Add_File.config(bg="#770000",fg="white")
                back_Folder.config(bg="#770000",fg="white")
                Saved_Label.config(bg="#770000",fg="white")
                self.Option_check_color="white"
                viewmenu.config(selectcolor=App.Option_check_color)
                themeMenu.config(selectcolor=App.Option_check_color)
                folder_side_menu.config(selectcolor=App.Option_check_color)
                s.configure("TNotebook.Tab",font=("arial",11),background="red",foreground="white")
                s.configure("Horizontal.TScrollbar", gripcount=0, background="#580000",troughcolor='#580000', borderwidth=0,bordercolor='#770000', lightcolor='#580000', darkcolor='#580000',arrowsize=12)
                s.configure("Vertical.TScrollbar", gripcount=0, background="#580000",troughcolor='#580000', borderwidth=0,bordercolor='#770000', lightcolor='#580000', darkcolor='#580000',arrowsize=12)
                s.configure("TNotebook",background="#580000")
                # text box
                firstrow=NoteBox.winfo_children()
                for i in firstrow:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.config(bg="#770000",fg="white",insertbackground="white")
                pass
            elif x==4:
                ToolBar.config(bg="#000095")
                FileButton.config(bg="#000095",fg="white",activebackground="#0000ff",activeforeground="white")
                EditButton.config(bg="#000095",fg="white",activebackground="#0000ff",activeforeground="white")
                ViewButton.config(bg="#000095",fg="white",activebackground="#0000ff",activeforeground="white")
                HelpButton.config(bg="#000095",fg="white",activebackground="#0000ff",activeforeground="white")
                filemenu.config(bg="#0000ff",fg="white",activebackground="#000095",activeforeground="white")
                editmenu.config(bg="#0000ff",fg="white",activebackground="#000095",activeforeground="white")
                viewmenu.config(bg="#0000ff",fg="white",activebackground="#000095",activeforeground="white")
                themeMenu.config(bg="#0000ff",fg="white",activebackground="#000095",activeforeground="white")
                folder_side_menu.config(bg="#0000ff",fg="white",activebackground="#000095",activeforeground="white")
                helpMenu.config(bg="#0000ff",fg="white",activebackground="#000095",activeforeground="white")
                StatusBar.config(bg="#000095",fg="white")
                Close_Button.config(bg="#0000ff",fg="white")
                Test_details.config(bg="#000095",fg="white")
                Panels.config(bg="#000095")
                FolderFrame.config(bg="blue")
                Folder_name.config(bg="blue",fg="white")
                File_Show_button.config(bg="blue",fg="white")
                File_List.config(bg="#000095",fg="yellow",selectbackground="#0000ff",selectforeground="white")
                Add_File.config(bg="#000095",fg="white")
                back_Folder.config(bg="#000095",fg="white")
                Saved_Label.config(bg="#000095",fg="white")
                self.Option_check_color="white"
                viewmenu.config(selectcolor=App.Option_check_color)
                themeMenu.config(selectcolor=App.Option_check_color)
                folder_side_menu.config(selectcolor=App.Option_check_color)
                s.configure("TNotebook.Tab",font=("arial",11),background="blue",foreground="white")
                s.configure("Horizontal.TScrollbar", gripcount=0, background="#000095",troughcolor='#000095', borderwidth=0,bordercolor='#0000ff', lightcolor='#000095', darkcolor='#000095',arrowsize=12)
                s.configure("Vertical.TScrollbar", gripcount=0, background="#000095",troughcolor='#000095', borderwidth=0,bordercolor='#0000ff', lightcolor='#000095', darkcolor='#000095',arrowsize=12)
                s.configure("TNotebook",background="#000095")
                # text box
                firstrow=NoteBox.winfo_children()
                for i in firstrow:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.config(bg="#0000ff",fg="black",insertbackground="white")
                pass
            elif x==5:
                ToolBar.config(bg="#008000")
                FileButton.config(bg="#008000",fg="black",activebackground="#00ff00",activeforeground="black")
                EditButton.config(bg="#008000",fg="black",activebackground="#00ff00",activeforeground="black")
                ViewButton.config(bg="#008000",fg="black",activebackground="#00ff00",activeforeground="black")
                HelpButton.config(bg="#008000",fg="black",activebackground="#00ff00",activeforeground="black")
                filemenu.config(bg="#00ff00",fg="black",activebackground="#008000",activeforeground="black")
                editmenu.config(bg="#00ff00",fg="black",activebackground="#008000",activeforeground="black")
                viewmenu.config(bg="#00ff00",fg="black",activebackground="#008000",activeforeground="black")
                themeMenu.config(bg="#00ff00",fg="black",activebackground="#008000",activeforeground="black")
                folder_side_menu.config(bg="#00ff00",fg="black",activebackground="#008000",activeforeground="black")
                helpMenu.config(bg="#00ff00",fg="black",activebackground="#008000",activeforeground="black")
                StatusBar.config(bg="#008000",fg="black")
                Close_Button.config(bg="#00ff00",fg="black")
                Test_details.config(bg="#008000",fg="black")
                Panels.config(bg="#008000")
                FolderFrame.config(bg="#005e00")
                Folder_name.config(bg="#005e00",fg="black")
                File_Show_button.config(bg="#005e00",fg="black")
                File_List.config(bg="#00ff00",fg="black",selectbackground="#005e00",selectforeground="black")
                Add_File.config(bg="#00ff00",fg="black")
                back_Folder.config(bg="#00ff00",fg="black")
                Saved_Label.config(bg="#00ff00",fg="black")
                self.Option_check_color="black"
                viewmenu.config(selectcolor=App.Option_check_color)
                themeMenu.config(selectcolor=App.Option_check_color)
                folder_side_menu.config(selectcolor=App.Option_check_color)
                s.configure("TNotebook.Tab",font=("arial",11),background="#005e00",foreground="white")
                s.configure("Horizontal.TScrollbar", gripcount=0, background="#008000",troughcolor='#008000', borderwidth=0,bordercolor='#00ff00', lightcolor='#008000', darkcolor='#008000',arrowsize=12)
                s.configure("Vertical.TScrollbar", gripcount=0, background="#008000",troughcolor='#008000', borderwidth=0,bordercolor='#00ff00', lightcolor='#008000', darkcolor='#008000',arrowsize=12)
                s.configure("TNotebook",background="#008000")
                # text box
                firstrow=NoteBox.winfo_children()
                for i in firstrow:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.config(bg="#00ff00",fg="black",insertbackground="black")
                pass
            elif x==6:
                ToolBar.config(bg="#787878")
                FileButton.config(bg="#787878",fg="black",activebackground="#a0a0a0",activeforeground="black")
                EditButton.config(bg="#787878",fg="black",activebackground="#a0a0a0",activeforeground="black")
                ViewButton.config(bg="#787878",fg="black",activebackground="#a0a0a0",activeforeground="black")
                HelpButton.config(bg="#787878",fg="black",activebackground="#a0a0a0",activeforeground="black")
                filemenu.config(bg="#a0a0a0",fg="black",activebackground="#787878",activeforeground="black")
                editmenu.config(bg="#a0a0a0",fg="black",activebackground="#787878",activeforeground="black")
                viewmenu.config(bg="#a0a0a0",fg="black",activebackground="#787878",activeforeground="black")
                themeMenu.config(bg="#a0a0a0",fg="black",activebackground="#787878",activeforeground="black")
                folder_side_menu.config(bg="#a0a0a0",fg="black",activebackground="#787878",activeforeground="black")
                helpMenu.config(bg="#a0a0a0",fg="black",activebackground="#787878",activeforeground="black")
                StatusBar.config(bg="#787878",fg="black")
                Close_Button.config(bg="#a0a0a0",fg="black")
                Test_details.config(bg="#787878",fg="black")
                Panels.config(bg="#787878")
                FolderFrame.config(bg="#c0c0c0")
                Folder_name.config(bg="#c0c0c0",fg="black")
                File_Show_button.config(bg="#c0c0c0",fg="black")
                File_List.config(bg="#a0a0a0",fg="black",selectbackground="#c0c0c0",selectforeground="black")
                Add_File.config(bg="#a0a0a0",fg="black")
                back_Folder.config(bg="#a0a0a0",fg="black")
                Saved_Label.config(bg="#a0a0a0",fg="black")
                self.Option_check_color="black"
                viewmenu.config(selectcolor=App.Option_check_color)
                themeMenu.config(selectcolor=App.Option_check_color)
                folder_side_menu.config(selectcolor=App.Option_check_color)
                s.configure("TNotebook.Tab",font=("arial",11),background="#c0c0c0",foreground="black")
                s.configure("Horizontal.TScrollbar", gripcount=0, background="#787878",troughcolor='#787878', borderwidth=0,bordercolor='#a0a0a0', lightcolor='#787878', darkcolor='#787878',arrowsize=12)
                s.configure("Vertical.TScrollbar", gripcount=0, background="#787878",troughcolor='#787878', borderwidth=0,bordercolor='#a0a0a0', lightcolor='#787878', darkcolor='#787878',arrowsize=12)
                s.configure("TNotebook",background="#787878")
                # text box
                firstrow=NoteBox.winfo_children()
                for i in firstrow:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.config(bg="#a0a0a0",fg="black",insertbackground="black")
                pass
            elif x==7:
                ToolBar.config(bg="#8000ff")
                FileButton.config(bg="#8000ff",fg="black",activebackground="yellow",activeforeground="black")
                EditButton.config(bg="#8000ff",fg="black",activebackground="yellow",activeforeground="black")
                ViewButton.config(bg="#8000ff",fg="black",activebackground="yellow",activeforeground="black")
                HelpButton.config(bg="#8000ff",fg="black",activebackground="yellow",activeforeground="black")
                filemenu.config(bg="yellow",fg="black",activebackground="#8000ff",activeforeground="black")
                editmenu.config(bg="yellow",fg="black",activebackground="#8000ff",activeforeground="black")
                viewmenu.config(bg="yellow",fg="black",activebackground="#8000ff",activeforeground="black")
                themeMenu.config(bg="yellow",fg="black",activebackground="#8000ff",activeforeground="black")
                folder_side_menu.config(bg="yellow",fg="black",activebackground="#8000ff",activeforeground="black")
                helpMenu.config(bg="yellow",fg="black",activebackground="#8000ff",activeforeground="black")
                StatusBar.config(bg="#8000ff",fg="black")
                Close_Button.config(bg="yellow",fg="black")
                Test_details.config(bg="#8000ff",fg="black")
                Panels.config(bg="#8000ff")
                FolderFrame.config(bg="#400080")
                Folder_name.config(bg="#400080",fg="white")
                File_Show_button.config(bg="#400080",fg="black")
                File_List.config(bg="yellow",fg="black",selectbackground="#400080",selectforeground="white")
                Add_File.config(bg="yellow",fg="black")
                back_Folder.config(bg="yellow",fg="black")
                Saved_Label.config(bg="yellow",fg="black")
                self.Option_check_color="black"
                viewmenu.config(selectcolor=App.Option_check_color)
                themeMenu.config(selectcolor=App.Option_check_color)
                folder_side_menu.config(selectcolor=App.Option_check_color)
                s.configure("TNotebook.Tab",font=("arial",11),background="#400080",foreground="white")
                s.configure("Horizontal.TScrollbar", gripcount=0, background="#8000ff",troughcolor='#8000ff', borderwidth=0,bordercolor='yellow', lightcolor='#8000ff', darkcolor='#8000ff',arrowsize=12)
                s.configure("Vertical.TScrollbar", gripcount=0, background="#8000ff",troughcolor='#8000ff', borderwidth=0,bordercolor='yellow', lightcolor='#8000ff', darkcolor='#8000ff',arrowsize=12)
                s.configure("TNotebook",background="#8000ff")
                # text box
                firstrow=NoteBox.winfo_children()
                for i in firstrow:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                j.config(bg="yellow",fg="black",insertbackground="black")
                pass
        except:
            pass
        pass
    # reset
    def ResetAll_Func(self,*args):
        try:
            x=messagebox.askquestion("Reset","Do You want to Reset all changes")
            if x=="yes":
                self.FileURL=""
                self.FileName=""
                self.FileExtension=""
                self.DirURL=""
                self.img_multiplier=1
                self.delta=0.75
                self.Font_Face="arial"
                self.Font_Size=14
                self.Font_Style="none"
                self.Remove_AllTabs()
                self.title="MultiNote - Untitled"
                self.Total_Tabs=1
                self.no=1
                self.Tab_name=f"Untitled-{self.no}"
                Theme_value.set(0)
                self.Theme_Func()
                File_List.selection_clear(0,END)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                if self.Font_Style=="none":
                                    j.config(font=(self.Font_Face,self.Font_Size))
                                else:
                                    j.config(font=(self.Font_Face,self.Font_Size,self.Font_Style))
            else:
                pass
        except:
            pass
    # short cut Keys
    def shortcutKeys(self):
        try:
            short_win=Toplevel()
            short_win.title("ShortCut Keys")
            # short_win.geometry("400x300")
            short_win.config(bg="#252526",borderwidth=2,relief=SOLID)
            short_win.resizable(0,0)
            try:
                short_win.wm_iconbitmap(self.WinIcon)
            except:
                pass
            for i in range(2):
                short_win.columnconfigure(i,weight=1)
            keys=["New File","Open File","Save File","Save As","Delete Tab","Delete All Tabs","Change Text Size","Change Image Size","Rotate Image","Full Screen","Dublicate Line","Dublicate line(multiple)","Date and Time","Focus on Tabs","File Details"]
            keys1=["Ctrl+n","Ctrl+o","Ctrl+s","Ctrl+Shift+s","Ctrl+w","Control-Shift-w","Shift MouseWheel","Ctrl MouseWheel","Alt MouseWheel","F11","F2","F3","F5","Ctrl+t","Alt+B"]
            for i in range(len(keys)):
                short_win.rowconfigure(i,weight=1)
                for j in range(1):
                    Label(short_win,text=f"{keys[i]}",font=("arial",13,"bold"),bg="#444444",fg="white",borderwidth=1,relief=SOLID,padx=5,pady=5).grid(row=i,column=j,padx=2,pady=2,sticky="nswe")
                    Label(short_win,text=f"{keys1[i]}",font=("arial",13,"bold"),bg="#444444",fg="white",borderwidth=1,relief=SOLID,padx=5,pady=5).grid(row=i,column=j+1,padx=2,pady=2,sticky="nswe")
            short_win.grab_set()
            short_win.focus()
        except:
            pass
        pass
    # about
    def about(self,*args):
        try:
            messagebox.showinfo("About",f"Version:-1.0.0\nOperating System:-Windows")
        except:
            pass
        pass
    # font window
    def Font_Win_Func(self,*args):
        try:
            self.Font_Win=Toplevel()
            self.Font_Win.title("Font")
            self.Font_Win.config(bg="#252526")
            self.Font_Win.resizable(0,0)
            try:
                self.Font_Win.wm_iconbitmap(self.WinIcon)
            except:
                pass
            # labels
            Label(self.Font_Win,text="Font Face",font=("arial",15,"bold"),bg="#444444",fg="yellow").grid(row=0,column=0,padx=4,pady=4,sticky="nswe")
            Label(self.Font_Win,text="Font Style",font=("arial",15,"bold"),bg="#444444",fg="yellow").grid(row=0,column=1,padx=4,pady=4,sticky="nswe")
            Label(self.Font_Win,text="Font Size",font=("arial",15,"bold"),bg="#444444",fg="yellow").grid(row=0,column=2,padx=4,pady=4,sticky="nswe")
            # entry box
            self.E1=StringVar()
            self.E2=StringVar()
            fonts=font.families()
            self.com1=ttk.Combobox(self.Font_Win,font=("arial",15,"bold"),state="readonly",textvariable=self.E1)
            self.com1.grid(row=1,column=0,padx=4,pady=4,sticky="nswe")
            self.com2=ttk.Combobox(self.Font_Win,font=("arial",15,"bold"),state="readonly",textvariable=self.E2)
            self.com2.grid(row=1,column=1,padx=4,pady=4,sticky="nswe")
            self.com1["value"]=fonts
            self.com1.set(self.Font_Face)

            self.com2["value"]=("none","bold","underline","italic")
            self.com2.set(self.Font_Style)

            self.display_FSize=Label(self.Font_Win,text=f"{self.Font_Size}",font=("arial",15,"bold"),bg="#444444",fg="yellow")
            self.display_FSize.grid(row=1,column=2,padx=4,pady=4,sticky="nswe")

            self.com1.bind("<<ComboboxSelected>>",self.Choose_Option)
            self.com2.bind("<<ComboboxSelected>>",self.Choose_Option)
            self.Font_Win.grab_set()
            self.Font_Win.focus()
        except:
            pass
        pass
    # choose options
    def Choose_Option(self,*args):
        try:
            family=self.E1.get()
            styles=self.E2.get()
            self.Font_Face=family
            self.Font_Style=styles
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                if styles=="none":
                                    j.config(font=(self.Font_Face,self.Font_Size))
                                else:
                                    j.config(font=(self.Font_Face,self.Font_Size,self.Font_Style))
        except:
            pass
        pass
    # Add Files Window
    def Add_File_Win_Func(self,*args):
        try:
            if self.DirURL!="":
                self.Add_Win=Toplevel()
                self.Add_Win.title("Add File")
                self.Add_Win.geometry(f"+{0}+{0}")
                self.Add_Win.resizable(0,0)
                self.Add_Win.overrideredirect(True)
                self.Add_Win.config(bg="#444444",pady=4,padx=4)
                Label(self.Add_Win,text="Enter the File name with Extension",font=("arial",15,"bold"),bg="#444444",fg="yellow").grid(row=0,column=0,columnspan=2,padx=4,pady=4,sticky="nswe")
                self.Ok_file_name=StringVar()
                Entry(self.Add_Win,textvariable=self.Ok_file_name,font=("arial",15,"bold"),highlightthickness=1,highlightbackground="yellow",highlightcolor="yellow").grid(row=1,column=0,columnspan=2,padx=4,pady=4,sticky="nswe")
                # ok button
                Button(self.Add_Win,text="Ok",font=("arial",15,"bold"),bg="yellow",fg="black",borderwidth=0,activebackground="yellow",activeforeground="black",command=self.Add_file_Func,cursor="hand2").grid(row=2,column=0,padx=4,pady=4,sticky="nswe")
                # Cancel button
                Button(self.Add_Win,text="Cancel",font=("arial",15,"bold"),bg="yellow",fg="black",borderwidth=0,activebackground="yellow",activeforeground="black",command=self.Close_Add_File_Win,cursor="hand2").grid(row=2,column=1,padx=4,pady=4,sticky="nswe")
                self.Add_Win.bind("<Return>",self.Add_file_Func)
                self.Add_Win.grab_set()
                self.Add_Win.focus()
        except:
            pass
        pass
    # close Add File Window
    def Close_Add_File_Win(self,*args):
        try:
            self.Add_Win.destroy()
        except:
            pass
        pass
    # Add Files button
    def Add_file_Func(self,*args):
        try:
            if self.DirURL!="":
                if self.Ok_file_name.get()=="":
                    pass
                else:
                    os.chdir(self.DirURL)
                    # creates file
                    f=open(self.Ok_file_name.get(),"w+")
                    f.close()
                    self.FileURL=os.path.abspath(self.Ok_file_name.get())
                    self.FileName=os.path.basename(self.FileURL)
                    self.FileExtension=os.path.splitext(self.FileName)[1]
                    # open file in tab
                    f1=Frame(NoteBox)
                    Label(f1,text=self.FileURL,bg="yellow").pack_forget()
                    Button(f1,text="saved").pack_forget()
                    t1=Text(f1,font=(App.Font_Face,App.Font_Size),borderwidth=1,relief=SOLID,wrap='none',undo=True,tabs=self.Tabs_Space)
                    t1.pack(fill=BOTH,expand=True)
                        
                    f1.pack(fill=BOTH,expand=True)
                    NoteBox.add(f1,text=self.FileName,padding=(-1, -1, -3, -3))
                    t1.delete(0.0,END)
                    NoteBox.select(NoteBox.index(END)-1)
                    self.Total_Tabs=self.Total_Tabs+1
                    self.Ok_file_name.set("")
                    self.Add_Win.destroy()
                    # add the file in list
                    File_List.insert(END,self.FileName)
                    File_List.selection_clear(0,END)
                    File_List.select_set(END)
                    self.Theme_Func()
        except:
            pass
        pass
    # open Right window
    def Open_RightWin_Func(self,e):
        try:
            if self.Open_RightClick_Window==True:
                self.Open_RightClick_Window=False
                self.Right_Win.destroy()
            if self.Open_RightClick_Window==False:
                self.Open_RightClick_Window=True
                # window
                self.Right_Win=Toplevel()
                self.Right_Win.overrideredirect(True)
                self.Right_Win.geometry(f"+{int(e.x+220)}+{e.y+20}")
                self.Right_Win.config(highlightthickness=2,highlightbackground="black",highlightcolor="black")
                Button(self.Right_Win,text="Undo",anchor="w",bg="#444444",fg="white",font=("arial",10,"bold"),borderwidth=1,relief=SOLID,activebackground="#252526",activeforeground="white",cursor="hand2",width=20,command=lambda:[self.Undos(),self.Close_RightWin_Func()]).pack(fill=X)
                Button(self.Right_Win,text="Redo",anchor="w",bg="#444444",fg="white",font=("arial",10,"bold"),borderwidth=1,relief=SOLID,activebackground="#252526",activeforeground="white",cursor="hand2",width=20,command=lambda:[self.Redos(),self.Close_RightWin_Func()]).pack(fill=X)
                Button(self.Right_Win,text="Cut",anchor="w",bg="#444444",fg="white",font=("arial",10,"bold"),borderwidth=1,relief=SOLID,activebackground="#252526",activeforeground="white",cursor="hand2",width=20,command=lambda:[self.Cuts(),self.Close_RightWin_Func()]).pack(fill=X)
                Button(self.Right_Win,text="Copy",anchor="w",bg="#444444",fg="white",font=("arial",10,"bold"),borderwidth=1,relief=SOLID,activebackground="#252526",activeforeground="white",cursor="hand2",width=20,command=lambda:[self.Copys(),self.Close_RightWin_Func()]).pack(fill=X)
                Button(self.Right_Win,text="Paste",anchor="w",bg="#444444",fg="white",font=("arial",10,"bold"),borderwidth=1,relief=SOLID,activebackground="#252526",activeforeground="white",cursor="hand2",width=20,command=lambda:[self.Pastes(),self.Close_RightWin_Func()]).pack(fill=X)
                Button(self.Right_Win,text="Select All",anchor="w",bg="#444444",fg="white",font=("arial",10,"bold"),borderwidth=1,relief=SOLID,activebackground="#252526",activeforeground="white",cursor="hand2",width=20,command=lambda:[self.SelectAll(),self.Close_RightWin_Func()]).pack(fill=X)
                Button(self.Right_Win,text="Date and Time",anchor="w",bg="#444444",fg="white",font=("arial",10,"bold"),borderwidth=1,relief=SOLID,activebackground="#252526",activeforeground="white",cursor="hand2",width=20,command=lambda:[self.Dateandtime_Func(),self.Close_RightWin_Func()]).pack(fill=X)
                Button(self.Right_Win,text="Format",anchor="w",bg="#444444",fg="white",font=("arial",10,"bold"),borderwidth=1,relief=SOLID,activebackground="#252526",activeforeground="white",cursor="hand2",width=20,command=lambda:[self.Proper_Format(),self.Close_RightWin_Func()]).pack(fill=X)
                self.Right_Win.mainloop()
        except:
            pass
        pass
    # close right window
    def Close_RightWin_Func(self,*args):
        try:
            if self.Open_RightClick_Window==True:
                self.Open_RightClick_Window=False
                self.Right_Win.destroy()
        except:
            pass
        pass
    # dublicate line
    def Dublicate_line(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                linestart=j.index("insert linestart")
                                lineend=j.index("insert lineend")
                                x=j.get(linestart,lineend)
                                j.insert(lineend,f"\n{x}")
                                pass
        except:
            pass
        pass
    # dublicate lines
    def Dublicate_noline(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                no=simpledialog.askinteger("Number","Enter the number of Dubicate lines")
                                if no=="":
                                    pass
                                else:
                                    linestart=j.index("insert linestart")
                                    lineend=j.index("insert lineend")
                                    x=j.get(linestart,lineend)
                                    for i in range(no):
                                        j.insert(lineend,f"\n{x}")
                                pass
        except:
            pass
        pass
    # find and replace window
    def Open_Find_Replace_Win_Func(self,*args):
        try:
            self.Find_Win=Toplevel()
            self.Find_Win.title("Find Replace")
            self.Find_Win.config(bg="#252526")
            self.Find_Win.resizable(0,0)
            try:
                self.Find_Win.wm_iconbitmap(self.WinIcon)
            except:
                pass
            # labels
            Label(self.Find_Win,text="Find",font=("arial",15,"bold"),bg="#252526",fg="yellow",anchor="w").grid(row=0,column=0,padx=2,pady=2,sticky="nswe")
            Label(self.Find_Win,text="Replace",font=("arial",15,"bold"),bg="#252526",fg="yellow",anchor="w").grid(row=1,column=0,padx=2,pady=2,sticky="nswe")
            self.Remaining_txt=Label(self.Find_Win,font=("arial",15,"bold"),bg="#252526",fg="yellow",anchor="w")
            self.Remaining_txt.grid(row=3,column=0,columnspan=3,padx=2,pady=2,sticky="nswe")
            # entry box
            self.find_var=StringVar()
            self.replace_var=StringVar()
            Entry(self.Find_Win,font=("arial",15,"bold"),highlightthickness=1,highlightbackground="yellow",highlightcolor="yellow",textvariable=self.find_var).grid(row=0,column=1,columnspan=3,pady=2,padx=2,sticky="nswe")
            Entry(self.Find_Win,font=("arial",15,"bold"),highlightthickness=1,highlightbackground="yellow",highlightcolor="yellow",textvariable=self.replace_var).grid(row=1,column=1,columnspan=3,pady=2,padx=2,sticky="nswe")
            # buttons
            Button(self.Find_Win,text="Find",font=("arial",15,"bold"),bg="yellow",fg="#252526",command=self.Find_Func).grid(row=2,column=0,padx=2,pady=2,sticky="nswe")
            Button(self.Find_Win,text="Replace",font=("arial",15,"bold"),bg="yellow",fg="#252526",command=self.ReplaceOnce_Func).grid(row=2,column=2,padx=2,pady=2,sticky="nswe")
            Button(self.Find_Win,text="Replace All",font=("arial",15,"bold"),bg="yellow",fg="#252526",command=self.ReplaceOAll_Func).grid(row=2,column=3,padx=2,pady=2,sticky="nswe")
            self.Find_Win.grab_set()
            self.Find_Win.focus()
        except:
            pass
        pass
    # find function
    def Find_Func(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if isinstance(i,Frame):
                    secondrow=i.winfo_children()
                    for j in secondrow:
                        if isinstance(j,Text):
                            search_var=self.find_var.get()
                            j.tag_remove("Finds","1.0",END)
                            if search_var!="":
                                idx="1.0"
                                while True:
                                    idx=j.search(search_var,idx,nocase=True,stopindex=END)
                                    if not idx: break
                                    lastidx='% s+% dc' % (idx, len(search_var))
                                    j.tag_add("found",idx,lastidx)
                                    idx=lastidx
                                j.tag_config("found",background=self.Highlights,foreground="black")
                            pass
        except:
            pass
        pass
    # Replace Once
    def ReplaceOnce_Func(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                x=j.get(0.0,END)
                                src=re.compile((r"\b"+self.find_var.get()+r"\b"),re.IGNORECASE)

                                self.numbers_words=len(re.findall(src,x))-1
                                self.now_words=(self.numbers_words-(self.numbers_words-1))

                                new_str=re.sub(src,self.replace_var.get(),x,self.now_words)
                                j.delete(0.0,END)
                                j.insert(END,new_str.strip())
                                if self.numbers_words>=0:
                                    self.Remaining_txt.config(text=f"0 of {self.numbers_words}")
                                pass
        except:
            pass
    # Replace All
    def ReplaceOAll_Func(self,*args):
        try:
            curr=NoteBox.index(CURRENT)
            firstrow=NoteBox.winfo_children()
            for index,i in enumerate(firstrow):
                if index==curr:
                    if isinstance(i,Frame):
                        secondrow=i.winfo_children()
                        for j in secondrow:
                            if isinstance(j,Text):
                                x=j.get(0.0,END)
                                src=re.compile((r"\b"+self.find_var.get()+r"\b"),re.IGNORECASE)

                                self.numbers_words=len(re.findall(src,x))
                                self.now_words=(self.numbers_words)

                                new_str=re.sub(src,self.replace_var.get(),x)
                                j.delete(0.0,END)
                                j.insert(END,new_str.strip())
                                if self.numbers_words>=1:
                                    self.Remaining_txt.config(text=f"0 of 0")
                                pass
        except:
            pass
        pass
    # focus Tabs
    def Focus_Tabs(self,*args):
        try:
            NoteBox.focus()
        except:
            pass
        pass
    # modified text
    def Modified_text(self,*args):
        try:
            if self.FileExtension not in self.img_list and self.FileExtension!=".gif":
                curr=NoteBox.index(CURRENT)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if index==curr:
                        if isinstance(i,Frame):
                            secondrow=i.winfo_children()
                            for j in secondrow:
                                if isinstance(j,Text):
                                    j.bind("<<Modified>>",self.Modified_text)
                                    if j.edit_modified()==True:
                                        Saved_Label.config(text="Modified")
                                        for n in secondrow:
                                            if isinstance(n,Button):
                                                n.config(text="Unsaved")
                                        j.edit_modified(False)
                                if isinstance(j,Button):
                                    data=j.cget('text')
                                    if data=="saved":
                                        Saved_Label.config(text="")
                                    if data=="Unsaved":
                                        Saved_Label.config(text="Modified")
            if self.FileExtension==".gif" or self.FileExtension in self.img_list:
                Saved_Label.config(text="")
                pass
        except:
            pass
        pass
    # Ask to save files
    def Ask_Save_File(self,*args):
        # Tabs
        Tabs=[]
        Tab_list=[]
        Name_List=[]
        Not_Saved_List=[]
        # to get the tab names
        for i in NoteBox.tabs():
            Tabs.append(NoteBox.tab(i,"text"))
        firstrow=NoteBox.winfo_children()
        # to get files status
        for index,i in enumerate(firstrow):
            if isinstance(i,Frame):
                secondrow=i.winfo_children()
                for j in secondrow:
                    if isinstance(j,Button):
                        txt=j.cget("text")
                        if txt=="Unsaved":
                            Tab_list.append(False)
                        elif txt=="saved":
                            Tab_list.append(True)
        # to get which files are not saved
        if False in Tab_list:
            for index,i in enumerate(Tab_list):
                if i==False:
                    Not_Saved_List.append(index)
            for index,j in enumerate(Tabs):
                if index in Not_Saved_List:
                    Name_List.append(j)
            # to save file/files or not
            query=", ".join(Name_List)
            prompts=messagebox.askquestion("Exit",f"Do you want to save this files\n{query}")
            if prompts=="yes":
                pass
            else:
                root.destroy()
        else:
            root.destroy()
        pass
    # Proper Format
    def Proper_Format(self,*args):
        try:
            if self.FileExtension==".html" or self.FileExtension==".xml":
                curr=NoteBox.index(CURRENT)
                firstrow=NoteBox.winfo_children()
                for index,i in enumerate(firstrow):
                    if index==curr:
                        if isinstance(i,Frame):
                            secondrow=i.winfo_children()
                            for j in secondrow:
                                if isinstance(j,Text):
                                    data=j.get(0.0,END).strip()
                                    soup=BeautifulSoup(data,"html.parser")
                                    forms=soup.prettify()
                                    j.delete(0.0,END)
                                    j.insert(END,forms.strip())
        except:
            pass
        pass
    # File Description
    def File_Description_Func(self,*args):
        try:
            if self.FileDetials_show==True:
                self.FileDetials_show=False
                Test_details.grid(row=1,column=1,sticky="nswe",padx=0,pady=0)
                self.File_Details_Func()
                NoteboxPanel.add(Test_details)
                Filedetails_Var.set(1)
            elif self.FileDetials_show==False:
                self.FileDetials_show=True
                Test_details.grid_forget()
                NoteboxPanel.forget(Test_details)
                Filedetails_Var.set(0)
        except:
            pass
    # show file details
    def File_Details_Func(self,*args):
        if self.FileURL!="":
            Test_details.config(text=f"""File Name = {self.FileName}\nFile Location = {self.FileURL}\nFile Extension = {self.FileExtension}\nFile Size = {os.path.getsize(self.FileURL)} bytes\nFile Created = {time.strftime('%d-%m-%Y %I:%M %p', time.localtime(os.path.getctime(self.FileURL)))}\nLast Accesed = {time.strftime('%d-%m-%Y %I:%M %p', time.localtime(os.path.getatime(self.FileURL)))}\nLast Modified = {time.strftime('%d-%m-%Y %I:%M %p', time.localtime(os.path.getmtime(self.FileURL)))}""")
        else:
            Test_details.config(text="No File")
        pass
    pass
try:
    App=MultiEditor()
    root=Tk()
    root.title(App.title)
    root.state("zoomed")
    root.rowconfigure(0,weight=1)
    root.columnconfigure(1,weight=1)
    root.protocol("WM_DELETE_WINDOW",App.Ask_Save_File)
    try:
        root.wm_iconbitmap(App.WinIcon)
    except:
        pass
    # styles
    s=ttk.Style()
    s.element_create("Horizontal.TScrollbar","from","clam")
    s.element_create("Horizontal.TScrollbar.trough","from","clam")
    s.element_create("Horizontal.TScrollbar.leftarrow","from","clam")
    s.element_create("Horizontal.TScrollbar.rightarrow","from","clam")
    s.element_create("Horizontal.TScrollbar.thumb","from","clam")
    s.layout("Horizontal.TScrollbar",[('Horizontal.TScrollbar.trough', 
    {'sticky': 'we', 'children': [('Horizontal.TScrollbar.leftarrow', 
    {'side': 'left', 'sticky': ''}), ('Horizontal.TScrollbar.rightarrow', 
    {'side': 'right', 'sticky': ''}), ('Horizontal.TScrollbar.thumb', 
    {'sticky': 'nswe', 'unit': '1', 'children': 
    [('Horizontal.TScrollbar.grip', {'sticky': ''})]})]})])
    s.configure("Horizontal.TScrollbar", gripcount=0, background="#a0a0a0",troughcolor='#444444', borderwidth=0,bordercolor='#252526', lightcolor='#444444', darkcolor='#444444',arrowsize=12)
    # Vertical scrollbar
    s.element_create("Vertical.TScrollbar","from","clam")
    s.element_create("Vertical.TScrollbar.trough","from","clam")
    s.element_create("Vertical.TScrollbar.uparrow","from","clam")
    s.element_create("Vertical.TScrollbar.downarrow","from","clam")
    s.element_create("Vertical.TScrollbar.thumb","from","clam")
    s.layout("Vertical.TScrollbar",[('Vertical.TScrollbar.trough', 
    {'sticky': 'ns', 'children': [('Vertical.TScrollbar.uparrow', 
    {'side': 'top', 'sticky': ''}), ('Vertical.TScrollbar.downarrow', 
    {'side': 'bottom', 'sticky': ''}), ('Vertical.TScrollbar.thumb', 
    {'sticky': 'nswe', 'unit': '1', 'children': [('Vertical.TScrollbar.grip', 
    {'sticky': ''})]})]})])
    s.configure("Vertical.TScrollbar", gripcount=0, background="#a0a0a0",troughcolor='#444444', borderwidth=0,bordercolor='#252526', lightcolor='#444444', darkcolor='#444444',arrowsize=12)
    # notebook
    s.element_create("TNotebook","from","default")
    s.element_create("TNotebook.tab","from","alt")
    s.element_create("TNotebook.padding","from","default")
    s.element_create("TNotebook.focus","from","clam")
    s.element_create("TNotebook.label","from","default")
    s.layout("TNotebook",[('Notebook.client', {'sticky': 'nswe'})])
    s.layout("TNotebook.Tab",[('TNotebook.tab', {'sticky': 'nswe', 'children': 
    [('TNotebook.padding', {'side': 'top', 'sticky': 'nswe', 'children': 
    [('TNotebook.focus', {'side': 'top', 'sticky': 'nswe', 'children': 
    [('TNotebook.label', {'side': 'top', 'sticky': ''})]})]})]})])
    s.configure("TNotebook",background="#444444",highlightthickness=0,padding=(0,0,0,0),margin=(0,0,0,0),tabmargins=1)
    s.configure("TNotebook.Tab",font=("Carlito",11),background="#252526",foreground="white",borderwidth=1,shiftrelief=SOLID,relief=SOLID,padding=0,highlightthickness=0,margin=0)
    # status bar
    Status_Frame=Frame(root)
    for i in range(1):
        Status_Frame.columnconfigure(i,weight=1)
    StatusBar=Label(Status_Frame,text="Status",bg="#444444",fg="white",anchor="w")
    StatusBar.grid(row=0,column=0,columnspan=1,padx=0,pady=0,sticky="nswe")

    Close_Button=Button(Status_Frame,text="Close Tab",bg="#252526",fg="white",borderwidth=2,relief=SOLID,cursor="hand2",command=App.Remove_Tab)
    Close_Button.grid(row=0,column=1,pady=0,padx=0,sticky="nswe")
    Status_Frame.grid(row=2,column=0,columnspan=3,sticky="nswe")
    # toolbar
    ToolBar=Frame(root,bg="#444444")
    # file
    FileButton=Menubutton(ToolBar,text="File",bg="#444444",fg="white",activebackground="#646464",activeforeground="white",cursor="hand2")
    # filemenu
    filemenu=Menu(FileButton,tearoff=0,bg="#252526",fg="white",activeborderwidth=4,font=("Microsoft Sans Serif",10,"bold"),activebackground="#a0a0a0",activeforeground="black",borderwidth=0)
    filemenu.add_command(label="New",accelerator="Ctrl+N",command=App.New_File)
    filemenu.add_command(label="Open",accelerator="Ctrl+O",command=App.Open_File)
    filemenu.add_command(label="Save",accelerator="Ctrl+S",command=App.Save_File)
    filemenu.add_command(label="Save As",accelerator="Shift+Ctrl+S",command=App.SaveAs_File)
    filemenu.add_separator()
    filemenu.add_command(label="Open Folder",command=App.Open_Folder_Func)
    filemenu.add_command(label="Close Folder",command=App.Close_Folder_Func)
    filemenu.add_separator()
    filemenu.add_command(label="Close Current Tab",command=App.Remove_Tab,accelerator="Ctrl+W")
    filemenu.add_command(label="Close All Tab",command=App.Remove_AllTabs,accelerator="Ctrl+Shift+W")
    filemenu.add_separator()
    filemenu.add_command(label="Exit",accelerator="Alt+F4",command=App.Ask_Save_File)
    FileButton.config(menu=filemenu)
    FileButton.grid(row=0,column=0,padx=2,pady=2,sticky="nswe")
    # Edit
    EditButton=Menubutton(ToolBar,text="Edit",bg="#444444",fg="white",activebackground="#646464",activeforeground="white",cursor="hand2")
    # editmenu
    editmenu=Menu(EditButton,tearoff=0,bg="#252526",fg="white",activeborderwidth=4,font=("Microsoft Sans Serif",10,"bold"),activebackground="#a0a0a0",activeforeground="black")
    editmenu.add_command(label="Undo",command=App.Undos,accelerator="Ctrl+Z")
    editmenu.add_command(label="Redo",command=App.Redos)
    editmenu.add_separator()
    editmenu.add_command(label="Cut",command=App.Cuts,accelerator="Ctrl+X")
    editmenu.add_command(label="Copy",command=App.Copys,accelerator="Ctrl+C")
    editmenu.add_command(label="Paste",command=App.Pastes,accelerator="Ctrl+V")
    editmenu.add_separator()
    editmenu.add_command(label="Select All",command=App.SelectAll,accelerator="Ctrl+A")
    editmenu.add_command(label="Clear All",command=App.ClearAll)
    editmenu.add_command(label="Date and Time",command=App.Dateandtime_Func,accelerator="F5")
    editmenu.add_command(label="Copy Path",command=App.CopyPaths)
    editmenu.add_command(label="Reset",command=App.ResetAll_Func)
    editmenu.add_command(label="Format",command=App.Proper_Format)
    editmenu.add_separator()
    editmenu.add_command(label="Find/Replace",command=App.Open_Find_Replace_Win_Func)
    editmenu.add_command(label="Font...",command=App.Font_Win_Func)
    EditButton.config(menu=editmenu)
    EditButton.grid(row=1,column=0,padx=2,pady=2,sticky="nswe")
    # View
    ViewButton=Menubutton(ToolBar,text="View",bg="#444444",fg="white",activebackground="#646464",activeforeground="white",cursor="hand2")
    # viewmenu
    viewmenu=Menu(ViewButton,tearoff=0,bg="#252526",fg="white",activeborderwidth=4,font=("Microsoft Sans Serif",10,"bold"),activebackground="#a0a0a0",activeforeground="black",selectcolor=App.Option_check_color)
    viewmenu.add_command(label="Word wrap",command=App.WordWrap_Func)
    Status_Var=IntVar()
    Folder_Var=IntVar()
    Tool_var=IntVar()
    Scroll_var=IntVar()
    FullScreen_Var=IntVar()
    Filedetails_Var=IntVar()
    # folder side
    viewmenu.add_separator()
    folder_side_menu=Menu(ViewButton,tearoff=0,bg="#252526",fg="white",activeborderwidth=4,font=("Microsoft Sans Serif",10,"bold"),activebackground="#a0a0a0",activeforeground="black",selectcolor=App.Option_check_color)
    folder_side=IntVar()
    folder_side_menu.add_radiobutton(label="Left Side",variable=folder_side,value=0,command=App.Show_Folder_Left_func)
    folder_side_menu.add_radiobutton(label="Right Side",variable=folder_side,value=1,command=App.Show_Folder_Right_func)
    folder_side.set(0)
    viewmenu.add_cascade(menu=folder_side_menu,label="Folder Side")
    viewmenu.add_separator()
    viewmenu.add_checkbutton(label="Show Folder",variable=Folder_Var,onvalue=1,offvalue=0,command=App.Show_Folder_Func)
    viewmenu.add_checkbutton(label="Show Statusbar",variable=Status_Var,onvalue=1,offvalue=0,command=App.Show_Status_Func)
    viewmenu.add_checkbutton(label="Show Toolbar",variable=Tool_var,onvalue=1,offvalue=0,command=App.Show_ToolBar_Func)
    viewmenu.add_checkbutton(label="Show Scrollbars",variable=Scroll_var,onvalue=1,offvalue=0,command=App.Show_Scrollbars_Func)
    viewmenu.add_checkbutton(label="Full Screen",variable=FullScreen_Var,onvalue=1,offvalue=0,command=App.FullScreen_Func,accelerator="F11")
    viewmenu.add_checkbutton(label="Show File Details",variable=Filedetails_Var,onvalue=1,offvalue=0,command=App.File_Description_Func,accelerator="Alt+B")
    Status_Var.set(1)
    Folder_Var.set(1)
    Tool_var.set(1)
    Scroll_var.set(1)
    Filedetails_Var.set(0)
    viewmenu.add_separator()
    # themes
    Theme_value=IntVar()
    themeMenu=Menu(ViewButton,tearoff=0,bg="#252526",fg="white",activeborderwidth=4,font=("Microsoft Sans Serif",10,"bold"),activebackground="#a0a0a0",activeforeground="black",selectcolor=App.Option_check_color)
    themeMenu.add_radiobutton(label="Default",variable=Theme_value,value=0,command=App.Theme_Func)
    themeMenu.add_separator()
    themeMenu.add_radiobutton(label="dark",variable=Theme_value,value=1,command=App.Theme_Func)
    themeMenu.add_radiobutton(label="Monokai",variable=Theme_value,value=2,command=App.Theme_Func)
    themeMenu.add_radiobutton(label="Red",variable=Theme_value,value=3,command=App.Theme_Func)
    themeMenu.add_radiobutton(label="Blue",variable=Theme_value,value=4,command=App.Theme_Func)
    themeMenu.add_radiobutton(label="Lime",variable=Theme_value,value=5,command=App.Theme_Func)
    themeMenu.add_radiobutton(label="white",variable=Theme_value,value=6,command=App.Theme_Func)
    themeMenu.add_radiobutton(label="Purple",variable=Theme_value,value=7,command=App.Theme_Func)
    Theme_value.set(0)
    viewmenu.add_cascade(menu=themeMenu,label="Themes")
    ViewButton.config(menu=viewmenu)
    ViewButton.grid(row=2,column=0,padx=2,pady=2,sticky="nswe")
    
    # help
    HelpButton=Menubutton(ToolBar,text="Help",bg="#444444",fg="white",activebackground="#646464",activeforeground="white",cursor="hand2")
    helpMenu=Menu(HelpButton,tearoff=0,bg="#252526",fg="white",activeborderwidth=4,font=("Microsoft Sans Serif",10,"bold"),activebackground="#a0a0a0",activeforeground="black",selectcolor=App.Option_check_color)
    helpMenu.add_command(label="About",command=App.about)
    helpMenu.add_command(label="Keyboard Shortcut",command=App.shortcutKeys)
    HelpButton.config(menu=helpMenu)
    HelpButton.grid(row=4,column=0,pady=2,padx=2,sticky="nswe")
    ToolBar.grid(row=0,column=0,rowspan=2,sticky="nswe")
    # panel window
    Panels=PanedWindow(root,orient=HORIZONTAL,borderwidth=0,bg="#444444",handlesize=0,handlepad=0)
    # folder frame
    FolderFrame=Frame(Panels,bg="#252526")
    # folder name
    Folder_name=Label(FolderFrame,text="Open Folder",bg="#252526",fg="white",font=("arial",9,"bold"),anchor="w")
    Folder_name.pack(fill=X)
    # show Saved or Not
    Saved_Label=Label(FolderFrame,text="",borderwidth=1,relief=SOLID,bg="#a0a0a0",fg="black",font=("arial",9))
    Saved_Label.pack(fill=X,side=BOTTOM,pady=2,padx=2)
    # add file
    back_Folder=Button(FolderFrame,text="Go back Folder",borderwidth=1,relief=SOLID,bg="#a0a0a0",fg="black",font=("arial",9),cursor="hand2",command=App.Go_Back_Folder_Func)
    back_Folder.pack(fill=X,side=BOTTOM,pady=2,padx=2)
    # add file
    Add_File=Button(FolderFrame,text="Add File",borderwidth=1,relief=SOLID,bg="#a0a0a0",fg="black",font=("arial",9),cursor="hand2",command=App.Add_File_Win_Func)
    Add_File.pack(fill=X,side=BOTTOM,pady=2,padx=2)
    # file list
    File_List=Listbox(FolderFrame,font=("Franklin Gothic",13,"bold"),borderwidth=0,highlightthickness=0,activestyle="none",selectbackground="#a0a0a0",selectforeground="black")
    File_List.pack(fill=BOTH,expand=True,padx=2,pady=2)
    FolderFrame.grid(row=0,column=0,sticky="nswe")
    # notebox panel
    NoteboxPanel=PanedWindow(Panels,orient=VERTICAL,borderwidth=0,handlesize=0,handlepad=1,sashwidth=2,width=10,bg="black")
    # notebook
    NoteBox=ttk.Notebook(NoteboxPanel,style="TNotebook",padding=0)
    f1=Frame(NoteBox)
    t1=Text(f1,font=(App.Font_Face,App.Font_Size),borderwidth=1,relief=SOLID,undo=True,xscrollcommand=None,yscrollcommand=None,tabs=App.Tabs_Space)
    t1.pack(fill=BOTH,expand=True)
    t1.focus()
    Label(f1,text="LB",bg="yellow").pack_forget()
    Button(f1,text="saved").pack_forget()
    f1.pack(fill=BOTH,expand=True,padx=0,pady=0)

    NoteBox.add(f1,text=App.Tab_name,padding=(-1, -1, -3, -3))
    NoteBox.grid(row=0,column=1,sticky="nswe",padx=0,pady=0)

    Test_details=Label(NoteboxPanel,font=("arial",12),bg="#444444",fg="white",anchor="nw",justify=LEFT)
    Test_details.grid_forget()

    NoteboxPanel.add(NoteBox)
    NoteboxPanel.grid(row=0,column=1,sticky="nswe",padx=0,pady=0)
    Panels.add(FolderFrame)
    Panels.add(NoteboxPanel)
    Panels.grid(row=0,column=1,sticky="nswe",padx=0,pady=0)
    # Horizontal scroll
    HorizontalScroll=ttk.Scrollbar(root,orient=HORIZONTAL,cursor="hand2")
    HorizontalScroll.grid(row=1,column=1,sticky="nswe")
    # Vertical scroll
    VerticalScroll=ttk.Scrollbar(root,cursor="hand2")
    VerticalScroll.grid(row=0,column=2,rowspan=2,sticky="nswe")
    # file show
    File_Show_button=Button(root,text="Show Toolbar",command=App.Show_ToolBar_Func,borderwidth=0,cursor="hand2",bg="#646464",fg="white")
    File_Show_button.grid_forget()

    root.bind("<Control-n>",App.New_File)
    root.bind("<Control-o>",App.Open_File_Key_Bind)
    root.bind("<Control-s>",App.Save_File)
    root.bind("<Control-S>",App.SaveAs_File)
    root.bind("<Control-w>",App.Remove_Tab)
    root.bind("<Control-W>",App.Remove_AllTabs)
    root.bind("<F2>",App.Dublicate_line)
    root.bind("<F3>",App.Dublicate_noline)
    root.bind("<F5>",App.Dateandtime_Func)
    root.bind("<F11>",App.FullScreen_Func)
    NoteBox.bind("<<NotebookTabChanged>>",App.Change_Tabs_Func)
    File_List.bind("<<ListboxSelect>>",App.OpenFile_Folder_Func)
    root.bind("<Shift MouseWheel>",App.Zooming)
    root.bind("<Control MouseWheel>",App.Zooming_img)
    root.bind("<Alt MouseWheel>",App.Rotate_img)
    root.bind("<Alt b>",App.File_Description_Func)
    App.Status_Data_func()
    root.bind("<ButtonRelease-1>",App.Close_RightWin_Func)
    root.bind("<Control-t>",App.Focus_Tabs)
    root.mainloop()
except:
    pass