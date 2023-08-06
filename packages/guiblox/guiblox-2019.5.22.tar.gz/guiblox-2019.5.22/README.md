# Object oriented TKINTER WIDGETS

## Project goals

Object oriented GUI library.  Programatically generate common gui items.

## Installation

```python
from guiblox                    import buttonRow, entryCol, theme, listWindow
```
## Getting Started

```python
from guiblox.__main__ import main

main()
```

# Documentation

## Entry Column

```python
from guiblox import entryCol

entryDict = {}                                          # Dict for entry column object
entryDict['Entry1']     = '192.168.1.114'               # Define Label & Default Val
entryDict['Entry2']     = '192.168.1.114'               # Define Label & Default Val
entryDict['Entry3']     = 'spaceHolder'                 # Define Label & Default Val

root = theme().addColor()                               # Create GUI object w/ colors
root.entryCol = entryCol(root, entryDict)               # Create column of entry fields

### Assign Functions/Behavior
root.entryCol.frame.config(width=100)                   # Chg frame width
root.entryCol.chg2Enum('entry2', ['Opt1','Opt2'])       # Chg entry2 to pull down
root.entryCol.entry2_enum.set('Opt1')                   # entry2 default value
```

## Button Row

```python
from guiblox import buttonRow

root = theme().addColor()                               # Create GUI object w/ colors defined.
root.title('GUI Example')

### Create GUI Elements
root.buttnRow = buttonRow(root, 3)                      # pylint: disable=unused-variable

### Assign Functions/Behavior
root.buttnRow.button0.config(text='foo'  ,command=lambda: buttonfunc1(root))
root.buttnRow.button1.config(text='clear',command=lambda: buttonfunc2(root))
root.buttnRow.button2.config(text='baz'  ,command=lambda: buttonfunc3(root))
```

## Output TextBoxes

```python
from guiblox import listWindow

root = theme().addColor()                               # Create GUI object w/ colors
root.title('GUI Example')

### Create GUI Elements
root.TextBox = listWindow(root)                        # Create bottom text box
root.TextBox.stdOut()                                  # Print --> TextBox

### Assign Functions/Behavior
root.TextBox.listWindow.config(height= 5,width=66)
```

listWindow Method       | Description
------------------------|------------------------------------------
listWindow.add_Files    | Opens GUI to add files
listWindow.clear        | Clears listWindow
listWindow.getlist      | returns contents as list
listWindow.getstr       | returns contents as string
listWindow.stdOut       | Redirects Print statements to listWindow
listWindow.writeN       | Prints text to listWindow
listWindow.writeH       | Prints text to listWindow w/ Highlight