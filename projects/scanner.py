import cv2
import threading
import re
import pytesseract
import time
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import CarPlates

is_detecting = False
cap = []
User = get_user_model()

def start_detection(camera_urls):
    global is_detecting, cap
    if not is_detecting:
        is_detecting = True
        cap = [cv2.VideoCapture(url) for url in camera_urls if url]
        print(camera_urls)
        threads = [threading.Thread(target=detect, args=(c, i)) for i, c in enumerate(cap)]
        for t in threads:
            t.start()
        # return cap

def stop_detection():
    global is_detecting, cap
    is_detecting = False
    if cap:
        for c in cap:
            if c.isOpened():
                c.release()
        cap = []

def clean_plate_number(plate_number):
    plate_number = re.sub(r'\W+', '', plate_number).upper()
    return plate_number

def validate_plate(plate_number):
    patterns = [
        re.compile(r'^[A-Z]{2}\d{4}$'),  # Old Chile format: Example XH6640
        re.compile(r'^[A-Z]{4}\d{2}$'),  # New Chile format: Example GKSB78
        re.compile(r'^[A-Z]{2}\d{3}[A-Z]{2}$'),  # Argentina format: Example AB123CD
    ]
    for pattern in patterns:
        if pattern.match(plate_number):
            return True
    return False

def save_plate(plate_number, frame):
    date_time = timezone.now()
    user, created = User.objects.get_or_create(username=plate_number)
    image_path = f"media/car_images/{plate_number}_{int(time.time())}.jpg"
    cv2.imwrite(image_path, frame)
    CarPlates.objects.create(
        plate_number=plate_number,
        user=user,
        car_year=0,
        brand="Test Brand",
        model="Test Model",
        car_type="Test Type",
        image_path=image_path,
        date_time=date_time
    )

def detect(cap, camera_id):
    global is_detecting
    while is_detecting and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --oem 3 --psm 11'
        plate_number_alphanumeric = pytesseract.image_to_string(binary, config=custom_config)
        plate_number_clean = clean_plate_number(plate_number_alphanumeric)

        if validate_plate(plate_number_clean):
            save_plate(plate_number_clean, frame)
        time.sleep(1)

    cap.release()
