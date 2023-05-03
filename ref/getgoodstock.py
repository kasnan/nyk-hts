import win32com.client

# 업종별 코드와 업종명을 출력
instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

# 패러미터에 업종코드를 전달하면 해당 업종의 종목의 코드를 반환
industryCodeList = instCpCodeMgr.GetIndustryList()

for industryCode in industryCodeList:
    print(industryCode, instCpCodeMgr.GetIndustryName(industryCode))

tarketCodeList = instCpCodeMgr.GetGroupCodeList(5)

for code in tarketCodeList:
    print(code, instCpCodeMgr.CodeToName(code))

instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")
# Get PER
instMarketEye.SetInputValue(0, 67)
instMarketEye.SetInputValue(1, tarketCodeList)
# BlockRequest 
instMarketEye.BlockRequest()

# GetHeaderValue
numStock = instMarketEye.GetHeaderValue(2)
# GetData
sumPer = 0
for i in range(numStock):
    sumPer += instMarketEye.GetDataValue(0, i)

print("Average PER: ", sumPer / numStock)