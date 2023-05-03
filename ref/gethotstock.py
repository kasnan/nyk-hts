import win32com.client

# Create object
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

# SetInputValue
instStockChart.SetInputValue(0, "A003540")
instStockChart.SetInputValue(1, ord('2'))
instStockChart.SetInputValue(4, 60)
instStockChart.SetInputValue(5, 8)
instStockChart.SetInputValue(6, ord('D'))
instStockChart.SetInputValue(9, ord('1'))

# BlockRequest
instStockChart.BlockRequest()

# GetData
volumes = []
numData = instStockChart.GetHeaderValue(3)
for i in range(numData):
    volume = instStockChart.GetDataValue(0, i)
    volumes.append(volume)
print(volumes)

averageVolume = (sum(volumes) - volumes[0]) / (len(volumes) -1)
if(volumes[0] > averageVolume * 10):
    print("대박 주")
else:
    print("일반 주", volumes[0] / averageVolume)

# 최근 거래일의 거래량이 평균 거래량의 10배 이상이면 대박주!