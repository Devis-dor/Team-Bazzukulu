import streamlit as st
from datetime import date, timedelta
import urllib.parse
st.set_page_config(page_title="Team Bazzukulu Kiwuwa Family", page_icon="👨‍👩‍👧‍👦", layout="wide")
PARTY_DATE = date(2026, 12, 19)
CHAIRMAN_FEE = 3000
members_data = [("Allan", 100000),("Kiyingi Vincent", 450000),("Kizza Kenneth", 100000),("Gloria Nabweteme", 460000),("Charles Mirimu", 100000),("Vivian Nantambi", 250000),("Justine Nabbosa", 850000),("Frank Namitala", 400000),("Carol Nalubaale Butunda", 3000000),("Kamya and Benitah", 340000),("Annet", 50000),]
phones = {"Allan": "256707606020","Kiyingi Vincent": "256703212072","Kizza Kenneth": "971558590787","Gloria Nabweteme": "27791540555","Charles Mirimu": "256708903418","Vivian Nantambi": "256758435710","Justine Nabbosa": "256755991596","Frank Namitala": "256785651960","Carol Nalubaale Butunda": "256760709833","Kamya and Benitah": "256782332245","Annet": "256708668959",}
if "paid" not in st.session_state:
    st.session_state.paid = {name: 0 for name, _ in members_data}
if "attendance" not in st.session_state:
    st.session_state.attendance = {name: False for name, _ in members_data}
if "chairman_bag" not in st.session_state:
    st.session_state.chairman_bag = {name: False for name, _ in members_data}
if "minutes" not in st.session_state:
    st.session_state.minutes = [{"date": "2026-11-22", "speaker": "Kiyingi Vincent", "said": "Pledged to go and check the prices of rice", "pledged": "Yes - Rice check"},{"date": "2026-11-22", "speaker": "Nabbosa Justine", "said": "Urged the members to stay on track and not to lose the spirit", "pledged": "No"},]
st.title("Team Bazzukulu Kiwuwa Family")
st.subheader("Meeting, Pledge & Party Tracker")
today = date.today()
days_left = (PARTY_DATE - today).days
st.success(f"PARTY DAY: 19 Dec 2026 - {days_left} DAYS LEFT!")
days_to_sat = (5 - today.weekday()) % 7
if days_to_sat == 0:
    st.info("MEETING IS TODAY! Saturday Meeting Today!")
else:
    next_sat = today + timedelta(days=days_to_sat)
    st.info(f"Next Meeting: Saturday {next_sat.strftime('%d %b %Y')} - in {days_to_sat} days")
total_pledged = sum(p for _, p in members_data)
total_paid = sum(st.session_state.paid.values())
total_balance = total_pledged - total_paid
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Pledged", f"{total_pledged:,} UGX")
c2.metric("Total Paid", f"{total_paid:,} UGX")
c3.metric("Balance Left", f"{total_balance:,} UGX")
c4.metric("Members", len(members_data))
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Attendance", "Pledges & Payments", "Chairman's Bag", "Minutes", "Group Message", "Saturday Report"])
with tab1:
    st.header("Saturday Attendance")
    for name, _ in members_data:
        st.session_state.attendance[name] = st.checkbox(f"{name}", value=st.session_state.attendance[name], key=f"att_{name}")
    present = sum(1 for v in st.session_state.attendance.values() if v)
    st.write(f"Present: {present} / {len(members_data)}")
    if present == len(members_data):
        st.balloons()
        st.success("Everyone is present today!")
with tab2:
    st.header("Who Pledged & Who Paid?")
    for name, pledged in members_data:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1:
            st.write(f"**{name}**")
        with col2:
            st.write(f"Pledged: {pledged:,}")
        with col3:
            paid = st.number_input(f"Paid by {name}", min_value=0, max_value=pledged, value=st.session_state.paid[name], key=f"paid_{name}", label_visibility="collapsed")
            st.session_state.paid[name] = paid
        with col4:
            balance = pledged - paid
            phone = phones.get(name, "")
            if paid >= pledged and pledged > 0:
                st.success(f"CONGRATS {name}! PAID FULL!")
                msg = f"Hi {name}, CONGRATULATIONS! You have fully paid your pledge of {pledged:,} UGX for Team Bazzukulu Party! Thank you! Party Day 19 Dec 2026!"
                if phone:
                    link = f"https://wa.me/{phone}?text=" + urllib.parse.quote(msg)
                    st.markdown(f"[Send Congrats on WhatsApp]({link})")
            elif paid > 0:
                st.warning(f"Paid {paid:,} | Balance {balance:,}")
                msg = f"Hi {name}, Team Bazzukulu reminder: You pledged {pledged:,} UGX, you paid {paid:,} UGX, balance {balance:,} UGX. Please pay before 19 Dec 2026 party! Thank you."
                if phone:
                    link = f"https://wa.me/{phone}?text=" + urllib.parse.quote(msg)
                    st.markdown(f"[Send WhatsApp Reminder]({link})")
            else:
                st.error(f"Not Paid Yet | Balance {balance:,}")
                msg = f"Hi {name}, Team Bazzukulu reminder: You pledged {pledged:,} UGX, you have not paid yet. Please pay before 19 Dec 2026 party!"
                if phone:
                    link = f"https://wa.me/{phone}?text=" + urllib.parse.quote(msg)
                    st.markdown(f"[Send WhatsApp Reminder]({link})")
