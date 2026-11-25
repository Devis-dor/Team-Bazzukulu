<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Team Bazzukulu</title>
<style>
body{font-family:Arial;padding:12px;background:#f5f5f5}
.card{background:#fff;padding:14px;border-radius:12px;margin-bottom:12px}
button{padding:10px 14px;border-radius:8px;border:0;background:#111;color:#fff;font-weight:bold}
input,select,textarea{width:100%;padding:10px;margin:6px 0;border:1px solid #ddd;border-radius:8px}
.paid{color:green;font-weight:bold}.partial{color:orange;font-weight:bold}.notpaid{color:red;font-weight:bold}
.note{border-bottom:1px solid #eee;padding:8px 0}
</style>
</head>
<body>
<h2>Team Bazzukulu</h2>

<div class="card">
<b>Chairman Login</b>
<input id="pass" type="password" placeholder="Chairman password">
<button onclick="login()">Unlock Chairman</button>
<p id="loginMsg"></p>
</div>

<div class="card">
<b>Chairman's Bag (Starting Money): <span id="bag">3000</span></b><br>
<span id="chairOnly" style="display:none">
<input id="bagAmt" type="number" placeholder="Amount">
<button onclick="addBag()">Add to Bag</button>
<button onclick="removeBag()">Remove from Bag</button>
</span>
</div>

<div class="card">
<b>Total Pledged:</b> <span id="tPledged">0</span> |
<b>Total Paid:</b> <span id="tPaid">0</span> |
<b>Remaining:</b> <span id="tRem">0</span><br>
<button onclick="refresh()">Refresh Now</button>
</div>

<div class="card"><h3>Members</h3><div id="members"></div></div>

<div class="card">
<h3>Record Note</h3>
<select id="noteName"></select>
<textarea id="noteText" placeholder="Write comment here..."></textarea>
<button onclick="saveNote()">Save Note</button>
<div id="notesList"></div>
</div>

<script>
let members=[
{name:"Allan Kiwuuwa",pledged:0,paid:0,phone:"256707606020"},
{name:"Kamya and Benitah",pledged:0,paid:0,phone:"256781332245"},
{name:"Vivian Nantambi",pledged:0,paid:0,phone:"256758435710"},
{name:"Mirimu Charles",pledged:0,paid:0,phone:"256708903418"},
{name:"Kiyingi Vincent",pledged:0,paid:0,phone:"256703212072"},
{name:"Carol Nalubaale",pledged:0,paid:0,phone:"256760709833"},
{name:"Justine Nabbosa",pledged:0,paid:0,phone:"256755991596"},
{name:"Frank Namitala",pledged:0,paid:0,phone:"256785651960"},
{name:"Annet",pledged:0,paid:0,phone:"256708668959"},
{name:"Kizza Kenneth",pledged:0,paid:0,phone:"971558590787"},
{name:"Gloria",pledged:0,paid:0,phone:"27791540555"},
];
let bag=3000;
let isChairman=false;
let notes=JSON.parse(localStorage.getItem("bazz_notes")||"[]");

function login(){
  if(document.getElementById("pass").value==="Devisplendour9000.."){
    isChairman=true;
    document.getElementById("loginMsg").innerText="Chairman unlocked - you can edit now";
    document.getElementById("chairOnly").style.display="block";
  } else { alert("Wrong password"); }
  render();
}
function addBag(){ bag+=Number(document.getElementById("bagAmt").value||0); render(); }
function removeBag(){ bag-=Number(document.getElementById("bagAmt").value||0); render(); }

function status(m){
  if(m.paid>=m.pledged && m.pledged>0) return '<span class="paid">PAID</span>';
  if(m.paid>0) return '<span class="partial">PARTIAL</span>';
  return '<span class="notpaid">NOT PAID</span>';
}
function render(){
  document.getElementById("bag").innerText=bag;
  let tp=0, tpaid=0, html="", opts="";
  members.forEach((m,i)=>{
    tp+=m.pledged; tpaid+=m.paid;
    html+=`<div style="border-bottom:1px solid #eee;padding:8px 0"><b>${m.name}</b> - ${status(m)}<br>Pledged: ${m.pledged} | Paid: ${m.paid} | Balance: ${m.pledged-m.paid}<br><a href="https://wa.me/${m.phone}">WhatsApp ${m.name}</a> ${isChairman?`<br><input type="number" placeholder="Pledged" onchange="members[${i}].pledged=Number(this.value);render()"> <input type="number" placeholder="Paid" onchange="members[${i}].paid=Number(this.value);render()">`:""}</div>`;
    opts+=`<option>${m.name}</option>`;
  });
  document.getElementById("members").innerHTML=html;
  document.getElementById("noteName").innerHTML=opts;
  document.getElementById("tPledged").innerText=tp;
  document.getElementById("tPaid").innerText=tpaid;
  document.getElementById("tRem").innerText=tp-tpaid;
  document.getElementById("notesList").innerHTML=notes.map(n=>`<div class="note"><b>${n.name}</b> <small>${n.time}</small><br>${n.text}</div>`).join("");
}
function refresh(){ render(); }
function saveNote(){
  let name=document.getElementById("noteName").value;
  let text=document.getElementById("noteText").value;
  if(!text) return alert("Write comment first");
  let time=new Date().toLocaleString();
  notes.unshift({name,text,time});
  localStorage.setItem("bazz_notes",JSON.stringify(notes));
  document.getElementById("noteText").value="";
  render();
}
render();
</script>
</body>
</html>
