import geopandas as gpd

def display_shapefile(file_path):
    try:
        # 1. Shapefile 읽기 (.shp 파일 경로 입력)
        # 팁: .shp 파일과 같은 폴더에 .dbf, .shx, .prj 파일이 함께 있어야 온전하게 읽힙니다.
        gdf = gpd.read_file(file_path)
        
        # 2. 데이터 구조 확인 (총 행과 열의 수)
        print(f"=== 데이터 구조 ===")
        print(f"총 데이터 수(행): {gdf.shape[0]}")
        print(f"속성 컬럼 수(열): {gdf.shape[1]}\n")
        
        # 3. 좌표계(CRS) 정보 확인 (지적측량이나 지도 매핑 시 필수 확인)
        print(f"=== 좌표계(CRS) 정보 ===")
        print(f"{gdf.crs}\n")
        
        # 4. 상위 5개 행을 표 형태로 출력
        print("=== 표 형태 데이터 확인 (상위 5개 행) ===")
        # 판다스와 마찬가지로 head()를 사용해 표 형태로 출력합니다.
        # 가장 오른쪽 컬럼에 'geometry'라는 이름으로 공간 도형 정보(POINT, POLYGON 등)가 자동으로 들어옵니다.
        print(gdf.head())
        
        # (선택 사항) 만약 텍스트가 잘리지 않고 모든 컬럼을 보고 싶다면 아래 주석을 해제하세요.
        # import pandas as pd
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', 1000)
        # print(gdf.head())

    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")

# --- 실행 부분 ---
# 본인의 컴퓨터에 있는 실제 .shp 파일 경로를 입력해 주세요.
# 예시: "C:/data/seoul_cadastral.shp" 또는 "./지적도_데이터.shp"
file_path = "your_file_path_here.shp" 
file_path = "./shp/tl_bus_station_info.shp" 

display_shapefile(file_path)