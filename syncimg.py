import os
import telebot
from hashlib import md5

# Thông tin Bot
API_TOKEN = '7433233012:AAE2qytIbLm3Tak0EFssZGRj_g5poyR6qvQ'  # Thay bằng API token của bot
CHAT_ID = '-1002401061978'  # Thay bằng ID nhóm hoặc người nhận
FOLDER_PATH = 'E:/img'  # Thay bằng đường dẫn tới thư mục ảnh
HASH_FILE = 'uploaded_hashes.txt'  # File để lưu hash ảnh đã đồng bộ

bot = telebot.TeleBot(API_TOKEN)


def calculate_file_hash(file_path):
    """Tính hash MD5 của file để kiểm tra trùng lặp."""
    with open(file_path, 'rb') as f:
        return md5(f.read()).hexdigest()


def get_uploaded_hashes():
    """Đọc danh sách hash đã được tải lên từ file."""
    if not os.path.exists(HASH_FILE):
        return set()
    with open(HASH_FILE, 'r') as f:
        return set(f.read().splitlines())


def save_uploaded_hash(hash_value):
    """Lưu hash của file đã tải lên."""
    with open(HASH_FILE, 'a') as f:
        f.write(hash_value + '\n')


def sync_images():
    """Đồng bộ ảnh từ thư mục lên Telegram."""
    uploaded_hashes = get_uploaded_hashes()
    all_files = os.listdir(FOLDER_PATH)
    images = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    uploaded_count = 0
    for image in images:
        image_path = os.path.join(FOLDER_PATH, image)
        image_hash = calculate_file_hash(image_path)

        if image_hash in uploaded_hashes:
            print(f"Đã đồng bộ trước đó: {image}")
            continue

        with open(image_path, 'rb') as img:
            try:
                bot.send_photo(CHAT_ID, img)
                print(f"Đã đồng bộ: {image}")
                save_uploaded_hash(image_hash)
                uploaded_count += 1
            except Exception as e:
                print(f"Lỗi khi gửi ảnh {image}: {e}")

    if uploaded_count == 0:
        print("Không có ảnh mới để đồng bộ.")
    else:
        print(f"Đã đồng bộ {uploaded_count} ảnh.")
        bot.send_message(CHAT_ID, f"Đã đồng bộ {uploaded_count} ảnh từ thư mục.")


if __name__ == '__main__':
    sync_images()
