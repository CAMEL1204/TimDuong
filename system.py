import json
import math
import time
from graph import Node, Edge, Graph

def find_index(target_id, id_list):
    for i in range(len(id_list)):
        if id_list[i] == target_id:
            return i
    return -1

def search_node_index(query, graph, id_list):
    """
    Tìm vị trí (index) dựa trên ID hoặc Tên địa điểm.
    Hỗ trợ tìm kiếm không phân biệt hoa/thường và khớp một phần tên.
    """
    query = query.strip().lower()

    # 1. Ưu tiên tìm theo ID trước (khớp tuyệt đối)
    for i in range(len(id_list)):
        if id_list[i].lower() == query:
            return i

    # 2. Nếu không khớp ID, thử tìm theo Tên (khớp tuyệt đối)
    for i in range(len(graph.nodes)):
        if graph.nodes[i].name.lower() == query:
            return i

    # 3. Nếu vẫn không thấy, thử tìm khớp một phần (Chỉ cần chứa từ khóa)
    # VD: Nhập "thư viện" sẽ khớp với "Thư viện Tạ Quang Bửu"
    for i in range(len(graph.nodes)):
        if query in graph.nodes[i].name.lower():
            return i

    return -1

class FileHandler:
    @staticmethod
    def  loadData(nodes_file, edges_file):
        with open(nodes_file, "r", encoding='utf-8') as f:
            nodes_data = json.load(f)
        with open(edges_file, "r", encoding='utf-8') as f:
            edges_data = json.load(f)

        graph = Graph()
        id_list = []

        for nd in nodes_data:
            id_list.append(str(nd['id']))

        for i in range(len(nodes_data)):
            nd = nodes_data[i]
            node = Node(i, nd['name'], nd['x'], nd['y'])
            graph.addNode(node)

        for ed in edges_data:
            u_str = str(ed['from'])
            v_str = str(ed['to'])

            u = find_index(u_str, id_list)
            v = find_index(v_str, id_list)

            if u == -1 or v == -1:
                continue

            x1, y1 = graph.nodes[u].x, graph.nodes[u].y
            x2, y2 = graph.nodes[v].x, graph.nodes[v].y
            weight = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            graph.addEdge(Edge(u, v, weight))
            if ed.get('bidirectional', True):
                graph.addEdge(Edge(v, u, weight))

        return graph, id_list

    @staticmethod
    def saveData(path, distance, graph, id_list, output_file="output_path.txt"):
        if len(path) == 0 or distance == -1:
            with open(output_file, "w", encoding='utf-8') as f:
                f.write("Không tìm thấy đường đi")
            return

        lines = []
        lines.append("=" * 55)
        lines.append("         LỘ TRÌNH DI CHUYỂN NGẮN NHẤT")
        lines.append("=" * 55)
        lines.append(f"Tổng quãng đường: {distance:.2f} px")
        lines.append("-" * 55)

        for step, index in enumerate(path):
            real_id = id_list[index]
            node_name = graph.nodes[index].name
            lines.append(f"Bước {step + 1}: ID {real_id} -> {node_name}")

        lines.append("=" * 55)

        with open(output_file, "w", encoding='utf-8') as f:
            f.write("\n".join(lines) + "\n")
        print(f"[OK] Đã ghi kết quả vào file: {output_file}")
class UI:
    @staticmethod
    def showMenu():
        print("\n" + "="*50)
        print(" HỆ THỐNG TÌM ĐƯỜNG ĐI NGẮN NHẤT - ĐHBK HÀ NỘI")
        print("="*50)
        print("1. Nạp dữ liệu bản đồ")
        print("2. Tìm đường đi ngắn nhất")
        print("3. Chạy bài kiểm tra hiệu năng (Performance Test)")
        print("0. Thoát")
        print("="*50)

    @staticmethod
    def display(path, distance, graph, id_list):
        if len(path) == 0:
            print("\n[!] Không tìm thấy đường đi giữa hai điểm này.")
            return

        print(f"\n-> HOÀN THÀNH! Tổng quãng đường: {distance:.2f} px")
        print("Lộ trình chi tiết:")
        for index in path:
            print(f"  -> [{id_list[index]}] {graph.nodes[index].name}")


class PerformTest:
    @staticmethod
    def measureTime(func, *args):
        """Hàm bọc để đo thời gian thực thi của bất kỳ hàm nào truyền vào"""
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = (time.perf_counter() - t0) * 1000  # Đổi ra ms
        return result, elapsed

    @staticmethod
    def runTest(navigator_instance, graph):
        """Mô phỏng chạy test với dữ liệu hiện tại"""
        print("\n[Đang chạy Performance Test...]")
        # Lấy bừa điểm đầu và điểm cuối để test thuật toán
        start_idx = 0
        end_idx = len(graph.nodes) - 1

        # Gọi hàm measureTime để đo tốc độ của hàm dijkstra
        (distances, previous), elapsed = PerformTest.measureTime(
            navigator_instance.dijkstra, start_idx, end_idx
        )

        print(f"-> Thuật toán Dijkstra quét qua {len(graph.nodes)} đỉnh mất: {elapsed:.4f} ms")