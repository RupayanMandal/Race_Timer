

from tkinter import * 

class Table:
    def __init__(self,root,rows: int,cols: int, col_names: list):
        self.entries = []
        self.root=root
        self.rows=rows
        self.columns=cols  
        self.root.rowconfigure(list(range(rows)), weight=1) 
        self.root.columnconfigure(list(range(cols)), weight=1)    
        for i in range(rows):
            row = []  # this will actually contain 1 row of cell entry widgets
            for j in range(cols):
                if i==0:
                    fgcolor='blue'
                    fontstyle=('Arial',16,'bold')
                    mywidth=10
                else:
                    fgcolor='black'    
                    fontstyle=('Arial',8)
                    mywidth=20
                e = Entry(root, width=mywidth, fg='blue',
                               font=fontstyle, disabledforeground=fgcolor,justify='center')
                
                e.grid(row=i, column=j, sticky="nsew")
                if i==0:
                    e.insert(END, col_names[j])
                else:
                    e.insert(END, '')
                e.config(state='disabled')    
                row.append(e)
            self.entries.append(row)
        """ close_btn = Button(text="Close", 
                   command=quit,
                   activebackground="blue", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgray",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=1,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=10,
                   pady=10,
                   width=15,
                   wraplength=100
                   )
        close_btn.grid(row=i+1,column=1,columnspan=self.columns)
 """
                    

    def update_row(self,row,array: list):
        col=self.columns
        for i in range (col):
            self.update(row,i,array[i])

    def update(self,row,col=-1,text:str= ''):
        e = self.entries[row][col]
        e.config(state='normal')
        val = e.get()            #  Get the current text in cell
        e.delete(0,last=len(val))  # remove current text
        e.insert(END, text)   # insert new text
        e.config(state='disabled')

            

if __name__=='__main__':
    root = Tk()

    rows = 7
    columns = 8
    col_names=['  RANK  ','  ID  ','  LAP 1  ','  LAP 2  ','  LAP 3  ','  LAP 4  ','  LAP 5  ','  LAP 6  ']

    t = Table(root,rows,columns,col_names)
    t.update(1,4,'Hello')

    mainloop()










    ## created by Rupayan Mandal ##