import math

import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="아폴로니우스 내분점 실험", page_icon="🔵", layout="centered")

st.title("🔵 아폴로니우스 내분점 실험")
st.markdown(
    "아래에서 직접 숫자를 입력하여 점 A, 점 B, 그리고 AP:PB 비율을 설정하세요."
)

st.header("입력 값")
col1, col2 = st.columns(2)
with col1:
    ax = st.number_input("점 A x", value=0.0, step=0.5)
    ay = st.number_input("점 A y", value=0.0, step=0.5)
with col2:
    bx = st.number_input("점 B x", value=5.0, step=0.5)
    by = st.number_input("점 B y", value=0.0, step=0.5)

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
    "1. 점 A와 B 좌표를 각각 입력합니다.\n"
    "2. AP : PB 비율을 m:n 형태로 입력합니다.\n"
    "3. 계산된 내분점 P와 그래프를 확인합니다."
)

st.subheader("입력 결과")
st.write(f"- 점 A = ({ax:.2f}, {ay:.2f})")
st.write(f"- 점 B = ({bx:.2f}, {by:.2f})")
st.write(f"- AP : PB = {ratio_m:.2f} : {ratio_n:.2f}")

if ratio_m + ratio_n == 0:
    st.error("비율의 합이 0이 될 수 없습니다.")
else:
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

    fig, ax_plot = plt.subplots(figsize=(6, 6))
    ax_plot.plot([ax, bx], [ay, by], marker="o", color="#1f77b4", linewidth=2)
    ax_plot.scatter([px], [py], color="#ff7f0e", s=80, zorder=5)
    ax_plot.text(ax, ay, " A", fontsize=12, verticalalignment="bottom")
    ax_plot.text(bx, by, " B", fontsize=12, verticalalignment="bottom")
    ax_plot.text(px, py, " P", fontsize=12, verticalalignment="bottom")

    padding = max(abs(bx - ax), abs(by - ay), 1) * 0.25
    ax_plot.set_xlim(min(ax, bx) - padding, max(ax, bx) + padding)
    ax_plot.set_ylim(min(ay, by) - padding, max(ay, by) + padding)
    ax_plot.set_xlabel("x")
    ax_plot.set_ylabel("y")
    ax_plot.set_aspect("equal", adjustable="box")
    ax_plot.set_title("내분점 P 위치")
    ax_plot.grid(True, linestyle="--", alpha=0.4)

    st.pyplot(fig)

    if ratio_m > 0 and ratio_n > 0:
        st.success("내분점이 AB 선분 위에 올바르게 계산되었습니다.")
    else:
        st.warning("비율 중 하나가 0이면 점이 A 또는 B에 위치합니다.")
