import tkinter as tk
from tkinter import ttk, messagebox
from pyproj import Transformer, CRS

class CoordConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("공간정보 좌표 변환기 (PyProj GUI)")
        self.root.geometry("480x420")
        self.root.resizable(False, False)

        # 자주 사용하는 대표적인 EPSG 코드 목록 (이외의 코드는 직접 입력 가능)
        self.common_epsg = [
            "4326 (WGS84 위경도)",
            "3857 (Web Mercator / 구글지도)",
            "5186 (중부원점 - GR80)",
            "5181 (다음/카카오지도)",
            "5179 (네이버지도 / UTM-K)",
            "5174 (기존 지적도 - Bessel)",
            "직접 입력 (숫자만)"
        ]

        self.create_widgets()

    def create_widgets(self):
        # 입력 값 제한 (숫자, 소수점, 마이너스 부호만 허용)
        vcmd = (self.root.register(self.validate_numeric), '%P')

        # --- Source (출발 좌표계) 세션 ---
        src_frame = ttk.LabelFrame(self.root, text=" 출발 좌표계 (Source) ", padding=10)
        src_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(src_frame, text="EPSG 선택:").grid(row=0, column=0, sticky="w", pady=5)
        self.src_combo = ttk.Combobox(src_frame, values=self.common_epsg, width=25, state="readonly")
        self.src_combo.grid(row=0, column=1, columnspan=2, sticky="w", padx=5)
        self.src_combo.current(0) # 기본값 EPSG:4326
        self.src_combo.bind("<<ComboboxSelected>>", lambda e: self.toggle_entry(self.src_combo, self.src_entry))

        self.src_entry = ttk.Entry(src_frame, width=10, state="disabled")
        self.src_entry.grid(row=0, column=3, sticky="w")

        ttk.Label(src_frame, text="X 좌표 (경도):").grid(row=1, column=0, sticky="w", pady=5)
        self.src_x = ttk.Entry(src_frame, validate='key', validatecommand=vcmd, width=15)
        self.src_x.grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(src_frame, text="Y 좌표 (위도):").grid(row=1, column=2, sticky="w", pady=5)
        self.src_y = ttk.Entry(src_frame, validate='key', validatecommand=vcmd, width=15)
        self.src_y.grid(row=1, column=3, sticky="w", padx=5)

        # --- Target (도착 좌표계) 세션 ---
        tgt_frame = ttk.LabelFrame(self.root, text=" 도착 좌표계 (Target) ", padding=10)
        tgt_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(tgt_frame, text="EPSG 선택:").grid(row=0, column=0, sticky="w", pady=5)
        self.tgt_combo = ttk.Combobox(tgt_frame, values=self.common_epsg, width=25, state="readonly")
        self.tgt_combo.grid(row=0, column=1, columnspan=2, sticky="w", padx=5)
        self.tgt_combo.current(1) # 기본값 EPSG:3857
        self.tgt_combo.bind("<<ComboboxSelected>>", lambda e: self.toggle_entry(self.tgt_combo, self.tgt_entry))

        self.tgt_entry = ttk.Entry(tgt_frame, width=10, state="disabled")
        self.tgt_entry.grid(row=0, column=3, sticky="w")

        # --- 변환 실행 버튼 ---
        btn_convert = ttk.Button(self.root, text="▶ 좌표 변환 실행 ◀", command=self.convert_coordinates)
        btn_convert.pack(fill="x", padx=15, pady=10)

        # --- 변환 결과 세션 ---
        res_frame = ttk.LabelFrame(self.root, text=" 변환 결과 (Result) ", padding=10)
        res_frame.pack(fill="both", expand=True, padx=15, pady=10)

        ttk.Label(res_frame, text="변환된 X:").grid(row=0, column=0, sticky="w", pady=5)
        self.res_x = ttk.Entry(res_frame, width=35)
        self.res_x.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(res_frame, text="변환된 Y:").grid(row=1, column=0, sticky="w", pady=5)
        self.res_y = ttk.Entry(res_frame, width=35)
        self.res_y.grid(row=1, column=1, sticky="w", padx=5)

    def validate_numeric(self, text):
        # 입력값이 비어있거나, 숫자, 소수점, 마이너스 부호로만 이루어졌는지 검증
        if text == "" or text == "-":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False

    def toggle_entry(self, combo, entry):
        # '직접 입력' 선택시에만 우측 텍스트 입력창을 활성화
        if "직접 입력" in combo.get():
            entry.config(state="normal")
            entry.focus()
        else:
            entry.delete(0, tk.END)
            entry.config(state="disabled")

    def get_epsg_code(self, combo, entry):
        # 콤보박스 혹은 직접 입력창에서 순수 EPSG 숫자 코드를 추출
        selection = combo.get()
        if "직접 입력" in selection:
            code = entry.get().strip()
            if not code.isdigit():
                raise ValueError("직접 입력창에 올바른 EPSG 숫자 코드를 입력해주세요.")
            return f"EPSG:{code}"
        else:
            code = selection.split(" ")[0]
            return f"EPSG:{code}"

    def convert_coordinates(self):
        # 결과창 초기화
        self.res_x.delete(0, tk.END)
        self.res_y.delete(0, tk.END)

        try:
            # 1. EPSG 코드 가져오기 및 검증
            src_epsg = self.get_epsg_code(self.src_combo, self.src_entry)
            tgt_epsg = self.get_epsg_code(self.tgt_combo, self.tgt_entry)

            # pyproj 내부적으로 존재하는 올바른 EPSG 코드인지 검증
            CRS.from_string(src_epsg)
            CRS.from_string(tgt_epsg)

            # 2. 입력 좌표 가져오기
            if not self.src_x.get() or not self.src_y.get():
                raise ValueError("X 좌표와 Y 좌표를 모두 입력해주세요.")
            
            x_val = float(self.src_x.get())
            y_val = float(self.src_y.get())

            # 3. 좌표 변환 수행 (always_xy=True로 축 순서 고정)
            transformer = Transformer.from_crs(src_epsg, tgt_epsg, always_xy=True)
            tgt_x, tgt_y = transformer.transform(x_val, y_val)

            # 4. 결과 출력 (소수점 6자리까지 지적/정밀측량 수준 표기)
            self.res_x.insert(0, f"{tgt_x:.6f}")
            self.res_y.insert(0, f"{tgt_y:.6f}")

        except Exception as e:
            messagebox.showerror("오류 발생", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordConverterApp(root)
    root.mainloop()