import cv2
import numpy as np

# Global variables
mask_path = str()
template_path = str()
drawing = False  # True when mouse is pressed
erase_mode = False  # Toggle between draw and erase mode
ix, iy = -1, -1  # Initial mouse position
mask = None  # To store the mask

# Mouse callback function
def draw_or_erase(event, x, y, flags, param):
    global ix, iy, drawing, mask, erase_mode
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            color = 0 if erase_mode else 255  # Black for erase, white for draw
            cv2.circle(mask, (x, y), 10, color, -1)  # Draw/erase a circle on the mask
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(mask, (x, y), 10, 0 if erase_mode else 255, -1)

# Load template
template = cv2.imread(template_path, cv2.IMREAD_COLOR)
if template is None:
    print("Error loading template.")
    exit()

# Initialize mask
mask = np.zeros(template.shape[:2], dtype=np.uint8)  # Single-channel mask

# Set up the window and callback
cv2.namedWindow("Annotate Template")
cv2.setMouseCallback("Annotate Template", draw_or_erase)

while True:
    # Display the template with mask overlay
    overlay = template.copy()
    overlay[mask == 255] = [0, 0, 255]  # Mark ignored regions in red
    cv2.imshow("Annotate Template", overlay)
    
    # Handle keypresses
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to exit
        break
    elif key == ord('e'):  # Toggle erase mode
        erase_mode = not erase_mode
        print("Erase mode:", "ON" if erase_mode else "OFF")
    elif key == ord('s'):  # Save the mask
        try:
            # Visualize the mask to ensure correctness
            cv2.imshow("Mask Preview", mask)
            cv2.waitKey(1)  # Show for 100ms

            # Save the mask
            cv2.imwrite(mask_path, mask)

            print("Mask saved successfully as 'mask.png'!")
        except Exception as e:
            print(f"Failed to save mask: {e}")

cv2.destroyAllWindows()