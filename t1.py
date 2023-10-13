import cv2

# 读取图片
image = cv2.imread('question_set/T1.jpeg')

# 将图像转换为灰度
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 二值化处理
_, binary_img = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

# #显示二值化图像
# cv2.imshow('Binary', binary_img)
# cv2.waitKey(0)

# 寻找轮廓
contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print("星星数量：",len(contours))

image_center = image.copy()
image_num = image.copy()


#找出每个轮廓的重心 并标号
for i in range(len(contours)):
    M = cv2.moments(contours[i])
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.drawMarker(image_center, (cx, cy), (0, 0, 255), cv2.MARKER_CROSS, 20, 1)
    cv2.putText(image_num, str(i+1), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
    

#显示图片
cv2.imshow('Image', image_center)
cv2.imshow('Image', image_num)
cv2.waitKey(0)
cv2.destroyAllWindows()

