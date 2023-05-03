import win32com.client
instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
print(instCpStockCode.GetCount())

# 출력 : 총 종목 수

import win32com.client
instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
print(instCpStockCode.GetData(1, 0))

# 각 인덱스에 해당하는 종목에 대한 데이터를 얻기 위해서는 표 10.1에서 설명한 GetData 메서드를 사용하면 됩니다. GetData 메서드는 두 개의 인자를 받는데, 첫 번째 인자로 0, 1, 2 중 하나의 값을 받습니다. 
# 첫 번째 인자의 값이 0이면 종목 코드를, 1이면 종목명을, 2면 FullCode를 리턴합니다.
# 해당 종목의 이름을 비교해 해당 종목의 코드를 얻어올 수 있다.

# 종목에 대한 조회 및 매수/매도는 종목 코드를 통해 이루어진다.
import win32com.client
instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = instCpCodeMgr.GetStockListByMarket(1)
print(codeList)
# 유가증권 리스트를 가져옴

