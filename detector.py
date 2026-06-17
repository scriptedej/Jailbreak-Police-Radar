import pyautogui
import math
import time
import winsound

config = {
    "target_color": [42, 204, 255],
    "tolerance": 20,
    "max_radius": 75,
    "region": [11, 774, 149, 152],
    "middle_screen": [85, 851]
}

print("Jailbreak Police Radar by @ej1334")
print("Loading Setup...")

input("Move your mouse to the center of the minimap and press Enter...")
middle_screen = pyautogui.position()

print(f"Center set to {middle_screen}")

target_color = tuple(config["target_color"])
tolerance = config["tolerance"]
max_radius = config["max_radius"]

input("Move mouse to TOP-LEFT corner and press Enter...")
top_left = pyautogui.position()

input("Move mouse to BOTTOM-RIGHT corner and press Enter...")
bottom_right = pyautogui.position()

region = (
    top_left.x,
    top_left.y,
    bottom_right.x - top_left.x,
    bottom_right.y - top_left.y
)

print("Region:", region)

middle_x = middle_screen[0] - region[0]
middle_y = middle_screen[1] - region[1]

def color_matches(c1, c2, tol):
    return all(abs(a - b) <= tol for a, b in zip(c1[:3], c2))

def find_color_with_radius(screenshot, target, tol):
    best = None
    best_dist = float("inf")
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            pixel = screenshot.getpixel((x, y))
            if color_matches(pixel, target, tol):
                dist = math.hypot(x - middle_x, y - middle_y)
                if dist < best_dist:
                    best_dist = dist
                    best = (x, y, dist)
    return best

def main():
    print("Starting detection loop... (Ctrl+C to stop)")
    last_beep_time = 0.0
    while True:
        screenshot = pyautogui.screenshot(region=region)
        result = find_color_with_radius(screenshot, target_color, tolerance)

        if result:
            x, y, dist = result
            print(f"Color found at ({x},{y}) — radius {dist:.1f}px from center")

            if dist <= max_radius:
                print(f"Detected at radius {dist:.1f}px")

                if dist < 40:
                    print(f"ALERT — radius {dist:.1f}px < {40}px")

                    min_freq = 500
                    max_freq = 2500

                    dist_clamped = min(dist, 40)

                    freq = int(max_freq - ((dist_clamped / 40) * (max_freq - min_freq)))

                    now = time.time()
                    if now - last_beep_time >= 5.0:
                        winsound.Beep(freq, 300)
                        last_beep_time = now
        time.sleep(0.5)

if __name__ == "__main__":
    main()
