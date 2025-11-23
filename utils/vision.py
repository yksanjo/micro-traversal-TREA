import cv2

def find_element_on_screen(screen_path, template_path, threshold=0.7):
    screen = cv2.imread(screen_path, 0)
    template = cv2.imread(template_path, 0)
    if screen is None or template is None:
        return None
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)
    return None