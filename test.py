import threading
count = 0 # Khởi tạo biến count bằng 0
def update_count(): # Định nghĩa một hàm để cập nhật và in ra biến count
    global count # Khai báo biến toàn cục count
    count += 1 # Tăng biến count lên 1
    print(count) # In ra màn hình giá trị của biến count
    timer = threading.Timer(1, update_count) # Khởi tạo lại luồng Timer với khoảng thời gian là 1 giây và hàm là update_count
    timer.start() # Bắt đầu luồng Timer

timer = threading.Timer(1, update_count) # Khởi tạo luồng Timer đầu tiên với khoảng thời gian là 1 giây và hàm là update_count
timer.start() # Bắt đầu luồng Timer
