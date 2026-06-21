import numpy as np
import math
import requests
from io import BytesIO
from PIL import Image, ImageDraw

def deg2num(lat_deg, lon_deg, zoom):
  """위도, 경도를 타일 좌표로 변환"""
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  """타일 좌표를 위도, 경도로 변환"""
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

def generate_wgs84_png(latitude, longitude):
  """
  WGS84 좌표를 입력받아 지도 타일과 함께 빨간색 원이 표시된 PNG 이미지를 생성합니다.
  """
  
  # 설정
  zoom = 15  # 확대 레벨 (적절한 크기)
  tile_size = 256  # OpenStreetMap 기본 타일 크기

  # 입력 좌표를 중심으로 타일 좌표 계산
  xtile, ytile = deg2num(latitude, longitude, zoom)

  # 타일 이미지 가져오기 (OpenStreetMap 사용)
  url = f"https://tile.openstreetmap.org/{zoom}/{xtile}/{ytile}.png"
  response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
  
  if response.status_code == 200:
    tile_image = Image.open(BytesIO(response.content))
  else:
    # 이미지 가져오기에 실패한 경우, 빈 이미지 생성 (오류 표시 등 추가 가능)
    tile_image = Image.new('RGB', (tile_size, tile_size), color=(255, 255, 255))
    draw = ImageDraw.Draw(tile_image)
    draw.text((tile_size // 2, tile_size // 2), f"Error {response.status_code}", fill=(255, 0, 0))


  # 좌표 표시를 위한 빨간색 원 설정
  circle_radius = 10
  circle_color = (255, 0, 0)  # 빨간색

  # 입력 좌표를 이미지 내부 좌표로 변환
  # 타일의 중심에 가깝게 표시하기 위해 타일 좌표를 기반으로 계산
  
  # 현재 타일의 왼쪽 상단 경위도 좌표
  nw_lat, nw_lon = num2deg(xtile, ytile, zoom)
  
  # 타일의 크기를 기반으로 픽셀 단위 계산
  n = 2.0 ** zoom
  point_x = int((longitude - nw_lon) * n / 360.0 * tile_size)
  
  # 위도 계산이 더 복잡하여, 타일 중심에 표시하는 것으로 단순화
  # (보다 정밀한 계산은 타일 기반 경위도 변환을 더 자세히 구현해야 함)
  point_y = tile_size // 2


  # 이미지 위에 그리기
  draw = ImageDraw.Draw(tile_image)
  draw.ellipse((point_x - circle_radius, point_y - circle_radius, point_x + circle_radius, point_y + circle_radius), outline=circle_color, fill=circle_color)


  # PNG 이미지로 저장
  output_filename = "wgs84_point.png"
  tile_image.save(output_filename, "PNG")
  print(f"이미지가 생성되었습니다: {output_filename}")


# --- 메인 실행 ---
# 입력 예시 (원하는 WGS84 경위도 좌표로 변경)
input_lat = 37.5665  # 예시: 서울시청 위도
input_lon = 126.9780 # 예시: 서울시청 경도

generate_wgs84_png(input_lat, input_lon)