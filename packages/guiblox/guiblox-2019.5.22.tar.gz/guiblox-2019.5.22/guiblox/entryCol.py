import tkinter      as tk
from guiblox        import theme
import sys

class entryCol:
    def __init__(self, master, names):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.config(bg=master.clr['appBg'])
        for i,key in enumerate(names):
            setattr(self, f'label{i}', tk.Label(self.frame,width=15, bg=master.clr['appBg'], fg=master.clr['appFg'], text=key))
            getattr(self,f'label{i}').grid(row=i,column=0)
            setattr(self, f'entry{i}', tk.Entry(self.frame,width=15, bg=master.clr['txtBg'], fg=master.clr['txtFg']))
            getattr(self,f'entry{i}').insert(tk.END,names[key])
            getattr(self,f'entry{i}').grid(row=i,column=1)
            getattr(self,'frame').grid_rowconfigure(i, weight=1)
        self.frame.grid(column=1,sticky="nsew")
#        self.frame.grid_columnconfigure(1, weight=1)

    def chg2Enum(self,sName, vals):
        setattr(self, f'{sName}_enum', tk.StringVar(self.frame))
        vEnum = getattr(self, f'{sName}_enum')
        foo = getattr(self, f'{sName}').grid_info()
        getattr(self, f'{sName}').grid_forget()
        getattr(self, f'{sName}').destroy()
        setattr(self, f'{sName}', tk.OptionMenu(self.frame, vEnum, *vals))
        getattr(self, f'{sName}').config(width=8, bg=self.master.clr['appBg'], fg=self.master.clr['appFg'])
        getattr(self, f'{sName}').grid(row=foo['row'], column=foo['column'])

    def save(self):
        outDict = {}
        childList = self.frame.winfo_children()
        for child in childList:
            if type(child) == tk.Entry:
                outDict[child._name] = child.get()
        return outDict

class entryCol1:
    def __init__(self, master, names):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.config(bg=master.clr['appBg'])
        for i,key in enumerate(names):
            if i == 0:
                setattr(self, f'label{i}', tk.Label(self.frame,width=15, bg=master.clr['appBg'], fg=master.clr['appFg'], text=key))
                getattr(self,f'label{i}').grid(row=i,column=0)
            setattr(self, f'entry{i}', tk.Entry(self.frame,width=15, bg=master.clr['txtBg'], fg=master.clr['txtFg']))
            getattr(self,f'entry{i}').insert(tk.END,names[key])
            getattr(self,f'entry{i}').grid(row=i+1,column=0,sticky='ew')
            getattr(self,'frame').grid_rowconfigure(i+1, weight=1)
        self.frame.grid(column=1,sticky="nsew")
#        self.frame.grid_columnconfigure(1, weight=1)

if __name__ == '__main__':
    root = theme.theme().addColor()
    root.geometry(f'{300}x{300}')
    dictIn = {} 
    dictIn['FreqStart']     = '24e9'
    dictIn['FreqStop']      = '39e9'
    
    app = entryCol(root,dictIn)                     #pylint: disable=unused-variable
    app.frame.config(width=100, height=100)
    app.frame.grid(row=0,column=0,sticky="nsew")
    print(app.save())
    root.mainloop()
