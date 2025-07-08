import cv2

def cleanAndBinarize(img):
    gray = cv2.imread(f"{img}", cv2.IMREAD_GRAYSCALE)

    blurredG = cv2.GaussianBlur(gray, (3,3), 0)

    _, binary = cv2.threshold(blurredG, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    cv2.imwrite("cleaned_score.png", cleaned)
    cv2.imshow("Cleaned", cleaned)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def staffLineDetectionAndRemoval():

    img = cv2.imread("cleaned_score.png", cv2.IMREAD_GRAYSCALE)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))

    # MORPH_CLOSE with 3 iterations gives the best results of detecting the staff lines
    # since the binary image is with white background, MORPH_BLACKHAT with 3 iterations gives only the musical objetcts
    # detected_lines = cv2.morphologyEx(img, cv2.MORPH_CLOSE, horizontal_kernel, iterations=3) # for THRESH_BINARY
    detected_lines = cv2.morphologyEx(img, cv2.MORPH_OPEN, horizontal_kernel, iterations=4) # for THRESH_BINARY_INV

    inpainted = cv2.inpaint(img, detected_lines, inpaintRadius=0.1, flags=cv2.INPAINT_TELEA)

    cv2.imshow("Inpaint", inpainted)
    cv2.waitKey(0)
    cv2.imwrite("cleaned_score.png", inpainted)
    cv2.destroyAllWindows()
