###############################################################################
### Rohde & Schwarz SCPI Driver Software Test
###
### Purpose: Import Library-->Create Object-->Catch obvious typos.
###          Tests do not require instrument.
### Author:  mclim
### Date:    2018.06.13
###############################################################################
### Code Start
###############################################################################
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        from guiblox import theme
        self.GUI = theme().addColor()                            #Create GUI object
        print("",end="")
        pass

    def tearDown(self):                             #Run after each test
        pass

###############################################################################
### <Test>
###############################################################################
    def test_common(self):
        pass

    def test_buttonrow(self):
        from guiblox import buttonRow
        self.testObj = buttonRow(self.GUI, 3)

    def test_listWindow(self):
        from guiblox import listWindow
        self.testObj = listWindow(self.GUI)

    def test_entryCol(self):
        from guiblox import entryCol
        entryDict = {} 
        entryDict['Label1'] = 'Value1'
        entryDict['Label2'] = 'Value2'
        self.testObj = entryCol(self.GUI, entryDict)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    if 0:     #Run w/o test names
        unittest.main()
    else:     #Verbose run
        suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
        unittest.TextTestRunner(verbosity=2).run(suite)
