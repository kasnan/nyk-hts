import win32com.client

from pkHandle import *

import time
# multithreading으로 각 종목을 검색해서 가격 받아오기

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")
instCpTd6033 = win32com.client.Dispatch("CpTrade.CpTd6033")

def update_pricelist(tree):
    pricelist = []
    added_items = load_txt()
    for row in tree.get_children():
        tree.delete(row)

    for i in added_items:
        price = getPrice(i)
        # tree.insert('', 'end', text=i, values=price)
        pricelist.append(price)

    # print("after update test")
    return pricelist

def getStockList():
    CPE_MARKET_KIND = {'KOSPI':1,  'KOSDAQ':2}
    kospistock = []
    kosdaqstock = []


    for key, value in CPE_MARKET_KIND.items():
        codeList = instCpCodeMgr.GetStockListByMarket(value)
        for code in codeList:
            name = instCpCodeMgr.CodeToName(code)
            sectionKind = instCpCodeMgr.GetStockSectionKind(code)
            if value == 1:
                # print("kospi: ",name)
                kospistock.append(name)
            elif value == 2:
                # print("kosdaq: ",name)
                kosdaqstock.append(name)
    return kospistock, kosdaqstock

def getPrice(item): # item : 주식종목명
    # print(item)

    code = instCpStockCode.NameToCode(item)

    instStockChart.SetInputValue(0, code)
    instStockChart.SetInputValue(1, ord('2'))
    instStockChart.SetInputValue(4, 1)
    instStockChart.SetInputValue(5, 5)
    instStockChart.SetInputValue(6, ord('D'))
    instStockChart.SetInputValue(9, ord('1'))

    instStockChart.BlockRequest()

    return instStockChart.GetDataValue(0, 0)
    
    
# 매도, 매수
# tree에서 체크한 아이템을 거래 누르면 subwindow
# 1. 현재 시장가 2. 원하는 수량 3. 매도(True)/매수(False)
def tradeInit(flag, item, amount, price):
    instCpTdUtil.TradeInit()
    # 이용할 계좌를 호출
    accountNumber = instCpTdUtil.AccountNumber[0]
    code = instCpStockCode.NameToCode(item)
    # 해당 주식을 원하는 가격에 원하는 수량을 판매
    if not flag:
        tradetyp = 1
    # 해당 주식을 원하는 가격에 원하는 수량을 구매
    else:
        tradetyp=2
    instCpTd0311.SetInputValue(0, tradetyp)
    # 주문을 수행할 계좌
    instCpTd0311.SetInputValue(1, accountNumber)
    # 주문할 종목
    instCpTd0311.SetInputValue(3, code)
    # 주문할 수량
    instCpTd0311.SetInputValue(4, amount)
    # 주문 단가
    instCpTd0311.SetInputValue(5, price)
    instCpTd0311.BlockRequest()
    
    # rqStatus : 0=성공
    # rqRet : 94060모의투자 정상처리 되었습니다=성공, 그외는 에러
    rqStatus = instCpTd0311.GetDibStatus()
    rqRet = instCpTd0311.GetDibMsg1()
    orderNum = instCpTd0311.GetHeaderValue(9)
    
    return rqStatus, rqRet, orderNum, tradetyp, code

def checkTrade(orderNum):
    instCpTdUtil.TradeInit()
    accountNumber = instCpTdUtil.AccountNumber[0]
    instCpTd6033.SetInputValue(0, accountNumber)  # 계좌번호
    instCpTd6033.SetInputValue(1, "0")  # 전체
    instCpTd6033.SetInputValue(2, "1")  # 최근순
    instCpTd6033.BlockRequest()

    # 체결 개수 확인
    numOfConcluded = instCpTd6033.GetHeaderValue(7)
    print("체결 개수", numOfConcluded)

    # 체결 정보 출력
    flag = 0
    for j in range(5):
        for i in range(numOfConcluded):
            stockName = instCpTd6033.GetDataValue(12, i)
            orderStatus = instCpTd6033.GetDataValue(14, i)
            orderQty = instCpTd6033.GetDataValue(15,i)

            # 최근 주문 거래 상태 확인
            if orderNum == instCpTd6033.GetDataValue(3, i):
                print("최근 주문 거래 상태:", orderStatus)
                flag =1
                break
        
        if flag==1:
            return True
        else:
            return False

def getTradelist():
    instCpTdUtil.TradeInit()
    accountNumber = instCpTdUtil.AccountNumber[0]
    instCpTd6033.SetInputValue(0, accountNumber)  # 계좌번호
    instCpTd6033.SetInputValue(1, "0")  # 전체
    instCpTd6033.SetInputValue(2, "1")  # 최근순
    instCpTd6033.BlockRequest()

    # 체결 개수 확인
    numOfConcluded = instCpTd6033.GetHeaderValue(7)
    print("체결 개수", numOfConcluded)

    # 체결 정보 출력
    for i in range(numOfConcluded):
        stockName = instCpTd6033.GetDataValue(12, i)
        orderStatus = instCpTd6033.GetDataValue(14, i)
        orderQty = instCpTd6033.GetDataValue(15,i)

        print("종목:",instCpStockCode.CodeToName(stockName),"주문상태:",bool(orderStatus),"주문수량:",orderQty)

def get_stock_info(stock_name):
    # 대신증권 API 객체 생성
    instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
    instCpStock = win32com.client.Dispatch("DsCbo1.StockMst")

    # 주식 코드로부터 종목명 획득
    stock_code = instCpStockCode.NameToCode(stock_name)

    # 주식 정보 요청
    instCpStock.SetInputValue(0, stock_code)
    instCpStock.BlockRequest()

    # 주식 정보 획득
    stock_open = instCpStock.GetHeaderValue(13)  # 시가
    stock_high = instCpStock.GetHeaderValue(14)  # 고가
    stock_low = instCpStock.GetHeaderValue(15)  # 저가
    stock_close = instCpStock.GetHeaderValue(1)  # 종가
    stock_volume = instCpStock.GetHeaderValue(18)  # 거래량

    # 결과 반환
    return {
        "name": stock_name,
        "code": stock_code,
        "open": stock_open,
        "high": stock_high,
        "low": stock_low,
        "close": stock_close,
        "volume": stock_volume
    }

def chart_info_stock(stock_info):
    # API 요청 정보 설정
    instStockChart.SetInputValue(0, stock_info["code"])  # 종목코드
    instStockChart.SetInputValue(1, ord('2'))  # 요청구분 (개수로 요청)
    instStockChart.SetInputValue(4, 20)  # 요청 개수
    instStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])  # 요청항목 (날짜, 시가, 고가, 저가, 종가, 거래량)
    instStockChart.SetInputValue(6, ord('D'))  # 차트 종류 (일간)

    instStockChart.BlockRequest()
    dates = []
    closes = []

    for i in range(instStockChart.GetHeaderValue(3)):
        date = instStockChart.GetDataValue(0, i)
        close = instStockChart.GetDataValue(4, i)

        # datetime 타입으로 변환
        date = f"{date // 100 % 100:02d}-{date % 100:02d}"
        dates.append(date)
        closes.append(close)
    
    dates.reverse()
    closes.reverse()

    return dates,closes