import math

import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="아폴로니우스 내분점 실험", page_icon="🔵", layout="centered")

st.title("🔵 아폴로니우스 내분점 실험")
st.markdown(
    "점 A와 B 좌표는 내부적으로 고정되어 있습니다. 아래에서 AP : PB 비율만 입력하세요."
)

st.header("입력 값")
ratio_text = st.text_input("AP : PB 비율 (m:n)", value="1:1")
ratio_m = 1.0
ratio_n = 1.0
try:
    parts = [part.strip() for part in ratio_text.split(":") if part.strip() != ""]
    if len(parts) != 2:
        raise ValueError
    ratio_m = float(parts[0])
    ratio_n = float(parts[1])
except ValueError:
    st.error("비율을 'm:n' 형식으로 입력하세요. 예: 2:3")
    st.stop()

if ratio_m == 0 and ratio_n == 0:
    st.error("m과 n 중 하나는 0이 아니어야 합니다.")
    st.stop()

st.markdown("---")
st.markdown(
    "### 사용 방법\n"
    "1. AP : PB 비율을 m:n 형태로 입력합니다.\n"
    "2. 계산된 내분점 P 좌표를 확인합니다.\n"
    "3. 수직선과 원으로 결과를 시각화합니다."
)

ax = 0.0
ay = 0.0
bx = 5.0
by = 0.0
px = (ratio_n * ax + ratio_m * bx) / (ratio_m + ratio_n)
py = (ratio_n * ay + ratio_m * by) / (ratio_m + ratio_n)

st.subheader("계산된 내분점")
st.write(f"P = ({px:.4f}, {py:.4f})")

st.markdown(
    "### 공식\n"
    "내분점 P의 좌표는 다음과 같습니다:\n"
    "$P = \left(\frac{nA_x + mB_x}{m+n},\ \frac{nA_y + mB_y}{m+n}\right)$\n"
    "\n\n"
    "여기서 AP:PB = m:n 입니다."
)

k = ratio_m / ratio_n if ratio_n != 0 else float("inf")

fig, ax_plot = plt.subplots(figsize=(4.5, 4.5))

# AB 선분 그리기 (실선, 검정)
ax_plot.plot([ax, bx], [ay, by], color="black", linewidth=3)

# A, B 점 표시
ax_plot.scatter([ax, bx], [ay, by], color="black", s=80, zorder=5)
ax_plot.text(ax, ay, " A", fontsize=12, verticalalignment="bottom", horizontalalignment="right")
ax_plot.text(bx, by, " B", fontsize=12, verticalalignment="bottom", horizontalalignment="left")

# 원 그리기
if ratio_n == 0:
    circle_center_x = bx
    circle_radius = 0.5
elif ratio_m == 0:
    circle_center_x = ax
    circle_radius = 0.5
elif math.isclose(k, 1.0):
    circle_center_x = (ax + bx) / 2
    circle_radius = abs(bx - ax) * 0.4
else:
    circle_center_x = (k**2 * bx) / (k**2 - 1)
    circle_radius = abs(k * (bx - ax) / (k**2 - 1))

circle = plt.Circle((circle_center_x, 0), circle_radius, edgecolor="red", fill=False, linewidth=2)
ax_plot.add_patch(circle)

# P 점 표시
ax_plot.scatter([px], [py], color="red", s=80, zorder=5)
ax_plot.text(px, py, " P", fontsize=12, verticalalignment="bottom")

# 간단한 범위 계산
margin = max(abs(bx - ax), circle_radius, 1) * 0.4
x_min = min(ax, bx, circle_center_x - circle_radius) - margin
x_max = max(ax, bx, circle_center_x + circle_radius) + margin
y_min = min(ay, by, py, -circle_radius) - margin
y_max = max(ay, by, py, circle_radius) + margin
ax_plot.set_xlim(x_min, x_max)
ax_plot.set_ylim(y_min, y_max)
ax_plot.axis("off")
ax_plot.set_aspect("equal", adjustable="box")

st.pyplot(fig)

if ratio_m > 0 and ratio_n > 0:
    st.success("수평선과 원으로 Apollonius 조건을 시각화했습니다.")
else:
    st.warning("비율이 0을 포함하면 P는 고정점 A 또는 B에 위치합니다.")
