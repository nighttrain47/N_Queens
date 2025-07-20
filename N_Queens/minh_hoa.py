import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import time
import os

class NQueensVisualizer:
    def __init__(self, num_queens=4, export_mode=False):
        self.num_queens = num_queens
        self.export_mode = export_mode
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.board_patches = []
        self.queen_patches = []
        self.attack_patches = []
        self.steps = []
        self.current_step = 0
        self.step_counter = 0
        
        # Tạo output folder nếu đang ở export mode
        if self.export_mode:
            self.setup_output_folder()
        
        # Load ảnh queen
        self.load_queen_image()
        self.setup_board()
        
    def setup_output_folder(self):
        """Tạo thư mục output cho việc export hình ảnh"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(current_dir, "output", f"{self.num_queens}Queens")
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"Đã tạo thư mục output: {self.output_dir}")
        
    def load_queen_image(self):
        """Load ảnh quân hậu"""
        try:
            # Tìm đường dẫn đến file queen.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            queen_path = os.path.join(parent_dir, 'queen.png')
            
            if os.path.exists(queen_path):
                self.queen_image = mpimg.imread(queen_path)
                print(f"Đã load ảnh queen từ: {queen_path}")
            else:
                print(f"Không tìm thấy file queen.png tại: {queen_path}")
                self.queen_image = None
        except Exception as e:
            print(f"Lỗi khi load ảnh queen: {e}")
            self.queen_image = None
        
    def setup_board(self):
        """Thiết lập bàn cờ"""
        self.ax.set_xlim(0, self.num_queens)
        self.ax.set_ylim(0, self.num_queens)
        self.ax.set_aspect('equal')
        self.ax.set_title(f'N-Queens Problem ({self.num_queens}x{self.num_queens})', fontsize=16)
        
        # Tắt tick marks
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Vẽ bàn cờ với màu xen kẽ
        for i in range(self.num_queens):
            for j in range(self.num_queens):
                color = 'white' if (i + j) % 2 == 0 else 'lightgray'
                square = patches.Rectangle((j, self.num_queens-1-i), 1, 1, 
                                         facecolor=color, edgecolor='black', linewidth=1)
                self.ax.add_patch(square)
                self.board_patches.append(square)
    
    def clear_queens_and_attacks(self):
        """Xóa tất cả quân hậu và vùng tấn công"""
        for patch in self.queen_patches:
            patch.remove()
        for patch in self.attack_patches:
            patch.remove()
        self.queen_patches.clear()
        self.attack_patches.clear()
    
    def draw_queen(self, row, col, color='red'):
        """Vẽ quân hậu tại vị trí (row, col)"""
        if self.queen_image is not None:
            # Sử dụng ảnh queen.png
            # Mỗi ô có kích thước 1x1 trong coordinate system của matplotlib
            # Chúng ta muốn ảnh chiếm tối đa 80% kích thước ô
            
            # Lấy kích thước gốc của ảnh (pixels)
            img_height, img_width = self.queen_image.shape[:2]
            
            # Trong matplotlib, kích thước ảnh được tính theo DPI
            # Figure size là 10x8 inch, với DPI mặc định 100
            # Vậy mỗi ô có kích thước khoảng 800/num_queens pixels (chiều cao)
            pixels_per_cell = 800 / self.num_queens

            # Kích thước mục tiêu cho ảnh (40% kích thước ô thay vì 60%)
            target_pixels = pixels_per_cell * 0.4
            
            # Tính zoom factor: target_size / original_size
            # Lấy chiều lớn hơn để đảm bảo ảnh không vượt quá ô
            max_original_dimension = max(img_height, img_width)
            zoom_factor = target_pixels / max_original_dimension
            
            # Giới hạn zoom factor để tránh ảnh quá lớn hoặc quá nhỏ
            zoom_factor = max(0.05, min(zoom_factor, 1.5))
            
            # Tạo OffsetImage từ ảnh queen với zoom chính xác
            imagebox = OffsetImage(self.queen_image, zoom=zoom_factor)
            
            # Tạo AnnotationBbox để đặt ảnh tại vị trí chỉ định
            ab = AnnotationBbox(imagebox, (col + 0.5, self.num_queens - 1 - row + 0.5), 
                               frameon=False, pad=0, box_alignment=(0.5, 0.5))
            
            # Thêm màu nền nếu cần (để phân biệt các trạng thái khác nhau)
            if color != 'blue' and color != 'green':  # Không vẽ vòng tròn cho green vì đã có hình vuông
                circle = patches.Circle((col + 0.5, self.num_queens - 1 - row + 0.5), 
                                       0.45, facecolor=color, alpha=0.2, edgecolor=color, linewidth=2)
                self.ax.add_patch(circle)
                self.queen_patches.append(circle)
            
            self.ax.add_artist(ab)
            self.queen_patches.append(ab)
        else:
            # Fallback: Vẽ hình tròn nếu không load được ảnh
            circle = patches.Circle((col + 0.5, self.num_queens - 1 - row + 0.5), 
                                   0.3, facecolor=color, edgecolor='black', linewidth=2)
            self.ax.add_patch(circle)
            self.queen_patches.append(circle)
            
            # Thêm ký tự Q
            text = self.ax.text(col + 0.5, self.num_queens - 1 - row + 0.5, 'Q', 
                               ha='center', va='center', fontsize=20, fontweight='bold', color='white')
            self.queen_patches.append(text)
    
    def draw_attacked_positions(self, state):
        """Vẽ các vị trí bị tấn công"""
        attacked = set()
        
        for row, col in enumerate(state):
            # Tấn công theo hàng ngang (toàn bộ hàng)
            for c in range(self.num_queens):
                if c != col:  # Không đánh dấu vị trí của chính quân hậu
                    attacked.add((row, c))
            
            # Tấn công theo cột dọc (toàn bộ cột)
            for r in range(self.num_queens):
                if r != row:  # Không đánh dấu vị trí của chính quân hậu
                    attacked.add((r, col))
            
            # Tấn công theo đường chéo chính (top-left to bottom-right)
            # Đi lên trái
            r, c = row - 1, col - 1
            while r >= 0 and c >= 0:
                attacked.add((r, c))
                r -= 1
                c -= 1
            # Đi xuống phải
            r, c = row + 1, col + 1
            while r < self.num_queens and c < self.num_queens:
                attacked.add((r, c))
                r += 1
                c += 1
            
            # Tấn công theo đường chéo phụ (top-right to bottom-left)
            # Đi lên phải
            r, c = row - 1, col + 1
            while r >= 0 and c < self.num_queens:
                attacked.add((r, c))
                r -= 1
                c += 1
            # Đi xuống trái
            r, c = row + 1, col - 1
            while r < self.num_queens and c >= 0:
                attacked.add((r, c))
                r += 1
                c -= 1
        
        # Vẽ tất cả các vị trí bị tấn công (trừ vị trí có quân hậu)
        queen_positions = set((row, col) for row, col in enumerate(state))
        
        for attack_row, attack_col in attacked:
            if (attack_row, attack_col) not in queen_positions:
                square = patches.Rectangle((attack_col, self.num_queens-1-attack_row), 1, 1, 
                                         facecolor='red', alpha=0.25, edgecolor='red', linewidth=0.5)
                self.ax.add_patch(square)
                self.attack_patches.append(square)
    
    def add_color_legend(self):
        """Thêm chú thích màu sắc"""
        from matplotlib.patches import Patch
        
        # Tạo các patch cho legend
        legend_elements = [
            Patch(facecolor='red', alpha=0.25, label='Ô bị tấn công\n(không đi được)'),
            Patch(facecolor='green', alpha=0.7, label='Quân hậu đang\nthử đặt'),
            Patch(facecolor='white', edgecolor='black', label='Ô an toàn\n(có thể đặt)')
        ]
        
        # Đặt legend bên ngoài bàn cờ, ở bên phải
        self.ax.legend(handles=legend_elements, loc='center left', 
                      bbox_to_anchor=(1.05, 0.5), fontsize=9, 
                      framealpha=0.9, fancybox=True, shadow=True)
    
    def show_step(self, state, step_type="trying", candidate_col=None, export_step=False):
        """Hiển thị một bước trong thuật toán"""
        self.clear_queens_and_attacks()
        
        # Vẽ các quân hậu đã đặt
        for row, col in enumerate(state):
            self.draw_queen(row, col, 'blue')
        
        # Vẽ các vị trí bị tấn công
        self.draw_attacked_positions(state)
        
        # Nếu đang thử đặt quân hậu mới
        if step_type == "trying" and candidate_col is not None and len(state) < self.num_queens:
            # Vẽ hình vuông xanh lá bao phủ toàn bộ ô (giống như ô màu đỏ)
            square = patches.Rectangle((candidate_col, self.num_queens-1-len(state)), 1, 1, 
                                     facecolor='green', alpha=0.25, edgecolor='green', linewidth=0.5)
            self.ax.add_patch(square)
            self.queen_patches.append(square)
            
            # Vẽ quân hậu lên trên
            self.draw_queen(len(state), candidate_col, 'green')
            title = f'Đang thử đặt quân hậu tại hàng {len(state)}, cột {candidate_col}'
        elif step_type == "backtrack":
            title = f'Quay lui từ trạng thái: {state}'
        elif step_type == "solution":
            title = f'Tìm thấy lời giải: {state}'
        else:
            title = f'Trạng thái hiện tại: {state}'
        
        self.ax.set_title(title, fontsize=12)
        
        # Thêm chú thích màu sắc
        self.add_color_legend()
        
        plt.draw()
        
        # Export hình ảnh nếu được yêu cầu
        if self.export_mode and export_step:
            self.export_current_step(step_type, state, candidate_col)
        
        if not self.export_mode:
            plt.pause(1.5)  # Dừng 1.5 giây để xem rõ (chỉ khi không export)
    
    def export_current_step(self, step_type, state, candidate_col=None):
        """Export bước hiện tại thành file ảnh"""
        self.step_counter += 1
        
        # Tạo tên file dựa trên loại bước
        if step_type == "trying" and candidate_col is not None:
            filename = f"step_{self.step_counter:03d}_trying_row_{len(state)}_col_{candidate_col}.png"
        elif step_type == "backtrack":
            filename = f"step_{self.step_counter:03d}_backtrack_{state}.png"
        elif step_type == "solution":
            filename = f"step_{self.step_counter:03d}_solution_{state}.png"
        else:
            filename = f"step_{self.step_counter:03d}_{step_type}.png"
        
        # Làm sạch tên file (loại bỏ ký tự đặc biệt)
        filename = filename.replace("[", "").replace("]", "").replace(",", "_").replace(" ", "")
        
        filepath = os.path.join(self.output_dir, filename)
        self.fig.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Đã export: {filename}")

# Sao chép các hàm từ 8queens.py với điều chỉnh để có thể visualize
def is_valid_state(state, num_queens):
    return len(state) == num_queens

def get_candidates(state, num_queens):
    if not state:
        return range(num_queens)

    position = len(state)
    candidates = set(range(num_queens))

    for row, col in enumerate(state):
        candidates.discard(col)
        dist = position - row 
        candidates.discard(col + dist)
        candidates.discard(col - dist)

    return candidates

def search_for_final_solution(state, num_queens, path=[]):
    """Tìm một lời giải và trả về đường đi đến lời giải đó"""
    if is_valid_state(state, num_queens):
        return path + [("solution", state.copy())]
    
    for candidate in get_candidates(state, num_queens):
        # Thêm bước thử vào đường đi
        new_path = path + [("trying", state.copy(), candidate)]
        
        state.append(candidate)
        
        # Đệ quy tìm lời giải
        result = search_for_final_solution(state, num_queens, new_path)
        if result:
            return result
        
        # Quay lui và thêm bước backtrack
        state.pop()
        if len(state) > 0:  # Chỉ thêm backtrack nếu không phải trạng thái rỗng
            new_path.append(("backtrack", state.copy()))
    
    return None

def export_solution_steps(num_queens):
    """Export tất cả các bước của một lời giải"""
    print(f"Đang tìm lời giải cho {num_queens}-Queens và export các bước...")
    
    # Tìm đường đi đến lời giải
    solution_path = search_for_final_solution([], num_queens)
    
    if solution_path:
        # Tạo visualizer ở chế độ export
        visualizer = NQueensVisualizer(num_queens, export_mode=True)
        
        print(f"Tìm thấy lời giải! Đang export {len(solution_path)} bước...")
        
        # Export từng bước
        for step_data in solution_path:
            if len(step_data) == 2:  # solution hoặc backtrack
                step_type, state = step_data
                visualizer.show_step(state, step_type, export_step=True)
            elif len(step_data) == 3:  # trying
                step_type, state, candidate = step_data
                visualizer.show_step(state, step_type, candidate, export_step=True)
        
        plt.close(visualizer.fig)
        print(f"Hoàn thành export! Tất cả hình ảnh đã được lưu trong thư mục: {visualizer.output_dir}")
        return True
    else:
        print(f"Không tìm thấy lời giải cho {num_queens}-Queens")
        return False

def search_visualized(state, solutions, num_queens, visualizer, max_solutions=1):
    """Tìm kiếm với visualization"""
    if is_valid_state(state, num_queens):
        solutions.append(state.copy())
        visualizer.show_step(state, "solution")
        return len(solutions) >= max_solutions  # Dừng sau khi tìm đủ số lời giải
    
    for candidate in get_candidates(state, num_queens):
        # Hiển thị bước đang thử
        visualizer.show_step(state, "trying", candidate)
        
        state.append(candidate)
        
        # Đệ quy và kiểm tra nếu cần dừng
        if search_visualized(state, solutions, num_queens, visualizer, max_solutions):
            return True
        
        # Quay lui
        state.pop()
        visualizer.show_step(state, "backtrack")
    
    return False

def solve_visualized(num_queens, max_solutions=1):
    """Giải bài toán với visualization"""
    visualizer = NQueensVisualizer(num_queens)
    solutions = []
    state = []
    
    print(f"Bắt đầu giải bài toán {num_queens}-Queens...")
    print("Đóng cửa sổ để kết thúc chương trình.")
    
    # Hiển thị bàn cờ trống ban đầu
    visualizer.show_step([], "initial")
    
    search_visualized(state, solutions, num_queens, visualizer, max_solutions)
    
    print(f"\nTìm thấy {len(solutions)} lời giải:")
    for i, solution in enumerate(solutions, 1):
        print(f"Lời giải {i}: {solution}")
    
    # Giữ cửa sổ mở
    plt.show()
    
    return solutions

# Hàm demo với nhiều tùy chọn
def demo_nqueens():
    """Demo chương trình với menu lựa chọn"""
    print("=== DEMO THUẬT TOÁN N-QUEENS VỚI VISUALIZATION ===")
    print("1. 4-Queens (nhanh)")
    print("2. 5-Queens (trung bình)")
    print("3. 6-Queens (chậm hơn)")
    print("4. 8-Queens (chỉ 1 lời giải đầu tiên)")
    print("5. Tùy chỉnh")
    print("6. Export các bước của lời giải (4-Queens)")
    print("7. Export các bước của lời giải (8-Queens)")
    print("8. Export tùy chỉnh")
    
    choice = input("Chọn option (1-8): ").strip()
    
    if choice == "1":
        solve_visualized(4, max_solutions=2)
    elif choice == "2":
        solve_visualized(5, max_solutions=1)
    elif choice == "3":
        solve_visualized(6, max_solutions=1)
    elif choice == "4":
        solve_visualized(8, max_solutions=1)
    elif choice == "5":
        try:
            n = int(input("Nhập số quân hậu (khuyến nghị 4-6): "))
            max_sol = int(input("Số lời giải tối đa muốn tìm (1-3): "))
            if n > 0 and max_sol > 0:
                solve_visualized(n, max_solutions=max_sol)
            else:
                print("Vui lòng nhập số dương!")
        except ValueError:
            print("Đầu vào không hợp lệ!")
    elif choice == "6":
        export_solution_steps(4)
    elif choice == "7":
        export_solution_steps(8)
    elif choice == "8":
        try:
            n = int(input("Nhập số quân hậu để export (khuyến nghị 4-8): "))
            if n > 0:
                export_solution_steps(n)
            else:
                print("Vui lòng nhập số dương!")
        except ValueError:
            print("Đầu vào không hợp lệ!")
    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    demo_nqueens()