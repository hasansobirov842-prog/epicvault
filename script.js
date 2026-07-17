const tg = window.Telegram.WebApp;

tg.expand();

const buttons = document.querySelectorAll(".grid button");

buttons.forEach(button => {
    button.addEventListener("click", () => {

        const name = button.innerText;

        tg.HapticFeedback.impactOccurred("light");

        alert(name + " is coming soon!");

    });
});

const navButtons = document.querySelectorAll(".bottom-nav button");

navButtons.forEach(button => {
    button.addEventListener("click", () => {

        tg.HapticFeedback.selectionChanged();

    });
});
