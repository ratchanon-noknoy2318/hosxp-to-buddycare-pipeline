from datetime import datetime
from linebot import LineBotApi
from linebot.models import TextSendMessage

# ใส่ Token เดิมของคุณ
LINE_ACCESS_TOKEN = 'LINE_ACCESS_TOKEN'
USER_ID = 'USER_ID'

def test_empty_report():
    # ---- [ จุดที่เปลี่ยน ] ----
    # สร้าง List ว่างเปล่า (จำลองว่าไม่มีข้อมูล)
    rows = []
    
    yesterday = datetime.now().strftime('%Y-%m-%d')

    # ส่วนประมวลผลข้อความ (เหมือนเดิมเป๊ะ)
    if rows:
        report_msg = f"📊 [TEST] รายงานสรุปผู้ป่วยวันที่ {yesterday}\n"
        report_msg += "--------------------------\n"
        total_all = 0
        for row in rows:
            report_msg += f"🔹 {row['clinic_name']}: {row['total']} คน\n"
            total_all += row['total']
            
        report_msg += "--------------------------\n"
        report_msg += f"✅ รวมทั้งสิ้น: {total_all} คน"
    else:
        # ระบบจะวิ่งมาที่นี่ถ้า rows ว่างเปล่า
        report_msg = f"⚠️ [EMPTY TEST] วันที่ {yesterday}\nไม่พบข้อมูลผู้ป่วยในระบบ หรือไม่มีการรับบริการ"

    # พิมพ์ดูหน้าตา
    print("--- Preview Message (Empty Case) ---")
    print(report_msg)
    
    # ส่งเข้า Line
    try:
        line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
        line_bot_api.push_message(USER_ID, TextSendMessage(text=report_msg))
        print("✅ Line Notification Sent (Empty Case)!")
    except Exception as e:
        print(f"❌ Line Error: {e}")

if __name__ == "__main__":
    test_empty_report()
