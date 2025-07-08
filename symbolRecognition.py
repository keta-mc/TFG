import cv2

img = cv2.imread("cleaned_score.png", cv2.IMREAD_GRAYSCALE)


# Binarize the image (convert to black and white)
_, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

# Convert the grayscale image to BGR for visualization
img_with_contour = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)

for contour in contours:
    cv2.drawContours(img_with_contour, [contour], -1, (0,255,0), 1)
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img_with_contour, (x,y), (x + w, y + h), (255,0,0), 1)


cv2.imshow('contour', img_with_contour)
cv2.waitKey(0)
cv2.destroyAllWindows()
