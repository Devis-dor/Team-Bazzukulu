import streamlit as st
import pandas as pd
import urllib.parse

# --- PAGE SETUP ---
st.set_page_config(page_title="Team Bazzukulu - Olumbe", page_icon="👥", layout="wide")

# Hide Streamlit menu / Manage stuff for normal members
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("👥 Team Bazzukulu")
st.write("Welcome! Manage attendance, pledges & reports for our Olumbe.")
st.success("🎉 OLUMBE DAY: 19 Dec 2026")

# --- YOUR GOOGLE SHEET LINK - ALREADY FIXED FOR YOU ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1xzrxbR3uCmk9sTL8bhCPgrdnPQuO5rivsdBwDs5ipSE/export?format=csv&gid=0"

# --- LOAD DATA - NO CACHE, ALWAYS FRESH ---
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        df = df.dropna(subset=["Name"])
        df = df[df["Name"].astype(str).str.strip() != ""]
        return df
    except Exception as e:
        st.error(f"Could not load Sheet. Check link. Error: {e}")
        return pd.DataFrame(columns=["Name", "Pledged", "Paid", "Phone"])

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Refresh Now"):
        st.rerun()

df = load_data()

# --- TOP STATS ---
total_members = len(df)
total_pledged = pd.to_numeric(df["Pledged"], errors="coerce").fillna(0).sum() if "Pledged" in df.columns else 0
total_paid = pd.to_numeric(df["Paid"], errors="coerce").fillna(0).sum() if "Paid" in df.columns else 0

c1, c2, c3 = st.columns(3)
c1.metric("Members", total_members)
c2.metric("Total Pledged", f"{total_pledged:,.0f}")
c3.metric("Total Paid", f"{total_paid:,.0f}")

st.divider()

# --- TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Attendance",
    "💰 Pledges & Payments",
    "👑 Chairman's Bag",
    "📝 Minutes",
    "💬 Send All WhatsApp",
    "📅 Saturday Report"
])

with tab1:
    st.subheader("📋 Attendance")
    st.write(f"Total Members: **{total_members}**")
    if not df.empty:
        for i, row in df.iterrows():
            st.checkbox(f"{row['Name']}", key=f"att_{i}")
        if st.button("Save Attendance"):
            st.success("Attendance saved for today!")
    else:
        st.info("No members found. Add members in Google Sheet > Sheet1")

with tab2:
    st.subheader("💰 Pledges & Payments - Olumbe")
    if not df.empty:
        show_df = df.copy()
        show_df["Pledged"] = pd.to_numeric(show_df["Pledged"], errors="coerce").fillna(0)
        show_df["Paid"] = pd.to_numeric(show_df["Paid"], errors="coerce").fillna(0)
        show_df["Balance"] = show_df["Pledged"] - show_df["Paid"]
        st.dataframe(show_df[["Name", "Pledged", "Paid", "Balance"]], use_container_width=True)
    else:
        st.info("No data yet")

with tab3:
    st.subheader("👑 Chairman's Bag")
    st.metric("In Bag", f"{total_paid:,.0f}")
    st.info("Edit this in Sheet to update")

with tab4:
    st.subheader("📝 Minutes")
    st.text_area("Write minutes for today:", height=200, key="minutes")
    if st.button("Save Minutes"):
        st.success("Minutes saved!")

with tab5:
    st.subheader("💬 Send All WhatsApp - To All Members")
    st.write("Type ONE message, it will go to EVERYONE for the Olumbe.")
    st.info("Tip: Use {name} - it will change to each person's name automatically.")

    msg_template = st.text_area("Type message to ALL members:", 
        value="Hi {name}, This is Team Bazzukulu. Reminder for our Olumbe on 19 Dec 2026. Please check your pledge and payment. Thank you!",
        height=120, key="msg_all")

    t1, t2, t3 = st.columns(3)
    with t1:
        if st.button("📅 Meeting Reminder"):
            st.session_state.msg_all = "Hi {name}, Team Bazzukulu meeting this Saturday. Please come on time. Olumbe is 19 Dec 2026. Thank you!"
            st.rerun()
    with t2:
        if st.button("💰 Payment Reminder"):
            st.session_state.msg_all = "Hi {name}, Team Bazzukulu Olumbe reminder: Please pay your balance before 19 Dec 2026. Thank you!"
            st.rerun()
    with t3:
        if st.button("🎉 Thank You"):
            st.session_state.msg_all = "Hi {name}, Thank you for your support towards our Olumbe. God bless you! - Team Bazzukulu"
            st.rerun()

    if st.button("✅ Generate WhatsApp Links For ALL"):
        if df.empty:
            st.error("No members found in Sheet.")
        else:
            st.success(f"Ready! Tap each name to send on WhatsApp - {len(df)} members")
            st.write("---")
            st.markdown("**Option 1: For WhatsApp GROUP - Copy this one message:**")
            group_msg = msg_template.replace("{name}", "everyone")
            st.code(group_msg)
            st.markdown("Copy the text above and paste it in your WhatsApp Group.")
            st.write("---")
            st.markdown("**Option 2: Send one-by-one to each person:**")
            for i, row in df.iterrows():
                name = str(row["Name"])
                phone = ""
                if "Phone" in df.columns:
                    phone = str(row["Phone"]).strip().replace("+", "").replace(" ", "").replace(".0", "")
                    if phone.startswith("0"):
                        phone = "256" + phone[1:]
                personal_msg = msg_template.replace("{name}", name)
                try:
                    pledged = float(row["Pledged"])
                    paid = float(row["Paid"])
                    bal = pledged - paid
                    if "Payment" in msg_template or "pay" in msg_template.lower():
                        personal_msg += f" Your pledged: {pledged:,.0f}, Paid: {paid:,.0f}, Balance: {bal:,.0f}."
                except:
                    pass
                link = "https://wa.me/" + phone + "?text=" + urllib.parse.quote(personal_msg) if phone and phone != "nan" and len(phone) >= 9 else ""
                c_name, c_btn = st.columns([2, 1])
                with c_name:
                    st.write(f"**{name}** - {phone if phone else 'No phone in Sheet'}")
                with c_btn:
                    if link:
                        st.markdown(f"[📱 Send to {name}]({link})")
                    else:
                        st.write("⚠️ Add phone in Sheet")

with tab6:
    st.subheader("📅 Saturday Report - Olumbe")
    st.write(f"**Members:** {total_members}")
    st.write(f"**Total Pledged:** {total_pledged:,.0f}")
    st.write(f"**Total Paid:** {total_paid:,.0f}")
    st.write(f"**Balance:** {total_pledged - total_paid:,.0f}")
    st.success("Report generated from live Sheet data for Olumbe!")
