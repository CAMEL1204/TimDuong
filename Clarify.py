def dijkstra(self, start_id, end_id):
        # Lấy tổng số lượng đỉnh (vertices) của đồ thị từ thuộc tính nodes
        n = len(self.graph.nodes)
        
        # BƯỚC 1: KHỞI TẠO MẢNG SỔ SÁCH (INITIALIZATION)
        # distances[i] lưu khoảng cách ngắn nhất tạm tính từ điểm xuất phát đến đỉnh i
        # Ban đầu chưa đi qua đâu nên gán tất cả bằng Vô cực (float('inf'))
        distances = [float('inf')] * n
        
        # previous[i] lưu chỉ số của đỉnh đứng ngay trước đỉnh i trên con đường ngắn nhất
        # Khởi tạo bằng -1 (nghĩa là chưa có đỉnh nào đứng trước)
        previous = [-1] * n
        
        # Khoảng cách từ điểm xuất phát (start_id) đến chính nó luôn luôn bằng 0
        distances[start_id] = 0

        # BƯỚC 2: KHỞI TẠO HÀNG ĐỢI ƯU TIÊN (MIN-HEAP)
        # Tạo một đối tượng MinHeap tự chế để quản lý các đỉnh cần duyệt
        pq = MinHeap()
        # Đẩy phần tử đầu tiên vào Heap: [khoảng cách hiện tại, chỉ số đỉnh]
        pq.push(0, start_id)

        # BƯỚC 3: VÒNG LẶP DÒ ĐƯỜNG CHÍNH (CORE LOOP)
        # Vòng lặp chạy liên tục cho đến khi hàng đợi ưu tiên không còn phần tử nào
        while len(pq.heap) > 0:
            # Lấy ra phần tử có khoảng cách nhỏ nhất hiện tại từ đỉnh Heap
            current_item = pq.pop()
            current_dist = current_item[0] # Khoảng cách từ gốc đến đỉnh u này
            u = current_item[1]            # Chỉ số (index) của đỉnh u hiện tại

            # TỐI ƯU SỚM (EARLY EXIT):
            # Nếu đỉnh vừa lấy ra khỏi Heap chính là đỉnh Đích (end_id),
            # nghĩa là ta đã tìm được đường ngắn nhất tuyệt đối tới đích. Dừng thuật toán ngay!
            if u == end_id:
                break

            # KIỂM TRA ĐƯỜNG CŨ / LỖI THỜI:
            # Nếu khoảng cách lấy từ Heap ra còn lớn hơn khoảng cách tối ưu đang lưu trong sổ,
            # chứng tỏ đây là một đường đi vòng, không tối ưu -> Bỏ qua không xét tiếp từ đỉnh này nữa.
            if current_dist > distances[u]:
                continue

            # BƯỚC 4: CẬP NHẬT KHOẢNG CÁCH (RELAXATION)
            # Quét qua tất cả các cạnh (edges) lân cận xuất phát từ đỉnh u hiện tại
            # Hàm getNeighbors truy xuất thẳng vào mảng 2 chiều self.adjList[u] với tốc độ O(1)
            for edges in self.graph.getNeighbors(u):
                v = edges.to_node   # Đỉnh lân cận (hàng xóm) kế tiếp
                # new_dist = (Quãng đường ngắn nhất đến u) + (Độ dài con đường từ u sang v)
                new_dist = current_dist + edges.weight

                # NẾU TÌM THẤY CON ĐƯỜNG TỐT HƠN (NGẮN HƠN):
                # Nếu khoảng cách mới này nhỏ hơn khoảng cách cũ đang ghi trong sổ distances[v]
                if new_dist < distances[v]:
                    distances[v] = new_dist  # Gạch bỏ số cũ, cập nhật khoảng cách mới ngắn hơn cho v
                    previous[v] = u          # Ghi vết: Để đến được v ngắn nhất, bắt buộc phải rẽ từ u sang
                    pq.push(new_dist, v)     # Ném đỉnh v kèm khoảng cách mới vào Heap để lát nữa dò tiếp từ v

        # Trả về 2 mảng sổ sách sau khi đã tối ưu xong để phục vụ cho việc in kết quả
        return distances, previous

    def getPath(self, start_id, end_id, previous):
        # Mảng chứa danh sách các đỉnh theo thứ tự di chuyển từ Xuất phát -> Đích
        path = []
        current = end_id

        # BƯỚC 1: TRUY VẾT NGƯỢC (BACKTRACKING)
        # Xuất phát từ Đích (end_id), lùi dần về phía sau theo dấu vết lưu trong mảng previous
        while current != -1:
            path.append(current)          # Thêm đỉnh hiện tại vào lộ trình
            current = previous[current]  # Nhìn sổ xem đỉnh nào dẫn tới đỉnh này thì lùi về đỉnh đó

        # BƯỚC 2: ĐẢO NGƯỢC MẢNG THỦ CÔNG (ARRAY REVERSAL)
        # Vì ta lùi từ Đích về Xuất phát nên mảng path đang bị ngược (Đích -> ... -> Xuất phát).
        # Áp dụng thuật toán hoán đổi 2 con trỏ chạy từ 2 đầu mảng vào giữa để lật ngược lộ trình.
        n = len(path)
        for i in range(n // 2):
            # Tráo đổi phần tử đầu với phần tử cuối, phần tử thứ 2 với phần tử kế cuối...
            path[i], path[n - i - 1] = path[n - i - 1], path[i]

        # Trả về mảng lộ trình đã được sắp xếp đúng thứ tự từ Xuất phát -> Đích
        return path
