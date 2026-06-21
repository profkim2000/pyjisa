import math
import requests
from io import BytesIO
from PIL import Image, ImageDraw

def latlon_to_pixel(lat, lon, zoom, xtile, ytile):
    """
    입력받은 위경도 좌표가 해당 타일(256x256) 내에서 
    정확히 몇 번째 X, Y 픽셀 위치에 있는지 계산합니다.
    """
    n = 2.0 ** zoom
    
    # 전체 지도에서의 절대 타일 위치(소수점 포함)
    x_exact = (lon + 180.0) / 360.0 * n
    lat_rad = math.radians(lat)
    y_exact = (1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * n
    
    # 현재 타일의 시작점과의 차이를 픽셀(256px)로 환산
    pixel_x = int((x_exact - xtile) * 256)
    pixel_y = int((y_exact - ytile) * 256)
    
    return pixel_x, pixel_y

def generate_wgs84_png(latitude, longitude, zoom=16):
    tile_size = 256
    n = 2.0 ** zoom
    
    # 1. 위경도를 기준으로 타일 번호 계산
    xtile = int((longitude + 180.0) / 360.0 * n)
    lat_rad = math.radians(latitude)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    
    # 2. 차단이 없는 안정적인 CartoDB 오픈 타일 서버 사용
    # (기존 OpenStreetMap의 Access Blocked 문제를 해결합니다)
    url = f"https://basemaps.cartocdn.com/rastertiles/voyager/{zoom}/{xtile}/{ytile}.png"
    
    # 브라우저처럼 보이도록 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("지도 타일 다운로드 중...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"지도 다운로드 실패 (에러 코드: {response.status_code})")
        return

    # 3. 이미지 로드 및 그리기 준비
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    # 4. 수학적 계산을 통해 타일 내부의 정확한 픽셀 위치 추출
    px, py = latlon_to_pixel(latitude, longitude, zoom, xtile, ytile)
    
    # 5. 빨간색 원 그리기 (반지름 8픽셀)
    r = 8
    # 원의 외곽선과 채우기를 모두 빨간색으로 지정
    draw.ellipse([px - r, py - r, px + r, py + r], fill=(255, 0, 0, 255), outline=(255, 0, 0, 255))
    
    # 중심점에 작은 하얀 점 점 하나 더 찍어서 조준점 효과 (선택 사항)
    draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255, 255))

    # 6. 저장
    output_filename = "wgs84_fixed_point.png"
    img.save(output_filename, "PNG")
    print(f"▶ 성공! 이미지가 정상적으로 생성되었습니다: {output_filename}")

# --- 실행 ---
# 예시: 서울시청 좌표
target_lat = 37.5665
target_lon = 126.9780

# zoom 레벨은 1~20까지 설정 가능합니다. (16 정도가 동네 수준으로 적당합니다)
generate_wgs84_png(target_lat, target_lon, zoom=16)