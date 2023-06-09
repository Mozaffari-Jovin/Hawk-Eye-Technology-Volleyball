import cv2 # opencv
import numpy as np

kernel_sharp = np.array([[0, -1, 0],
	[-1, 5, -1],
	[0, -1, 0]])

ball_ys = [] # ball's y-position
in_out = [] # whether inside the court or not

for i in range(1, 6): # for 5 sequential images
	img = cv2.imread(f"media/volleyball/{i}.png") # f-string
	
	# img = cv2.resize(img, None, fx=0.4, fy=0.4)
	img = cv2.resize(img, (975, 485))

	print(img.shape) # (489, 975, 3)
	
	img_show = img.copy()

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	sharp = cv2.filter2D(gray, -1, kernel_sharp) # increase sharpness
	
	circles = cv2.HoughCircles(sharp, cv2.HOUGH_GRADIENT, 1.5, 100, maxRadius=150) # give circle’s parameters
	print(circles)
	# quit()

	if circles is not None:
		circles = circles[0].astype(np.uint32) # change float to integer

		for circle in circles:
			ball_ys.append(circle[1]) # append ball's y-position to ball_ys
			if (circle[0] + circle[2]) < 460: # center (x) + radius (r), where 460 pixel refers to the white line (i.e. the column number 460)
				in_out.append("out")
			else:
				in_out.append("in")
			cv2.circle(img_show, (circle[0], circle[1]), circle[2], (0, 0, 255), 2) # draw a circle
	# cv2.imshow("Frames", img_show[:, 460:])	
	cv2.imshow("Frames", img_show)
	cv2.waitKey(0)

print(ball_ys)
print(in_out)

y_max_index = np.argmax(ball_ys) # select index for max y
print(f"Ball out? {in_out[y_max_index]}")
cv2.destroyAllWindows()