import win32com.client
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

# 조회할 종목을 코드로 조회, 뒤에는 해당 종목코드
instStockChart.SetInputValue(0, "A003540")
# 조회할 정보를 기간으로 조회, 아스키코드 값으로 변화
instStockChart.SetInputValue(1, ord('2'))
# 요청 개수라는 타입, 실제로 요청할 데이터의 개수
instStockChart.SetInputValue(4, 10)
# 요청할 데이터의 종류(5=종가)
instStockChart.SetInputValue(5, 5)
# 요청할 데이터는 일 단위의 데이터
instStockChart.SetInputValue(6, ord('D'))
# 수정 주가의 반영 여부에 대해서, 수정 주가를 의미하는 인수를 입력
instStockChart.SetInputValue(9, ord('1'))

# 데이터 처리를 요청
instStockChart.BlockRequest()

# Request/reply 방식으로 이루어지므로 reply 코드

# 요청한 데이터의 개수
numData = instStockChart.GetHeaderValue(3)
for i in range(numData):
    print(instStockChart.GetDataValue(0, i))

# 해당 종목의 최근 10일간의 종가