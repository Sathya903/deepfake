document.addEventListener("DOMContentLoaded", function () {

    const auth = JSON.parse(sessionStorage.getItem("authResult"));
    const deepfake = JSON.parse(sessionStorage.getItem("deepfakeResult"));

    if (!auth || !deepfake) {
        document.body.innerHTML = "❌ Missing analysis data.";
        return;
    }

    document.getElementById("authScore").innerText =
        auth.total_score + "%";

    document.getElementById("deepfakeScore").innerText =
        deepfake.deepfake_score + "%";

    document.getElementById("cnnBar").style.width =
        deepfake.methods.cnn + "%";

    document.getElementById("freqBar").style.width =
        deepfake.methods.frequency + "%";

    document.getElementById("landmarkBar").style.width =
        deepfake.methods.landmark + "%";

    let finalScore =
        (0.4 * auth.total_score) +
        (0.6 * (100 - deepfake.deepfake_score));

    let verdict;
    let color;

    if (finalScore >= 80) {
        verdict = "✅ TRUSTED MEDIA";
        color = "#00ff9d";
    } else if (finalScore >= 50) {
        verdict = "⚠ SUSPICIOUS MEDIA";
        color = "#ffd166";
    } else {
        verdict = "❌ HIGH RISK – LIKELY DEEPFAKE";
        color = "#ff4d4d";
    }

    const verdictEl = document.getElementById("finalVerdict");
    verdictEl.innerText = verdict;
    verdictEl.style.color = color;
});
