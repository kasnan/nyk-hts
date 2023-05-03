import matplotlib.pyplot as plt

# 샘플 데이터 생성
x1 = [1, 2, 3, 4, 5]
y1 = [2, 4, 6, 8, 10]
x2 = [1, 2, 3, 4, 5]
y2 = [3, 6, 9, 12, 15]

# 그래프 그리기
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
ax1.plot(x1, y1)
ax2.plot(x2, y2)

# 특정 값 입력받기
val = float(input("Enter a value: "))

# 입력받은 값에 해당하는 높이 찾기
idx1 = y1.index(val)
height1 = y1[idx1]
idx2 = y2.index(val)
height2 = y2[idx2]

# 선 그리기
ax1.axhline(y=height1, color='r', linestyle='--')
ax2.axhline(y=height2, color='r', linestyle='--')

# 그래프 출력하기
plt.show()
