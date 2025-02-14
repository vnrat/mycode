from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import DeleteHistoryRequest

# Nhập API ID và API Hash từ my.telegram.org
api_id = "28279515"  # Thay bằng API ID của bạn
api_hash = "a5ffcd4952c161d7ee8f647264614512"  # Thay bằng API Hash của bạn

# Khởi tạo Telegram Client
with TelegramClient(None, api_id, api_hash) as client:  # None = Không lưu session
    try:
        client.connect()  # Kết nối với Telegram

        if not client.is_user_authorized():  # Nếu chưa đăng nhập
            phone_number = input("📱 Nhập số điện thoại (bao gồm mã quốc gia): ")
            client.send_code_request(phone_number)  # Gửi mã OTP
            code = input("📩 Nhập mã OTP: ")
            try:
                client.sign_in(phone_number, code)  # Đăng nhập với OTP
            except SessionPasswordNeededError:
                password = input("🔑 Nhập mật khẩu 2 bước: ")
                client.sign_in(password=password)  # Nhập password nếu cần

        me = client.get_me()  # Lấy thông tin tài khoản đăng nhập
        print(f"🔹 Đăng nhập thành công với tài khoản: {me.first_name} (ID: {me.id})\n")

        # Bắt đầu quét các cuộc trò chuyện
        dialogs = client.get_dialogs()
        deleted_chats = []  # Danh sách cuộc trò chuyện với tài khoản bị xóa

        print("📌 Danh sách các cuộc trò chuyện với 'Deleted Account':")
        for dialog in dialogs:
            if not dialog.name.strip():  # Phát hiện tài khoản bị xóa (tên rỗng)
                print(f"🔴 ID: {dialog.id} (Deleted Account)")
                deleted_chats.append(dialog)

        # Nếu có tài khoản bị xóa, hỏi trước khi thực hiện xóa
        if deleted_chats:
            confirm = input("\n❓ Bạn có muốn xóa tất cả cuộc trò chuyện với 'Deleted Account'? (y/n): ").strip().lower()

            if confirm == "y":
                for chat in deleted_chats:
                    print(f"🗑 Đang xóa cuộc trò chuyện ID {chat.id}...")
                    try:
                        client(DeleteHistoryRequest(peer=chat.entity, max_id=0, revoke=True))  # Xóa tin nhắn
                        print(f"✅ Đã xóa cuộc trò chuyện ID {chat.id}")
                    except Exception as e:
                        print(f"❌ Lỗi khi xóa ID {chat.id}: {e}")
            else:
                print("⚠️ Hủy xóa, không có cuộc trò chuyện nào bị xóa.")
        else:
            print("✅ Không có cuộc trò chuyện nào với 'Deleted Account'.")

    except Exception as e:
        print(f"❌ Lỗi đăng nhập: {e}")
