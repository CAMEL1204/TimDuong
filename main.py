# =================================================================
# FILE CHẠY CHÍNH (MAIN.PY) - TỔNG HỢP VÀ ĐIỀU PHỐI
# =================================================================
from system import FileHandler, UI, PerformTest, search_node_index
from navigator import Navigator


def main():
    graph = None
    id_list = None
    navigator = None

    while True:
        UI.showMenu()
        choice = input("Chọn chức năng (0-3): ")

        if choice == '1':
            print("\n[Đang nạp dữ liệu]")
            try:
                graph, id_list = FileHandler.loadData("data/nodes.json", "data/edges.json")
                navigator = Navigator(graph)
                print(f"-> Nạp thành công! Sẵn sàng xử lý {len(graph.nodes)} địa điểm.")
            except FileNotFoundError:
                print("-> [LỖI] Không tìm thấy file! Đảm bảo nodes.json và edges.json ở trong thư mục 'data/'.")
            except Exception as e:
                print(f"-> [LỖI] Quá trình nạp thất bại: {e}")

        elif choice == '2':
            if graph is None:
                print("\n[!] Vui lòng nạp dữ liệu (Chọn phím 1) trước khi tìm đường!")
                continue

            # Nâng cấp phần Input: Hỗ trợ nhập Tên hoặc ID
            start_str = input("Nhập Tên hoặc ID điểm xuất phát (VD: 'C2', 'thư viện', '1'): ").strip()
            end_str = input("Nhập Tên hoặc ID điểm đích: ").strip()

            # Sử dụng hàm tìm kiếm thông minh mới
            start_idx = search_node_index(start_str, graph, id_list)
            end_idx = search_node_index(end_str, graph, id_list)

            # Báo lỗi rõ ràng nếu nhập sai tên
            if start_idx == -1:
                print(f"\n[!] Không tìm thấy địa điểm nào khớp với từ khóa '{start_str}'.")
                continue
            if end_idx == -1:
                print(f"\n[!] Không tìm thấy địa điểm nào khớp với từ khóa '{end_str}'.")
                continue

            # Trích xuất tên chuẩn xác để in ra màn hình cho đẹp
            start_name = graph.nodes[start_idx].name
            end_name = graph.nodes[end_idx].name
            print(f"\n[Đang tính lộ trình: {start_name} -> {end_name}...]")

            distances, previous = navigator.dijkstra(start_idx, end_idx)
            path = navigator.getPath(start_idx, end_idx, previous)
            total_distance = distances[end_idx] if distances[end_idx] != float('inf') else -1

            UI.display(path, total_distance, graph, id_list)
            FileHandler.saveData(path, total_distance, graph, id_list, "output_path.txt")

        elif choice == '3':
            if graph is None:
                print("\n[!] Vui lòng nạp dữ liệu (Chọn phím 1) trước khi test!")
                continue
            PerformTest.runTest(navigator, graph)

        elif choice == '0':
            print("\nCảm ơn bạn đã sử dụng hệ thống! Tạm biệt.")
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ. Vui lòng nhập từ 0 đến 3.")


if __name__ == "__main__":
    main()