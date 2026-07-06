<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EpicVault</title>
<link rel="stylesheet" href="style.css">
</head>

<body>

<div class="top">
<div class="logo">🎮 EPIC VAULT</div>

<div class="balance">
<div class="card">
<p>Balance</p>
<h2>0 ⭐</h2>
</div>

<div class="card purple">
<p>Wallet</p>
<h2>TON</h2>
</div>
</div>
</div>

<div class="banner">
<h1>OPEN CASES</h1>
<p>Win Stars • TON • Gifts</p>
<button class="play">PLAY NOW</button>
</div>

<div class="grid">

<div class="item">
<div class="icon">🎁</div>
<h3>Free Cases</h3>
</div>

<div class="item">
<div class="icon">💎</div>
<h3>Premium Cases</h3>
</div>

<div class="item">
<div class="icon">⭐</div>
<h3>Buy Stars</h3>
</div>

<div class="item">
<div class="icon">💰</div>
<h3>Wallet</h3>
</div>

<div class="item">
<div class="icon">👥</div>
<h3>Referrals</h3>
</div>

<div class="item">
<div class="icon">🎯</div>
<h3>Tasks</h3>
</div>

<div class="item">
<div class="icon">🏆</div>
<h3>Leaderboard</h3>
</div>

<div class="item">
<div class="icon">⚙️</div>
<h3>Settings</h3>
</div>

</div>

<div class="bottom">
<button>🏠 Home</button>
<button>🎁 Cases</button>
<button>👤 Profile</button>
</div>

<style>
body {
  margin: 0;
  font-family: Arial;
  background: #0f0f0f;
  color: white;
}

.page {
  padding-bottom: 80px;
}

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
  font-size: 13px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  transition: 0.2s;
}

.bottom button.active {
  color: #00ffc8;
  transform: scale(1.1);
}
</style>

<div class="page">
  <div id="home">🏠 Home</div>
  <div id="cases" style="display:none">🎁 Cases</div>
  <div id="stars" style="display:none">⭐ Stars</div>
  <div id="profile" style="display:none">👤 Profile</div>
</div>

<div class="bottom">
  <button class="active" onclick="go(this,'home')">🏠<span>Home</span></button>
  <button onclick="go(this,'cases')">🎁<span>Cases</span></button>
  <button onclick="go(this,'stars')">⭐<span>Stars</span></button>
  <button onclick="go(this,'profile')">👤<span>Profile</span></button>
</div>

<script>
function go(btn,page){
  document.querySelectorAll(".page > div").forEach(e => e.style.display="none");
  document.getElementById(page).style.display="block";

  document.querySelectorAll(".bottom button").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}
</script>

