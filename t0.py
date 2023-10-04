import cv2
#打开图片
img = cv2.imread('question_set/T1.jpeg')

#显示图片
cv2.imshow('Image', img)

#按q推出
while True:
    if cv2.waitKey(1) == ord('q'): #ord将字符转换成整数
        break
