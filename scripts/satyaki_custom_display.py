from customtkinter import *
from CTkTable import *


app = CTk()

app.geometry("1440x900")

""" def button_event():
    print("button pressed")

button = CTkButton(master=app, text="CTkButton", command =button_event)
button.place(relx = 0.5, rely = 0.5, anchor='center') """

""" value = [[1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5],
         [1,2,3,4,5]] """
frame = CTkFrame(master=app, width=1000, height=300)
frame.place(relx = 0.5, rely = 0.7, anchor='center')
table = CTkTable(master=app, row=7, column=5, values=[["Rank", "Name", "Current Lap", "Best Lap Time", "Trailing By"]], height = 30, width = 200)
table.pack(expand=True, fill="both", padx=20, pady=20)
table.place(relx = 0.5, rely = 0.3, anchor='center')

labelOne = CTkLabel(app, text="Current Leader: ", fg_color="transparent", text_color="red")
labelOne.place(x = 100, y = 100)

labelTwo = CTkLabel(app, text="Time Elapsed: ", fg_color="transparent", text_color ="green")
labelTwo.place(x = 1200, y = 100)

labelThree = CTkLabel(app, text="Log: ", fg_color="transparent")
labelThree.place(x = 200, rely = 0.5, anchor="center")

app.mainloop()

