import cv2

# Load the image
img = cv2.imread("fire.5.png")

# Grid lines at these intervals (in pixels)
# dx and dy can be different
dx, dy = 100,100

# Custom (rgb) grid color
grid_color = [255,0,0]

# Modify the image to include the grid
img[:,::dy,:] = grid_color
img[::dx,:,:] = grid_color

# Show the result
cv2.imshow('img',img)
cv2.waitKey(0)