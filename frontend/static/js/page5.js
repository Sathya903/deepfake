document.addEventListener("DOMContentLoaded", function () {

    const deepfake = JSON.parse(sessionStorage.getItem("deepfakeResult"));

    if (!deepfake) {
        document.body.innerHTML = "❌ Missing analysis data.";
        return;
    }

    const risk = deepfake.confidence;        // Fake probability %
    const confidence = 100 - risk;           // Real confidence %

    // ========================
    // BASIC INFO
    // ========================

    document.getElementById("confidenceScore").innerText =
        confidence + "%";

    document.getElementById("riskScore").innerText =
        risk + "%";

    document.getElementById("processingTime").innerText =
        deepfake.processing_time + " sec";

    document.getElementById("fileSize").innerText =
        deepfake.file_size;

    // ========================
    // MODEL BREAKDOWN
    // ========================

    const container = document.getElementById("modelBreakdownContainer");
    container.innerHTML = "";

    Object.entries(deepfake.model_breakdown).forEach(([name, value]) => {

        const barHTML = `
            <div class="bar">
                <label>${name} (${value}%)</label>
                <div class="bar-bg">
                    <div class="bar-fill" style="width:${value}%"></div>
                </div>
            </div>
        `;

        container.innerHTML += barHTML;
    });

    // ========================
    // TECHNIQUES USED
    // ========================

    const techniquesList = document.getElementById("techniquesList");
    techniquesList.innerHTML = "";

    Object.keys(deepfake.model_breakdown).forEach(name => {
        const li = document.createElement("li");
        li.innerText = name;
        techniquesList.appendChild(li);
    });

    // ========================
    // FINAL VERDICT
    // ========================

    let verdict;
    let color;
    let recommendation;

    if (risk >= 70) {
        verdict = "❌ HIGH RISK – LIKELY DEEPFAKE";
        color = "#ff4d4d";
        recommendation = "Avoid sharing this media. Verify with trusted sources before distribution.";
    } 
    else if (risk >= 40) {
        verdict = "⚠ SUSPICIOUS MEDIA";
        color = "#ffd166";
        recommendation = "Cross-check the media source. Consider manual verification.";
    } 
    else {
        verdict = "✅ AUTHENTIC MEDIA";
        color = "#00ff9d";
        recommendation = "Media appears authentic based on AI analysis.";
    }

    const verdictEl = document.getElementById("finalVerdict");
    verdictEl.innerText = verdict;
    verdictEl.style.color = color;

    document.getElementById("recommendation").innerText =
        recommendation;
});
