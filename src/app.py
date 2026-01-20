import streamlit as st
import pandas as pd
import numpy as np

# 1. การตั้งค่าหน้ากระดาษแบบเป็นทางการ
st.set_page_config(
    page_title="HOSxP Data Analytics System",
    page_icon="🏥",
    layout="wide"
)

# ส่วนหัวของรายงาน
st.title("ระบบวิเคราะห์และเฝ้าระวังกลุ่มโรคไม่ติดต่อเรื้อรัง (NCDs)")
st.caption("ศูนย์ข้อมูลสารสนเทศโรงพยาบาล (Hospital Information Center)")
st.divider()

# 2. ส่วนควบคุมข้อมูล (Sidebar) - ออกแบบให้ดูสะอาดตา
with st.sidebar:
    st.header("ตัวเลือกการกรองข้อมูล")
    st.markdown("---")
    threshold = st.select_slider(
        "ระดับความดันโลหิตตัวบนที่เฝ้าระวัง (Systolic BP)",
        options=range(100, 201),
        value=140
    )
    st.markdown("---")
    st.write("**สถานะการเชื่อมต่อ:** ✅ ฐานข้อมูล HOSxP พร้อมใช้งาน")

# 3. ส่วนการคำนวณและเตรียมข้อมูล
@st.cache_data # ช่วยให้โหลดเร็วขึ้นเหมือนระบบมืออาชีพ
def load_data():
    sample_size = 1500
    df = pd.DataFrame({
        'HN': [f'{i:06d}' for i in range(1, sample_size + 1)],
        'ชื่อ-สกุล': [f'คนไข้ จำลอง {i}' for i in range(1, sample_size + 1)],
        'BPS': np.random.randint(90, 190, sample_size),
        'BPD': np.random.randint(60, 110, sample_size),
        'อายุ': np.random.randint(15, 90, sample_size),
        'สิทธิ์การรักษา': np.random.choice(['ชำระเงินเอง', 'บัตรทอง', 'ประกันสังคม', 'ข้าราชการ'], sample_size)
    })
    return df

df = load_data()
filtered_df = df[df['BPS'] >= threshold].sort_values('BPS', ascending=False)

# 4. ส่วนแสดงตัวชี้วัด (Key Performance Indicators - KPIs)
st.subheader("สรุปสถิติสำคัญ")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="จำนวนคนไข้ทั้งหมด", value=f"{len(df):,} ราย")
with kpi2:
    st.metric(label="กลุ่มที่เกินเกณฑ์ (Risk)", value=f"{len(filtered_df):,} ราย", delta=f"{(len(filtered_df)/len(df)*100):.1f}%")
with kpi3:
    st.metric(label="ค่าเฉลี่ย BPS", value=f"{filtered_df['BPS'].mean():.1f} mmHg")
with kpi4:
    st.metric(label="ค่าเฉลี่ยอายุกลุ่มเสี่ยง", value=f"{int(filtered_df['อายุ'].mean())} ปี")

st.markdown("---")

# 5. การแสดงผลข้อมูลเชิงลึก (Data Visualization)
col_left, col_right = st.columns([7, 3])

with col_left:
    st.subheader("กราฟแสดงระดับความดันแยกตามรายบุคคล (กลุ่มเสี่ยง)")
    # เปลี่ยนจาก Bar Chart เป็น Area Chart เพื่อความสวยงามและเป็นทางการ
    st.area_chart(filtered_df.set_index('HN')['BPS'])

with col_right:
    st.subheader("สัดส่วนสิทธิ์การรักษา")
    # แสดงสัดส่วนการเงิน
    insurance_counts = filtered_df['สิทธิ์การรักษา'].value_counts()
    st.bar_chart(insurance_counts)

# 6. ตารางข้อมูลรายละเอียด (Detailed Report)
st.subheader("บัญชีรายชื่อคนไข้กลุ่มเสี่ยง (Detailed Patient List)")
st.dataframe(
    filtered_df,
    use_container_width=True,
    column_config={
        "BPS": st.column_config.NumberColumn("ความดันตัวบน", format="%d mmHg"),
        "BPD": st.column_config.NumberColumn("ความดันตัวล่าง", format="%d mmHg"),
        "HN": st.column_config.TextColumn("เลขบัตรผู้ป่วย")
    },
    hide_index=True
)

# 7. ส่วนท้าย (Footer / Export)
st.download_button(
    label="📑 ส่งออกรายงานเป็นไฟล์ CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='hosxp_risk_report.csv',
    mime='text/csv',
)