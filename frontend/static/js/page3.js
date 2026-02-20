document.addEventListener("DOMContentLoaded", function () {

    const checksDiv = document.getElementById("checks");
    const finalStatus = document.getElementById("finalStatus");
    const deepfakeBtn = document.getElementById("deepfakeBtn");

    console.log("Page3 Loaded");

    const stored = sessionStorage.getItem("authResult");

    if (!stored) {
        finalStatus.innerHTML = "❌ No authentication result found.";
        deepfakeBtn.style.display = "none";
        return;
    }

    const result = JSON.parse(stored);
    
    checksDiv.innerHTML = "";

    result.checks.forEach(check => {

        const div = document.createElement("div");
        div.className = "check";

        if (check.status === "GREEN") {
            div.classList.add("green");
            div.innerHTML = `<strong>${check.name}</strong><br>✔ ${check.message}`;
        }
        else if (check.status === "YELLOW") {
            div.classList.add("yellow");
            div.innerHTML = `<strong>${check.name}</strong><br>⚠ ${check.message}`;
        }
        else {
            div.classList.add("red");
            div.innerHTML = `<strong>${check.name}</strong><br>❌ ${check.message}`;
        }

        checksDiv.appendChild(div);
    });

    let score = result.deepfake_score || 0;

    let level;
    if (score >= 75) {
        level = "Likely Deepfake";
    } 
    else if (score >= 40) {
        level = "Suspicious";
    }
    else {
        level = "Authentic";
    }

    


    // 🔥 Debug click
    deepfakeBtn.addEventListener("click", function () {
        console.log("Button clicked");
        window.location.href = "/page4";
    });

});
