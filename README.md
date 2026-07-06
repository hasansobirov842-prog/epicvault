<!DOCTYPE html>
<html>
<head>
<title>EpicVault</title>

<style>
body {
  margin: 0;
  font-family: Arial;
  background: #0f0f0f;
  color: white;
}

/* PAGE */
.page {
  padding: 20px;
  padding-bottom: 90px;
}

/* CARD */
.card {
  background: #1a1a1a;
  padding: 12px;
  margin: 10px 0;
  border-radius: 12px;
}

/* BOTTOM MENU */
.bottom {
  position: fixed;
  bottom: 15px;
  left: 10px;
  right: 10px;
  background: #1a1a1a;
  border-radius: 20px;
  display: flex;
  justify-content: space-around;
  padding: 10px 5px;
  box-shadow: 0 0 20px rgba(0,255,200,0.15);
}

.bottom button {
  background: none;
  border: none;
  color: #aaa;
  font-size: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bottom button.active {
  color: #00ffc8;
  transform: scale(1.1);
}
</style>
</head>

<body>

<!-- HOME -->
<div id="home" class="page">
  <h2>🎮 EPIC VAULT</h2>

  <div class="card">💰 Balance: 0 ⭐</div>
  <div class="card">Wallet: TON</div>
  <div class="card">🔥 OPEN CASES</div>
  <div class="card">Win Stars • TON • Gifts</div>
  <div class="card">🚀 PLAY NOW</div>

  <div class="card">🎁 Free Cases</div>
  <div class="card">💎 Premium Cases</div>
  <div class="card">⭐ Buy Stars</div>
  <div class="card">💰 Wallet</div>
  <div class="card">👥 Referrals</div>
  <div class="card">🎯 Tasks</div>
  <div class="card">🏆 Leaderboard</div>
  <div class="card">⚙️ Settings</div>
</div>

<!-- CASES -->
<div id="cases" class="page" style="display:none">
  <h2>🎁 Cases</h2>

  <div class="card">Free Case</div>
  <div class="card">Premium Case</div>
</div>

<!-- PROFILE -->
<div id="profile" class="page" style="display:none">
  <h2>👤 Profile</h2>

  <div class="card">User: EpicVault Player</div>
</div>

<!-- BOTTOM MENU -->
<div class="bottom">
  <button class="active" onclick="go(this,'home')">🏠 Home</button>
  <button onclick="go(this,'cases')">🎁 Cases</button>
  <button onclick="go(this,'profile')">👤 Profile</button>
</div>

<script>
function go(btn, page){
  document.querySelectorAll(".page").forEach(p => p.style.display = "none");
  document.getElementById(page).style.display = "block";

  document.querySelectorAll(".bottom button").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}
</script>

</body>
</html>
