import numpy as np

# Hàm kiểm tra xem đã tìm được một lời giải hợp lệ chưa
def is_valid_state(state, num_queens):
    # Một lời giải hợp lệ khi đã đặt đủ số quân hậu
    return len(state) == num_queens

# Hàm lấy các vị trí (cột) ứng viên cho hàng tiếp theo
def get_candidates(state, num_queens):
    # Nếu chưa có quân hậu nào, tất cả các cột đều là ứng viên
    if not state:
        return range(num_queens)

    # Vị trí (hàng) hiện tại đang cần đặt quân hậu
    position = len(state)
    # Bắt đầu với tất cả các cột có thể
    candidates = set(range(num_queens))

    # Lặp qua các quân hậu đã đặt để loại bỏ các vị trí bị tấn công
    for row, col in enumerate(state):
        # 1. Loại bỏ cột đã có quân hậu (tấn công theo chiều dọc)
        candidates.discard(col)
        
        # 2. Loại bỏ các vị trí bị tấn công theo đường chéo
        # Tính khoảng cách hàng giữa vị trí hiện tại và quân hậu đã đặt
        # === PHẦN SỬA 1 ===
        dist = position - row 
        
        # Loại bỏ vị trí trên đường chéo (xuống-phải)
        candidates.discard(col + dist)
        # Loại bỏ vị trí trên đường chéo (xuống-trái)
        candidates.discard(col - dist)

    return candidates

# Hàm tìm kiếm đệ quy (backtracking)
def search(state, solutions, num_queens):
    # Nếu đã tìm thấy một lời giải hoàn chỉnh, thêm vào danh sách và dừng nhánh này
    if is_valid_state(state, num_queens):
        solutions.append(state.copy())
        return
    
    # Lặp qua các ứng viên hợp lệ cho hàng hiện tại
    for candidate in get_candidates(state, num_queens):
        # Đặt thử quân hậu vào vị trí ứng viên
        state.append(candidate)
        # Tiếp tục tìm kiếm cho hàng tiếp theo
        search(state, solutions, num_queens)
        # Quay lui (backtrack): gỡ quân hậu vừa đặt ra để thử phương án khác
        # Dòng print này giúp theo dõi quá trình quay lui
        # print(f"Backtracking from state: {state}") 
        state.pop() # Sử dụng pop() hiệu quả hơn remove(candidate) khi phần tử cuối cùng luôn là phần tử cần xóa

# Hàm chính để giải bài toán
def solve(num_queens):
    solutions = []
    state = []
    search(state, solutions, num_queens)
    return solutions

# Hàm main chạy chương trình
if __name__ == "__main__":
    try:
        num_queens = int(input("Nhap so quan hau (ví dụ: 4 hoặc 8): "))
        if num_queens <= 0:
            print("Vui lòng nhập một số nguyên dương.")
        else:
            print(f"Bàn cờ trống {num_queens}x{num_queens}:")
            empty_board = np.full((num_queens, num_queens), "-")
            print(empty_board)
            
            solutions = solve(num_queens)
            
            print(f"\n=> Tong so loi giai tim duoc: {len(solutions)}")
            
            # In ra từng lời giải
            for index, solution in enumerate(solutions, start=1):
                board = np.full((num_queens, num_queens), "-")
                for row, col in enumerate(solution):
                    board[row][col] = 'Q'
                
                print(f"\n--- Loi giai {index}: {solution} ---")
                
                # In bàn cờ
                for row in board:
                    print(" ".join(row))
                
                # In theo tọa độ
                # === PHẦN SỬA 2 ===
                print("Toa do cac quan hau (hàng, cột):", end=" ")
                coordinates = []
                for row, col in enumerate(solution):
                    coordinates.append(f"({row}, {col})")
                print(", ".join(coordinates))

    except ValueError:
        print("Đầu vào không hợp lệ. Vui lòng nhập một số nguyên.")


