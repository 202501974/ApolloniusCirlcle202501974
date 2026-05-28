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
    "2. 계산된 내분점 P 좌표를 확인합니다."
)

ax = 0.0
ay = 0.0
bx = 5.0
by = 0.0

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

    if ratio_m > 0 and ratio_n > 0:
        st.success("내분점이 AB 선분 위에 올바르게 계산되었습니다.")
    else:
        st.warning("비율 중 하나가 0이면 점이 A 또는 B에 위치합니다.")
