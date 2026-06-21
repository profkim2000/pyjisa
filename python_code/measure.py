from shapely.geometry import Polygon
from pyproj import Transformer
from shapely.ops import transform

def calculate_wgs84_polygon_area(lon_lat_list):
    """
    WGS84(EPSG:4326) 경위도 좌표 리스트를 받아 
    제곱미터(㎡) 및 평수 단위로 정확한 면적을 계산합니다.
    """
    # 1. 입력받은 경위도 좌표로 Shapely 폴리곤 생성
    # (주의: Shapely는 기본적으로 (X, Y) 순서이므로 (경도, 위도) 순으로 넣어야 합니다)
    polygon_4326 = Polygon(lon_lat_list)
    
    # 2. 좌표 변환 정의 (EPSG:4326 -> 한국 표준 미터 좌표계인 EPSG:5179 UTM-K 사용)
    # ※ 만약 해외 지역이라면 해당 지역의 UTM Zone 번호나 EPSG:3857 등을 사용할 수 있습니다.
    project = Transformer.from_crs("EPSG:4326", "EPSG:5179", always_xy=True).transform
    
    # 3. 폴리곤의 모든 꼭짓점 좌표를 미터(m) 단위 좌표계로 일괄 변환
    polygon_meter = transform(project, polygon_4326)
    
    # 4. 변환된 폴리곤의 면적 구하기 (.area 메서드 활용)
    area_sq_meters = polygon_meter.area
    
    # 5. 평수로 환산 (1제곱미터 = 0.3025평)
    area_pyeong = area_sq_meters * 0.3025
    
    return area_sq_meters, area_pyeong

# --- 실행 및 테스트 ---
if __name__ == "__main__":
    # 예시 좌표: 서울시청 인근을 아우르는 가상의 사각형 필지 (경도, 위도 순서)
    # ※ 주의: 폴리곤을 닫기 위해 첫 번째 좌표와 마지막 좌표는 같아야 합니다.
    test_coordinates = [
        (126.9770, 37.5670),  # 좌측 상단
        (126.9790, 37.5670),  # 우측 상단
        (126.9790, 37.5650),  # 우측 하단
        (126.9770, 37.5650),  # 좌측 하단
        (126.9770, 37.5670)   # 다시 첫 점으로 돌아와서 닫기
    ]
    
    m2, pyeong = calculate_wgs84_polygon_area(test_coordinates)
    
    print(f"=== 폴리곤 면적 계산 결과 ===")
    print(f"계산된 면적 : {m2:,.2f} ㎡")
    print(f"평수 환산    : {pyeong:,.1f} 평")