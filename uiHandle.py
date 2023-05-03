import tkinter as tk
from tkinter import ttk
from ttkwidgets import checkboxtreeview as checktree

# import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from pkHandle import  *
from stockHandle import *

class MainWindow:
    def __init__(self):
        # create the main window
        self.root = tk.Tk()
        self.root.geometry("1200x600")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Insert some items into the treeview with price values
        self.added_items = load_txt()
        self.kospistock, self.kosdaqstock = getStockList()

        self.keepupdate = True
        self.checkbox_var = tk.BooleanVar()

    def exit_fullscreen(self,event):
        self.root.attributes("-fullscreen", False)

    def setcomponents(self):
        # create a frame for the first section
        self.frame1 = tk.Frame(self.root, height=200, width=400)
        self.frame1.grid(row=0,column=0)

        self.scrollbar_kospi = tk.Scrollbar(self.frame1)
        self.scrollbar_kospi.pack(side="left",fill="y")
        self.kospitree = ttk.Treeview(self.frame1)
        self.kospitree.pack()

        self.scrollbar_kospi.config(command=self.kospitree.yview)

        self.frame2 = tk.Frame(self.root, height=200, width=400)
        self.frame2.grid(row=1,column=0)

        scrollbar_kosdaq = tk.Scrollbar(self.frame2)
        scrollbar_kosdaq.pack(side="left",fill="y")
        self.kosdaqtree = ttk.Treeview(self.frame2)
        self.kosdaqtree.pack()

        scrollbar_kosdaq.config(command=self.kosdaqtree.yview)

        # create a frame for the second section
        frame3 = tk.Frame(self.root, height=200, width=400)
        frame3.grid(row=0,column=1)

        self.tree = checktree.CheckboxTreeview(frame3, columns=("price",))
        # Add columns to the treeview
        self.tree.heading('#0', text='Item')
        self.tree.heading('#1', text='Price')
        self.tree.pack(fill='both', expand=True)

        # Set up checkboxes for each item
        for item in self.tree.get_children():
            self.tree.item(item, tags=('unchecked',))
            self.tree.tag_bind('unchecked', '<Button-1>', lambda event: self.tree.item(event.tags[-1], tags=('checked',)))
            self.tree.tag_bind('checked', '<Button-1>', lambda event: self.tree.item(event.tags[-1], tags=('unchecked',)))

        # Create a button to remove checked items
        remove_button = tk.Button(frame3, text='Remove Checked Items', command=lambda: self.remove_checked_items(self.tree))
        remove_button.pack(pady=10)

        # trade_button = tk.Button(frame3, text='Issue Trade Request', command=lambda: self.issue_trade(self.tree))
        # trade_button.pack(pady=10)

        refresh_button = tk.Button(frame3, text='Refresh Market Prices',command=self.update_button_clicked)
        refresh_button.pack(pady=10)

        tradelist_button = tk.Button(frame3, text='Get Sent Requests',command=self.get_trade_list)
        tradelist_button.pack(pady=10)

        scan_button = tk.Button(frame3, text='Scan Stock',command=lambda: self.scanStock(self.tree))
        scan_button.pack(pady=10)

        self.tree.bind("<Double-1>", lambda event: self.issue_trade(self.tree))
        self.kospitree.bind("<Double-1>", lambda event: self.on_double_click(event,self.kospitree))
        self.kosdaqtree.bind("<Double-1>", lambda event: self.on_double_click(event,self.kosdaqtree))

        self.setSavedStocks()
        self.setStockList()

        self.update_tree()
    
    def setSavedStocks(self):
        for i in self.added_items:
            price = getPrice(i)
            self.tree.insert('', 'end', text=i, values=price)

    def setStockList(self):
        for i in self.kospistock:
            self.kospitree.insert('', 'end', text=f"{i}")

        for i in self.kosdaqstock:
            self.kosdaqtree.insert('', 'end', text=f"{i}")

    def on_double_click(self, event,treeview):
        item = treeview.selection()[0]
        item_text = treeview.item(item, "text")
        self.added_items = load_txt()
        if item_text in self.added_items:
            return
        add_to_txt(item_text)
        self.added_items.append(item_text)
        print("after addition",self.added_items)
    
        price = getPrice(item_text)
        self.tree.insert('', 'end', text=item_text, values=price)

    def remove_checked_items(self,treeview):
        checked_items = treeview.get_checked()
        checked_text = []
        added_items = load_txt()
        for item in checked_items:
            item_text = treeview.item(item, 'text')
            checked_text.append(item_text)
            treeview.delete(item)
        print('Removed items:', checked_text)
        for i in checked_text:
            added_items.remove(i)
            print(added_items)
        update(added_items)

    def issue_trade(self, treeview):
        selected_item = treeview.focus()  # 선택된 아이템 가져오기
        selected_text = treeview.item(selected_item, "text")  # 선택된 아이템의 텍스트 가져오기
    
        self.keepupdate = False

        tdwin = TradeWindow()
        tdwin.setcomponents(selected_text)

        # infowin = InfoWindow()
        # infowin.setcomponents(selected_text)

    def update_button_clicked(self):
        self.keepupdate = not(self.keepupdate)
        self.update_tree()

    def update_tree(self): # update button을 눌렀을 시 새로운 가격을 받아오는 것
        pricelist = update_pricelist(self.tree)
        self.added_items = load_txt()
        print("get updated prices")
        for i in range(len(pricelist)):
            price = pricelist[i]
            name = self.added_items[i]
            self.tree.insert('', 'end', text=name, values=price)
        if self.keepupdate:
            self.root.after(15000, lambda: self.update_tree())

    def scanStock(self, treeview):
        checked_items = treeview.get_checked()
        checked_text = []

        for item in checked_items:
            item_text = treeview.item(item, 'text')
            checked_text.append(item_text)

        for i in checked_text:
            infowin = InfoWindow()
            infowin.setcomponents(i)
        
    def get_trade_list(self):
        getTradelist()

