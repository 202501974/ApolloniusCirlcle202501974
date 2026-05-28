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

if "ratio_text" not in st.session_state or st.session_state.ratio_text != ratio_text:
    st.session_state.ratio_text = ratio_text
    st.session_state.click_count = 0
    st.session_state.shown_angle_groups = []

if "click_count" not in st.session_state:
    st.session_state.click_count = 0
if "shown_angle_groups" not in st.session_state:
    st.session_state.shown_angle_groups = []

if st.button("원 위 점 4개 추가"):
    if st.session_state.click_count < 3:
        angle_groups = [
            [30, 60, 120, 150],
            [210, 240, 300, 330],
            [0, 90, 180, 270],
        ]
        st.session_state.shown_angle_groups.append(angle_groups[st.session_state.click_count])
        st.session_state.click_count += 1

st.write(f"클릭 횟수: {st.session_state.click_count} / 3")

ax = 0.0
ay = 0.0
bx = 1000.0
by = 0.0
px = (ratio_n * ax + ratio_m * bx) / (ratio_m + ratio_n)
py = (ratio_n * ay + ratio_m * by) / (ratio_m + ratio_n)

st.markdown(
    "### 공식\n"
    "내분점 P의 좌표는 다음과 같습니다:\n"
    "$P = \left(\frac{nA_x + mB_x}{m+n},\ \frac{nA_y + mB_y}{m+n}\right)$\n"
    "\n\n"
    "여기서 AP:PB = m:n 입니다."
)

# 입력한 비율에 따른 Apollonius 원 계산
if ratio_m != ratio_n:
    circle_center_x = (ratio_m**2 * bx - ratio_n**2 * ax) / (ratio_m**2 - ratio_n**2)
    circle_radius = abs(ratio_m * ratio_n * (bx - ax) / (ratio_m**2 - ratio_n**2))
else:
    circle_center_x = bx / 2
    circle_radius = abs(bx - ax) / 2

fig, ax_plot = plt.subplots(figsize=(4.5, 4.5))

# AB 선분 그리기 (실선, 검정)
ax_plot.plot([ax, bx], [ay, by], color="black", linewidth=3)

# A, B 점 표시
ax_plot.scatter([ax, bx], [ay, by], color="black", s=80, zorder=5)
ax_plot.text(ax, ay, " A", fontsize=12, verticalalignment="bottom", horizontalalignment="right")
ax_plot.text(bx, by, " B", fontsize=12, verticalalignment="bottom", horizontalalignment="left")

# 내분점과 외분점
ax_plot.scatter([px], [py], color="blue", s=80, zorder=5)
ax_plot.text(px, py, " P", fontsize=12, verticalalignment="bottom", horizontalalignment="center", color="blue")
if ratio_m != ratio_n:
    qx = (ratio_n * ax - ratio_m * bx) / (ratio_n - ratio_m)
    qy = 0.0
    ax_plot.scatter([qx], [qy], color="green", s=80, zorder=5)
    ax_plot.text(qx, qy, " Q", fontsize=12, verticalalignment="top", horizontalalignment="center", color="green")
else:
    qx = None

# 추가 점들 (입력한 비율에 따라 계산된 원 위)
for group in st.session_state.shown_angle_groups:
    for angle_deg in group:
        angle = math.radians(angle_deg)
        px_extra = circle_center_x + circle_radius * math.cos(angle)
        py_extra = circle_radius * math.sin(angle)
        ax_plot.scatter([px_extra], [py_extra], color="red", s=40, zorder=4)

show_circle = st.session_state.click_count >= 3
if show_circle:
    if ratio_m != ratio_n:
        circle = plt.Circle((circle_center_x, 0), circle_radius, edgecolor="red", fill=False, linewidth=2)
        ax_plot.add_patch(circle)
    else:
        ax_plot.axvline(bx / 2, color="red", linewidth=2)

# 간단한 범위 계산
margin = max(abs(bx - ax), circle_radius, 1) * 0.4
x_min = min(ax, bx, circle_center_x - circle_radius) - margin
x_max = max(ax, bx, circle_center_x + circle_radius) + margin
if ratio_m == ratio_n:
    y_min = -margin
    y_max = margin
else:
    y_min = min(ay, by, py, -circle_radius) - margin
    y_max = max(ay, by, py, circle_radius) + margin
ax_plot.set_xlim(x_min, x_max)
ax_plot.set_ylim(y_min, y_max)
ax_plot.axis("off")
ax_plot.set_aspect("equal", adjustable="box")

st.pyplot(fig)

if show_circle:
    st.success("3번 클릭 완료되었습니다. Apollonius 원이 표시됩니다.")
else:
    st.info("내분점과 외분점을 먼저 찾은 다음, 클릭으로 Apollonius 원 위의 점 4개씩 추가 표시됩니다.")
