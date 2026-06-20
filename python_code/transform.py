from pyproj import Transformer

def convert_4326_to_3857(lat, lon):
    # Transformer 객체 생성
    # always_xy=True 옵션을 주면 EPSG:4326 환경에서도 (경도, 위도) 순서로 입출력을 고정합니다.
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
    
    # 변환 실행 (경도, 위도 순으로 입력)
    x, y = transformer.transform(lon, lat)
    
    return x, y

# 예시: 서울시청 좌표 (위도, 경도)
seoul_lat = 37.5665
seoul_lon = 126.9780

x_3857, y_3857 = convert_4326_to_3857(seoul_lat, seoul_lon)

print(print("--- 변환 결과 ---"))
print(f"원본 EPSG:4326 (위도, 경도): ({seoul_lat}, {seoul_lon})")
print(f"변환 EPSG:3857 (X, Y 미터): ({x_3857:.2f}, {y_3857:.2f})")