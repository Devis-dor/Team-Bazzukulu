import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Team Bazzukulu", layout="centered")
st.title("Team Bazzukulu")

# --- STARTING DATA ---
if "bag" not in st.session_state:
    st.session_state.bag = 3000
if "is_chairman" not in st.session_state:
    st.session_state.is_chairman = False
if "notes" not in st.session_state:
    st.session_state.notes = []
if "members" not in st.session_state:
    st.session_state.members = [
        {"name":"Allan Kiwuuwa","pledged":0,"paid":0,"phone":"256707606020"},
        {"name":"Kamya and Benitah","pledged":0,"paid":0,"phone":"256781332245"},
        {"name":"Vivian Nantambi","pledged":0,"paid":0,"phone":"256758435710"},
        {"name":"Mirimu Charles","pledged":0,"paid":0,"phone":"256708903418"},
        {"name":"Kiyingi Vincent","pledged":0,"paid":0,"phone":"256703212072"},
        {"name":"Carol Nalubaale","pledged":0,"paid":0,"phone":"256760709833"},
        {"name":"Justine Nabbosa","pledged":0,"paid":0,"phone":"256755991596"},
        {"name":"Frank Namitala","pledged":0,"paid":0,"phone":"256785651960"},
        {"name":"Annet","pledged":0,"paid":0,"phone":"256708668959"},
        {"name":"Kizza Kenneth","pledged":0,"paid":0,"phone":"971558590787"},
        {"name":"Gloria","pledged":0,"paid":0,"phone":"27791540555"},
    ]

# --- CHAIRMAN LOGIN ---
st.subheader("Chairman Login")
password = st.text_input("Chairman password", type="password")
if st.button("Unlock Chairman"):
    if password == "Devisplendour9000..":
        st.session_state.is_chairman = True
        st.success("Chairman unlocked - you can edit now")
    else:
        st.error("Wrong password")

# --- CHAIRMAN'S BAG ---
st.subheader(f"Chairman's Bag (Starting Money): {st.session_state.bag}")
if st.session_state.is_chairman:
    amt = st.number_input("Amount for Bag", min_value=0, step=100)
    c1, c2 = st.columns(2)
    if c1.button("Add to Bag"):
        st.session_state.bag += amt
        st.rerun()
    if c2.button("Remove from Bag"):
        st.session_state.bag -= amt
        st.rerun()

# --- TOTALS ---
total_pledged = sum(m["pledged"] for m in st.session_state.members)
total_paid = sum(m["paid"] for m in st.session_state.members)
st.info(f"Total Pledged: {total_pledged} | Total Paid: {total_paid} | Remaining: {total_pledged - total_paid}")

if st.button("Refresh Now"):
    st.rerun()

# --- MEMBERS ---
st.subheader("Members - Paid Status")
for i, m in enumerate(st.session_state.members):
    if m["pledged"] > 0 and m["paid"] >= m["pledged"]:
        status = "✅ PAID"
    elif m["paid"] > 0:
        status = "🟡 PARTIAL"
    else:
        status = "🔴 NOT PAID"
    st.write(f"**{m['name']}** - {status}")
    st.write(f"Pledged: {m['pledged']} | Paid: {m['paid']} | Balance: {m['pledged'] - m['paid']}")
    st.link_button(f"WhatsApp {m['name']}", f"https://wa.me/{m['phone']}")
    if st.session_state.is_chairman:
        m["pledged"] = st.number_input(f"Pledged - {m['name']}", value=m["pledged"], key=f"p{i}")
        m["paid"] = st.number_input(f"Paid - {m['name']}", value=m["paid"], key=f"paid{i}")
    st.divider()

# --- NOTES - DROPDOWN + COMMENT + TIME ---
st.subheader("Record Note")
names = [m["name"] for m in st.session_state.members]
selected = st.selectbox("Pick member name", names)
comment = st.text_area("Write comment here...")
if st.button("Save Note"):
    if not comment:
        st.warning("Write comment first")
    else:
        time_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        st.session_state.notes.insert(0, {"name": selected, "text": comment, "time": time_now})
        st.success("Note saved")
        st.rerun()

st.subheader("All Notes")
for n in st.session_state.notes:
    st.write(f"**{n['name']}** - {n['time']}")
    st.write(n["text"])
    st.divider()
