from unittest import TestCase
import uiHandle

import tkinter as tk
from tkinter import ttk
from ttkwidgets import checkboxtreeview as checktree

import stockHandle

class MyTests(TestCase):
    def test1(self):
        tmp = uiHandle.MainWindow()
        self.assertIsInstance(tmp,uiHandle.MainWindow)

    def test2(self):
        tmp = uiHandle.TradeWindow()
        self.assertIsInstance(tmp,uiHandle.TradeWindow)
    
    def test3(self):
        tmp = uiHandle.InfoWindow()
        self.assertIsInstance(tmp,uiHandle.InfoWindow)

    def test4_MainWindow(self):
        tmp = uiHandle.MainWindow()
        self.assertIsInstance(tmp.added_items,list)
    
    def test5_MainWindow(self):
        tmp = uiHandle.MainWindow()
        self.assertIsInstance(tmp.kospistock,list)

    def test6_MainWindow(self):
        tmp = uiHandle.MainWindow()
        self.assertIsInstance(tmp.kosdaqstock,list)
    
    def test7_MainWindow(self):
        tmp = uiHandle.MainWindow()
        self.assertIsInstance(tmp.checkbox_var,tk.BooleanVar)
        
    def test8_MainWindow(self):
        tmp = uiHandle.MainWindow()
        tmp.setcomponents()
        self.assertIsInstance(tmp.tree,checktree.CheckboxTreeview)

    def test9_TradeWindow(self):
        tmp = uiHandle.TradeWindow()
        self.assertIsInstance(tmp.checkbox_var,tk.BooleanVar)

    # stockHandler testcase
    def test1_sH(self):
        tmp = stockHandle.getStockList()
        self.assertIsInstance(tmp,tuple)

    def test2_sH(self):
        tmp = stockHandle.getPrice("KR모터스")
        self.assertNotEqual(tmp,stockHandle.getPrice("삼성전자"))

    
    

        


