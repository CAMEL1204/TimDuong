```markdown
# HỆ THỐNG TÌM ĐƯỜNG ĐI NGẮN NHẤT - ĐHBK HÀ NỘI (DSA PROJECT)

Dự án Bài tập lớn môn **Cấu trúc dữ liệu và Giải thuật (DSA)**. Chương trình sử dụng mô hình lập trình hướng đối tượng (OOP), triển khai cấu trúc dữ liệu **Đồ thị dạng Danh sách kề (Adjacency List)** bằng **100% mảng nguyên thủy (List)** và tự xây dựng **Hàng đợi ưu tiên (Min-Heap / Priority Queue)** từ đầu để tối ưu hóa thuật toán **Dijkstra**.

---

## 📌 MỤC TIÊU & YÊU CẦU ĐẠT ĐƯỢC
- **Cấu trúc dữ liệu chính:** Biểu diễn đồ thị bản đồ bằng Danh sách kề thông qua mảng 2 chiều (`List of Lists`).
- **Hàng đợi ưu tiên:** Không sử dụng thư viện có sẵn (`heapq`, `queue`), tự cài đặt cấu trúc `MinHeap` với các hàm `push()` (Sift-up) và `pop()` (Sift-down) để đạt độ phức tạp $O(\log V)$.
- **Chỉ sử dụng mảng:** Hoàn toàn vắng bóng cấu trúc Dictionary `{}` hoặc Map trong lõi lưu trữ dữ liệu và thuật toán, sử dụng kỹ thuật ánh xạ Chỉ số mảng (`Index-based mapping`) để quản lý đỉnh và cạnh.
- **Xử lý tệp tin:** Đáp ứng yêu cầu bắt buộc phải có hai phương thức `loadData()` (nạp dữ liệu từ file JSON, tự động tính khoảng cách hình học Euclid làm trọng số) và `saveData()` (xuất lộ trình chi tiết ra file text).
- **Kiểm thử dữ liệu lớn:** Tích hợp bộ sinh dữ liệu mẫu nhằm đánh giá chính xác hiệu năng tốc độ di chuyển thực tế của thuật toán (Performance Test).

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN
```text
BTL_TimDuong/
│
├── data/
│   ├── nodes.json         # Cơ sở dữ liệu chứa tọa độ (x, y) và tên các tòa nhà BKHN
│   ├── edges.json         # Cơ sở dữ liệu chứa các liên kết đường đi (Một chiều/Hai chiều)
│   ├── large_nodes.json   # Bộ dữ liệu lớn (10.000 đỉnh) dùng để test hiệu năng
│   └── large_edges.json   # Bộ dữ liệu lớn (~35.000 cạnh) dùng để test hiệu năng
│
├── graph.py               # [Module Cấu trúc] Định nghĩa các Class: Node, Edge, Graph
├── navigator.py           # [Module Thuật toán] Triển khai cấu trúc MinHeap và bộ lõi Dijkstra
├── system.py              # [Module Hệ thống] Chứa Class FileHandler, UI, PerformTest và bộ tìm kiếm
├── generate_data.py       # [Script phụ] Dùng để tự động sinh ngẫu nhiên bộ dữ liệu lớn 10.000 điểm
└── main.py                # [Nhạc trưởng] Điều phối luồng chạy, hiển thị Menu Console tương tác

```

---

## 🛠️ CHI TIẾT CÁC MODULE CHỨC NĂNG

### 1. `graph.py` (Quản lý cấu trúc dữ liệu đồ thị)

Gồm 3 thành phần chính bám sát Class Diagram:

* `Node`: Lưu chỉ số mảng (`id` dạng int), tên gọi (`name`) và tọa độ (`x`, `y`).
* `Edge`: Lưu chỉ số đỉnh đầu (`from_node`), đỉnh cuối (`to_node`) và trọng số khoảng cách (`weight`).
* `Graph`: Quản lý danh sách các node (`self.nodes`) và bảng danh sách kề dạng mảng 2 chiều (`self.adjList`). Khi lấy các đỉnh lân cận thông qua `getNeighbors(node_id)`, chương trình truy xuất trực tiếp trong ngăn mảng với chi phí thời gian cực hạn $O(1)$.

### 2. `navigator.py` (Bộ não thuật toán)

* `MinHeap`: Tự triển khai bằng mảng 1 chiều cơ bản. Hàm `push` thực hiện Sift-up và `pop` thực hiện Sift-down theo cấu trúc cây nhị phân để đảm bảo luôn lấy ra điểm có khoảng cách nhỏ nhất trong $O(\log V)$.
* `Navigator`:
* Hàm `dijkstra()`: Áp dụng MinHeap để liên tục cập nhật mảng khoảng cách ngắn nhất, bổ sung tính năng **Dừng sớm (Early Exit)** ngay khi tìm thấy đích để tiết kiệm tài nguyên.
* Hàm `getPath()`: Truy vết ngược mảng dấu vết để dựng lại lộ trình, sử dụng kỹ thuật hoán đổi 2 con trỏ thủ công để đảo ngược mảng thay vì dùng thư viện.



### 3. `system.py` (Xử lý File IO, Tìm kiếm & Giao diện)

* `FileHandler`:
* `loadData()`: Đọc tệp tin JSON và sử dụng công thức khoảng cách $d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$ để tự tạo trọng số cho cạnh.
* `saveData()`: Ghi lộ trình tìm đường ngắn nhất thành một báo cáo định dạng chuẩn hóa vào tệp `output_path.txt`.


* `search_node_index()`: Hàm tìm kiếm thông minh cho phép người dùng nhập tự do bằng Mã số ID, Tên viết tắt hoặc Tên khớp một phần (không phân biệt chữ hoa/thường) thông qua quét mảng tuần tính.
* `PerformTest`: Sử dụng bộ đếm thời gian độ chính xác cao `time.perf_counter()` để đo tốc độ tính toán tính bằng mili-giây (ms).

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT & CHẠY ỨNG DỤNG

### Bước 1: Chuẩn bị Thư mục và File dữ liệu

Đảm bảo bạn đã đặt file `nodes.json` và `edges.json` vào bên trong thư mục mang tên `data` nằm chung cấp với các file code `.py`.

### Bước 2: Chạy chương trình chính

Mở Terminal / Command Prompt tại thư mục dự án và thực hiện lệnh:

```bash
python main.py

```

### Bước 3: Tương tác qua Menu Hệ thống

Khi menu hiển thị, bạn thực hiện theo các bước sau:

1. Nhấn phím `1` để nạp bản đồ vào bộ nhớ RAM.
2. Nhấn phím `2` để thực hiện chức năng tìm đường. Hệ thống sẽ yêu cầu bạn nhập điểm đầu và điểm cuối (Ví dụ: Nhập điểm xuất phát là `c2` và điểm đến là `thư viện`). Lộ trình chi tiết sẽ hiển thị lên màn hình và tự động xuất ra file `output_path.txt`.
3. Nhấn phím `3` để thực hiện bài test tốc độ thực thi của thuật toán.

```

```