class TradeWindow:
    def __init__(self):
        # create the main window
        self.root = tk.Toplevel()
        self.root.title("거래창") # 창 제목 설정
        self.root.geometry("300x200") # 창 크기 설정

        self.checkbox_var = tk.BooleanVar()

    def setcomponents(self, item):
        self.item=item
        self.label = tk.Label(self.root, text=item) # 새로운 창에 텍스트 레이블 추가
        self.label.pack(pady=20) # 텍스트 레이블 패킹

        self.frame1 = tk.Frame(self.root, height=200, width=400)
        self.frame1.pack()

        amountLabel = tk.Label(self.frame1, text="수량 : ")
        amountLabel.grid(row=0,column=0)

        self.amountEntry = tk.Entry(self.frame1) # 입력 필드 생성
        self.amountEntry.grid(row=0,column=1)

        self.frame2 = tk.Frame(self.root, height=200, width=400)
        self.frame2.pack()

        priceLabel = tk.Label(self.frame2, text="가격 : ")
        priceLabel.grid(row=0,column=0)

        self.priceEntry = tk.Entry(self.frame2)
        self.priceEntry.delete(0, tk.END)  # Entry 위젯의 텍스트 삭제
        self.priceEntry.insert(0, str(getPrice(item)))  # 새로운 텍스트 삽입
        self.priceEntry.grid(row=0,column=1)
        
        bnsCheck =  tk.Checkbutton(self.root, text="Buy or Sell?", variable=self.checkbox_var)
        bnsCheck.pack()

        orderButton = tk.Button(self.root, text='Order Stock', command=lambda: self.IssueTrade())
        orderButton.pack()

    def IssueTrade(self):
        amount = self.amountEntry.get() # 입력된 텍스트 가져오기
        price = self.priceEntry.get() # 입력된 텍스트 가져오기

        # 원하는 종목을 원하는 수량으로 원하는 가격으로 주문요청
        rqStatus,rqRet,orderNum,tradetyp,code= tradeInit(self.checkbox_var.get(), self.item,amount,price)
        
        if not rqStatus == 0:
            print("request failed")
            self.label.config(text="요청 실패")
            print(orderNum,"주문 요청 실패")
        else:
            print("request complete")
            self.label.config(text="요청 성공")
            time.sleep(4)
            if getTradelist():
                print("거래 성공")
            
        time.sleep(2)
        self.root.destroy()

class InfoWindow:
    def __init__(self):
        # create the main window
        self.root = tk.Toplevel()
        self.root.title("정보창") # 창 제목 설정
        self.root.geometry("800x500") # 창 크기 설정

    def setcomponents(self, item):
        stock_info = get_stock_info(item)

        dates, closes = chart_info_stock(stock_info)
        # 차트 생성
        plt.rcParams['font.family'] = 'Malgun Gothic'
        self.fig, self.ax = plt.subplots()

        self.fig.set_size_inches(5,5)
        self.ax.set_title(stock_info["name"])
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Price (KRW)")
        

        low = [stock_info["low"]] * len(dates)
        high = [stock_info["high"]] * len(dates)

        self.ax.plot(dates, closes, color="blue")
        self.ax.plot(dates,low,'r--')
        self.ax.plot(dates,high,'r--')
        
        self.ax.tick_params(axis="x", rotation=90)

        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.canvas.mpl_connect("button_press_event", self.on_double_click_onchart)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,column=0)

        self.frame1 = tk.Frame(master=self.root)
        self.frame1.grid(row=0,column=1)
    
    def on_double_click_onchart(self, event):
        if event.xdata and event.ydata:
            self.ax.format_coord = lambda x, y: f"x={x}, y={y}" # 좌표 표시
            self.fig.canvas.draw_idle() # 그래프 업데이트

    
        





        
