document.addEventListener("DOMContentLoaded", function () {

    const deepfake = JSON.parse(sessionStorage.getItem("deepfakeResult"));

    if (!deepfake) {
        document.body.innerHTML = "❌ Missing analysis data.";
        return;
    }

    const risk = deepfake.confidence;
    const confidence = 100 - risk;

    // Basic values
    document.getElementById("confidenceScore").innerText = confidence + "%";
    document.getElementById("riskScore").innerText = risk + "%";
    document.getElementById("processingTime").innerText =
        deepfake.processing_time + " sec";
    document.getElementById("fileSize").innerText =
        deepfake.file_size + " MB";

    document.getElementById("confidenceBar").style.width = confidence + "%";
    document.getElementById("riskBar").style.width = risk + "%";

    const resultBox = document.getElementById("resultBox");
    const statusIcon = document.getElementById("statusIcon");
    const verdictEl = document.getElementById("finalVerdict");
    
    // Instead of innerHTML, we can create <li> elements for better security and styling
    recommendList.innerHTML = "";
    const recommendations = [];

    if (risk >= 70) {
        verdictEl.innerText = "Deepfake Detected";
        resultBox.style.background = "rgba(255,0,0,0.1)";
        resultBox.style.borderColor = "#ff4d4d";
        statusIcon.style.background = "#ff4d4d";
        document.getElementById("riskBar").style.background = "linear-gradient(90deg,#ff4d4d,#ff8800)";
        recommendations.push(
            "Do not share this media",
            "Report to platform moderators",
            "Verify through trusted sources",
            "Consider forensic analysis"
        );
    } else if (risk >= 40) {
        verdictEl.innerText = "Suspicious Media";
        resultBox.style.background = "rgba(255,200,0,0.1)";
        resultBox.style.borderColor = "#ffd166";
        statusIcon.style.background = "#ffd166";
        document.getElementById("riskBar").style.background = "#ffd166";
        recommendations.push(
            "Cross-check original source",
            "Perform manual verification",
            "Avoid immediate distribution"
        );
    } else {
        verdictEl.innerText = "Authentic Media";
        resultBox.style.background = "rgba(0,255,150,0.1)";
        resultBox.style.borderColor = "#00ff9d";
        statusIcon.style.background = "#00ff9d";
        document.getElementById("riskBar").style.background = "#00ff9d";
        recommendations.push(
            "Media appears authentic",
            "No manipulation patterns detected",
            "Safe for general distribution"
        );
    }

// Append recommendations dynamically
    recommendList.innerHTML = "";  // clear
    recommendations.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        recommendList.appendChild(li);
    });

    // Detection metrics
    const container = document.getElementById("modelBreakdownContainer");
    container.innerHTML = "";

    Object.entries(deepfake.model_breakdown).forEach(([name, value]) => {
        container.innerHTML += `
            <div style="margin:15px 0">
                <div style="display:flex;justify-content:space-between">
                    <span>${name}</span>
                    <span>${value}%</span>
                </div>
                <div class="progress">
                    <div class="progress-fill" style="width:${value}%; background:${risk>=70?'#ff4d4d':'#00ff9d'}"></div>
                </div>
            </div>
        `;
    });

    // Techniques
    const techniquesList = document.getElementById("techniquesList");
    Object.keys(deepfake.model_breakdown).forEach(name => {
        techniquesList.innerHTML += `<div>${name}</div>`;
    });

});