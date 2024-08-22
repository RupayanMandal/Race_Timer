import customtkinter
class toggle_button():
        def __init__(self,
                     master_frame,
                     display_frame=None,
                     display_texts: list=['OPTION 1','OPTION 2'],
                     default: str='OPTION 1',
                     event_list: tuple=((None,)),
                     resize=False):
            self.button_list=[]
            self.display_texts=display_texts
            self.display_frame=display_frame
            self.evet_list=event_list
            self.master=master_frame
            if resize:
                self.master.rowconfigure(0,weight=1)
                if display_texts==1:
                    self.master.columnconfigure(0,weight=1)
                else:
                    self.master.columnconfigure(list(range(len(display_texts))),weight=1)
            for i in range(len(self.display_texts)):
                self.button_list.append(customtkinter.CTkButton(master=self.master,
                                                    text=self.display_texts[i],
                                                    anchor='center',
                                                    text_color='white',
                                                    fg_color='black',
                                                    text_color_disabled='white',         
                                                    corner_radius=10,
                                                    hover=True, 
                                                    command=lambda c=i: self.click_function(self.button_list[c].cget("text"))))
                self.button_list[i].grid(row=0,column=i,sticky='ew',padx=5)
                
            if default in display_texts:
                text=default
                self.selected=self.display_texts.index(default)
            else:
                text=self.display_texts[0]
                self.selected=0
            #self.button_list[self.selected].configure(fg_color='blue',state='disabled')
            #self.selected_text=self.display_texts[self.selected] 
            self.click_function(text)

        def click_function(self,i):
            self.button_list[self.selected].configure(fg_color='black',state='normal')                   
            self.selected=self.display_texts.index(i)
            self.button_list[self.selected].configure(fg_color='blue',state='disabled')
            self.selected_text=i
            try:
                self.clear_frame(self.display_frame)
                (event,*args)=self.evet_list[self.selected]
                event(*args)
            except:
                pass        
        
        def clear_frame(self,frame):
            for widget in frame.winfo_children():
                widget.destroy()

if __name__=="__main__":
     app=customtkinter.CTk()
     t=toggle_button(app,["A","B","C"],"C",event_list=((sum,[1,2]),))
     app.mainloop()