with tab3:
    st.header(f"Chairman's Bag - {CHAIRMAN_FEE:,} UGX Every Saturday")
    for name, _ in members_data:
        paid_bag = st.checkbox(f"{name} - Paid {CHAIRMAN_FEE:,}?", value=st.session_state.chairman_bag[name], key=f"bag_{name}")
        st.session_state.chairman_bag[name] = paid_bag
        if paid_bag:
            st.success(f"Thank you {name} for Chairman's Bag!")
    bag_total = sum(1 for v in st.session_state.chairman_bag.values() if v) * CHAIRMAN_FEE
    st.metric("Chairman's Bag Total Today", f"{bag_total:,} UGX")
with tab4:
    st.header("Meeting Minutes")
    st.subheader("Add New Minute")
    with st.form("minutes_form"):
        m_date = st.date_input("Meeting Date", value=today)
        speaker = st.selectbox("Speaker", [n for n, _ in members_data])
        said = st.text_area("What did they say?")
        pledged_q = st.selectbox("Did they pledge?", ["No", "Yes"])
        pledged_detail = st.text_input("If Yes, what did they pledge?")
        submit = st.form_submit_button("Save Minute")
        if submit:
            st.session_state.minutes.append({"date": str(m_date), "speaker": speaker, "said": said, "pledged": f"{pledged_q} - {pledged_detail}" if pledged_q=="Yes" else "No"})
            st.success("Minute Saved!")
            st.rerun()
    st.subheader("Previous Minutes by Date")
    dates = sorted(set(m["date"] for m in st.session_state.minutes), reverse=True)
    if dates:
        chosen = st.selectbox("Choose Date to View", dates)
        for m in st.session_state.minutes:
            if m["date"] == chosen:
                st.info(f"**{m['speaker']}** ({m['date']}): {m['said']} | Pledged? {m['pledged']}")
with tab5:
    st.header("Send Group Message to ALL Members")
    group_msg = st.text_area("Group Message", value=f"Hello Team Bazzukulu! Reminder: Next Meeting Saturday, Party Day 19 Dec 2026 - {days_left} days left. Please pay your pledges. Thank you!")
    st.write("Click each person, it opens their WhatsApp with your message. Press Send, then next person:")
    for name, _ in members_data:
        phone = phones.get(name, "")
        if phone:
            link = f"https://wa.me/{phone}?text=" + urllib.parse.quote(group_msg)
            st.markdown(f"Send to {name} - {link}")
        else:
            st.write(f"{name} - No number yet")
    st.info("Tip: Also create a WhatsApp Group 'Team Bazzukulu' and paste this same message there once!")
with tab6:
    st.header("Saturday Report")
    report_lines = []
    report_lines.append("TEAM BAZZUKULU KIWUWA FAMILY - SATURDAY REPORT")
    report_lines.append(f"Date: {today} | Party Day: 19 Dec 2026 ({days_left} days left)")
    report_lines.append(f"TOTAL PLEDGED: {total_pledged:,} UGX")
    report_lines.append(f"TOTAL PAID: {total_paid:,} UGX")
    report_lines.append(f"BALANCE: {total_balance:,} UGX")
    report_lines.append("MEMBERS:")
    for name, pledged in members_data:
        paid = st.session_state.paid[name]
        bal = pledged - paid
        att = "Present" if st.session_state.attendance[name] else "Absent"
        bag = "Paid Bag" if st.session_state.chairman_bag[name] else "No Bag"
        report_lines.append(f"- {name}: Pledged {pledged:,} | Paid {paid:,} | Balance {bal:,} | {att} | {bag}")
    report_lines.append("MINUTES:")
    for m in st.session_state.minutes:
        report_lines.append(f"- {m['date']} - {m['speaker']}: {m['said']} | Pledged? {m['pledged']}")
    report = "\n".join(report_lines)
    st.text_area("Report Preview", report, height=400)
    st.download_button("Download Report", data=report, file_name=f"Bazzukulu_Report_{today}.txt", mime="text/plain")
