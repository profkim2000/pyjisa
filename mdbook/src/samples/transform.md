# 좌표 변환

## Gemini에게 물어보기

---

**질문: espg:4326 좌표를 epsg:3857로 변환하는 파이썬 코드**

<br>

**gemini 답:**


파이썬에서 공간 데이터(좌표)의 좌표계를 변환할 때 가장 널리 쓰이는 라이브러리는 `pyproj`입니다.

만약 라이브러리가 설치되어 있지 않다면, 터미널에 `pip install pyproj`를 입력해 먼저 설치해 주세요.

---

### 🌐 EPSG:4326 ➔ EPSG:3857 변환 코드

위도·경도(EPSG:4326) 좌표를 미터 단위의 구면 메르카토르 프로젝션(EPSG:3857)으로 변환하는 코드입니다. 서울시청 좌표(위도 37.5665, 경도 126.9780)를 예시로 작성했습니다.

```python
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

```

---

### 💡 핵심 포인트 설명

* **`always_xy=True` 설정이 중요한 이유**:
전통적으로 GIS에서 EPSG:4326은 **(위도, 경도)** 즉, (Y, X) 순서로 다루어집니다. 반면 EPSG:3857은 평면 좌표계라 **(X, Y)** 순서를 씁니다. 순서가 뒤바뀌는 혼란을 막기 위해 `always_xy=True`를 주면 **두 좌표계 모두 (경도/X, 위도/Y) 순서로 통일**되어 직관적으로 코딩할 수 있습니다.
* **대량의 데이터 변환**:
만약 리스트나 넘파이(Numpy) 배열 형태로 여러 개의 좌표를 한 번에 넣어도 `transformer.transform(lon_list, lat_list)` 방식으로 매우 빠르게 일괄 변환이 가능합니다.

---

## 실행 화면

```powershell
PS E:\test\pyjisa> python transform.py
Traceback (most recent call last):
  File "E:\test\pyjisa\02.transform.py", line 1, in <module>
    from pyproj import Transformer
ModuleNotFoundError: No module named 'pyproj'
```

에러 발생. 맨 마지막 줄 "ModuleNotFoundError: No module named 'pyproj'" 가 그 원인이다. "pyproj" 라는 이름의 라이브러리가 없기 때문.

gemini가 대답 제일 첫 줄에 언급한 pyproj 라이브러리를 설치한다.

```
pip install proj
```

위 방법으로 라이브러리 설치하고 다시 실행하기

```powershell
PS E:\test\pyjisa> pip install pyproj
Collecting pyproj
  Downloading pyproj-3.7.1-cp310-cp310-win_amd64.whl.metadata (31 kB)
Collecting certifi (from pyproj)
  Downloading certifi-2026.6.17-py3-none-any.whl.metadata (2.5 kB)
Downloading pyproj-3.7.1-cp310-cp310-win_amd64.whl (6.3 MB)
   ---------------------------------------- 6.3/6.3 MB 7.9 MB/s  0:00:00
Downloading certifi-2026.6.17-py3-none-any.whl (133 kB)
Installing collected packages: certifi, pyproj
Successfully installed certifi-2026.6.17 pyproj-3.7.1



PS E:\test\pyjisa> python transform.py
--- 변환 결과 ---
None
원본 EPSG:4326 (위도, 경도): (37.5665, 126.978)
변환 EPSG:3857 (X, Y 미터): (14135126.30, 4518366.51)
PS E:\test\pyjisa>
```

프로그램이 이렇게 짧을 수 있는 건 pyproj에 이미 좌표변환과 관련된 모든 기능이 이미 만들어져 있기 때문.