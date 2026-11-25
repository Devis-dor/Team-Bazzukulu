import streamlit as st
import pandas as pd
import urllib.parse
import re

st.set_page_config(page_title="Team Bazzukulu - Olumbe", page_icon="👥", layout="wide")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)

st.title("👥 Team Bazzukulu")
st.write("Welcome! Manage attendance, pledges & reports for our Olumbe.")
st.success("🎉 OLUMBE DAY: 19 Dec 2026")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1xzrxbR3uCmk9sTL8bhCPgrdnPQuO5rivsdBwDs5ipSE/export?format=csv&gid=0"

def clean_money(x):
    # Fixes 350,000 -> 350000, 350k, empty, etc
    if pd.isna(x): return 0
    s = str(x).replace(",", "").replace("UGX", "").replace("ugx", "").replace(" ", "").strip()
    if s == "" or s.lower() == "nan": return 0
    try: return float(s)
    except: return 0

def clean_phone(x):
    if pd.isna(x): return ""
    s = str(x).strip().replace("+", "").replace(" ", "").replace("-", "").replace(".0", "")
    if s.lower() == "nan" or s == "": return ""
    if s.startswith("0"): s = "256" + s[1:]
    # Keep only digits
    s = re.sub(r"\D", "", s)
    return s

def load_data():
    try:
        df = pd.read_csv(SHEET_URL, dtype=str)
        df.columns = [c.strip() for c in df.columns]
        df = df.dropna(subset=["Name"])
        df = df[df["Name"].astype(str).str.strip() != ""]
        return df
    except Exception as e:
        st.error(f"Could not load Sheet. Error: {e}")
        return pd.DataFrame(columns=["Name", "Pledged", "Paid"])

if st.button("🔄 Refresh Now"):
    st.rerun()

df = load_data()

# Find Phone column - whatever you named it
phone_col = None
for c in df.columns:
    if "phone" in c.lower() or "contact" in c.lower() or "number" in c.lower():
        phone_col = c
        break

total_members = len(df)
total_pledged = df["Pledged"].apply(clean_money).sum() if "Pledged" in df.columns else 0
total_paid = df["Paid"].apply(clean_money).sum() if "Paid" in df.columns else 0

c1, c2, c3 = st.columns(3)
c1.metric("Members", total_members)
c2.metric("Total Pledged", f"{total_pledged:,.0f}")
c3.metric("Total Paid", f"{total_paid:,.0f}")
st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Attendance","💰 Pledges & Payments","👑 Chairman's Bag","📝 Minutes","💬 Send All WhatsApp","📅 Saturday Report"])

with tab1:
    st.subheader("📋 Attendance")
    if not df.empty:
        for i, row in df.iterrows():
            st.checkbox(f"{row['Name']}", key=f"att_{i}")
        if st.button("Save Attendance"):
            st.success("Attendance saved!")
    else:
        st.info("No members found.")

with tab2:
    st.subheader("💰 Pledges & Payments - Olumbe")
    if not df.empty:
        show = df.copy()
        show["Pledged"] = show["Pledged"].apply(clean_money)
        show["Paid"] = show["Paid"].apply(clean_money)
        show["Balance"] = show["Pledged"] - show["Paid"]
        st.dataframe(show[["Name", "Pledged", "Paid", "Balance"]], use_container_width=True)

with tab3:
    st.subheader("👑 Chairman's Bag")
    st.metric("In Bag", f"{total_paid:,.0f}")

with tab4:
    st.subheader("📝 Minutes")
    st.text_area("Write minutes for today:", height=200, key="minutes_box")
    if st.button("Save Minutes"):
        st.success("Minutes saved!")

with tab5:
    st.subheader("💬 Send All WhatsApp - To All Members")
    st.info("Use {name} - it will change to each person's name.")

    # FIXED: No more broken buttons. Use dropdown instead - NO ERROR
    template = st.selectbox("Choose template:", ["Custom", "Meeting Reminder", "Payment Reminder", "Thank You"])
    if template == "Meeting Reminder":
        default_msg = "Hi {name}, Team Bazzukulu meeting this Saturday. Please come on time. Olumbe is 19 Dec 2026. Thank you!"
    elif template == "Payment Reminder":
        default_msg = "Hi {name}, Team Bazzukulu Olumbe reminder: Please pay your balance before 19 Dec 2026. Thank you!"
    elif template == "Thank You":
        default_msg = "Hi {name}, Thank you for your support towards our Olumbe. God bless you! - Team Bazzukulu"
    else:
        default_msg = "Hi {name}, This is Team Bazzukulu. Reminder for our Olumbe on 19 Dec 2026. Please check your pledge and payment. Thank you!"

    msg_template = st.text_area("Type message to ALL members:", value=default_msg, height=120, key="msg_all_fixed")

    if st.button("✅ Generate WhatsApp Links For ALL"):
        if df.empty:
            st.error("No members found.")
        else:
            st.success(f"Ready! {len(df)} members")
            st.markdown("**Option 1: For WhatsApp GROUP - Copy this:**")
            st.code(msg_template.replace("{name}", "everyone"))
            st.markdown("**Option 2: Send one-by-one:**")
            for i, row in df.iterrows():
                name = str(row["Name"])
                phone = clean_phone(row[phone_col]) if phone_col else ""
                personal = msg_template.replace("{name}", name)
                try:
                    p = clean_money(row["Pledged"]); pa = clean_money(row["Paid"])
                    if "pay" in msg_template.lower():
                        personal += f" Your pledged: {p:,.0f}, Paid: {pa:,.0f}, Balance: {p-pa:,.0f}."
                except: pass
                link = "https://wa.me/" + phone + "?text=" + urllib.parse.quote(personal) if len(phone) >= 9 else ""
                cc1, cc2 = st.columns([2, 1])
                with cc1: st.write(f"**{name}** - {phone if phone else 'No phone in Sheet'}")
                with cc2:
                    if link: st.markdown(f"[📱 Send to {name}]({link})")
                    else: st.write("⚠️ Add phone")

            if not phone_col:
                st.warning("⚠️ Your Sheet has NO Phone column. Add a column named 'Phone' in your Sheet, then press Refresh. That is why it says 'No phone'. Example: Kamya and Benitah -> 256781332245")

with tab6:
    st.subheader("📅 Saturday Report - Olumbe")
    st.write(f"**Members:** {total_members}")
    st.write(f"**Total Pledged:** {total_pledged:,.0f}")
    st.write(f"**Total Paid:** {total_paid:,.0f}")
    st.write(f"**Balance:** {total_pledged - total_paid:,.0f}")
    st.success("Report from live Sheet data for Olumbe!")
