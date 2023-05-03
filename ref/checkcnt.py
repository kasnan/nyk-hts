import win32com.client
instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")

if instCpCybos.IsConnect == 0:
    print("error")
    exit()
print(instCpCybos.IsConnect)

# 정상적으로 연결될 시 1을 출력