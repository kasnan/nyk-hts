import win32com.client

# 클래스 호출과 거래 초기화
instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")
instCpTdUtil.TradeInit()

# 매수

# 이용할 계좌를 호출
accountNumber = instCpTdUtil.AccountNumber[0]
# 주문(매수)
instCpTd0311.SetInputValue(0, 2)
# 주문을 수행할 계좌
instCpTd0311.SetInputValue(1, accountNumber)
# 주문할 종목
instCpTd0311.SetInputValue(3, 'A003540')
# 주문할 수량
instCpTd0311.SetInputValue(4, 10)
# 주문 단가
instCpTd0311.SetInputValue(5, 13000)

instCpTd0311.BlockRequest()

# # 매도

# # 이용할 계좌를 호출
# accountNumber = instCpTdUtil.AccountNumber[0]
# # 주문(매도)
# instCpTd0311.SetInputValue(0, 1)
# # 주문을 수행할 계좌
# instCpTd0311.SetInputValue(1, accountNumber)
# # 주문할 종목
# instCpTd0311.SetInputValue(3, 'A003540')
# # 주문할 수량
# instCpTd0311.SetInputValue(4, 10)
# # 주문 단가
# instCpTd0311.SetInputValue(5, 13000)

# instCpTd0311.BlockRequest()