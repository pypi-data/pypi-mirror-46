import tkinter  as tk
from guiblox    import theme

import sys

class buttonRow:
    def __init__(self, master, iNum, makequit=1):
        self.master = master
        self.btnWidth = 10
        self.frame = tk.Frame(self.master, bg='black',padx=3, pady=3)
        self.frame.config(bg=master.clr['appBg'])
        for i in range(iNum):
            setattr(self,f'button{i}', tk.Button(self.frame, text=f'Button{i}', width=self.btnWidth, command=self.new_window))
            getattr(self,f'button{i}').config(bg=master.clr['appBg'],fg=master.clr['appFg'])
            getattr(self,f'button{i}').grid(row=0,column=i)
            getattr(self,'frame').grid_columnconfigure(i, weight=1)
        if makequit:   #Quit Button
            setattr(self,f'button{iNum}', tk.Button(self.frame, text=f'Quit', width=self.btnWidth, command=self.GUI_quit))
            getattr(self,f'button{iNum}').config(bg='red2',fg=master.clr['appFg'])
            getattr(self,f'button{iNum}').bind("<Escape>",self.GUI_quit)
            getattr(self,f'button{iNum}').grid(row=0,column=iNum)
            getattr(self,'frame').grid_columnconfigure(iNum, weight=1)
        self.frame.grid(row = 0, sticky = "nsew")

    def GUI_quit(self):
        self.master.quit()
        self.master.destroy()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Popup(self.newWindow)

class Popup:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 15, command = self.close_windows)
        self.quitButton.grid()
        self.frame.grid()
    def close_windows(self):
        self.master.destroy()

if __name__ == '__main__':
    root = theme.theme().addColor()
    app = buttonRow(root,2)                     #pylint: disable=unused-variable
    #app.frame.config(width=300, height=50)
    root.mainloop()
