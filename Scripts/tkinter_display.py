import customtkinter
import CTkTable

class Table:
    def __init__(self,root,rows: int,cols: int, col_names: list):
        self.entries = []
        self.root=root
        self.rows=rows
        self.columns=cols
        self.table=CTkTable.CTkTable(master=root,row=rows,column=cols,values=[col_names])
        
    def update_rows(self,row,array: list):
        col=self.columns
        for i in range (col):
            self.update(row,i,array[i])

    def update(self,row,col=0,text:str= ''):
        self.table.insert(row=row,column=col,value=text)   # insert new text
        
            

if __name__=='__main__':
    root = customtkinter.CTk()

    rows = 7
    columns = 8
    col_names=['  RANK  ','  ID  ','  LAP 1  ','  LAP 2  ','  LAP 3  ','  LAP 4  ','  LAP 5  ','  LAP 6  ']

    t = Table(root,rows,columns,col_names)
    t.table.grid(row=0,column=0)
    t.update(1,4,'Hello')

    root.mainloop()













    ## created by Rupayan Mandal ##