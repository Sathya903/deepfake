document.addEventListener("DOMContentLoaded", async function () {

    const progressFill = document.getElementById("progressFill");
    const progressText = document.getElementById("progressText");
    const modelsDiv = document.getElementById("models");

    let progress = 0;

    const interval = setInterval(() => {

        progress += 4;
        progressFill.style.width = progress + "%";
        progressFill.innerText = progress + "%";

        if (progress < 30)
            progressText.innerText = "Loading CNN Model...";
        else if (progress < 60)
            progressText.innerText = "Running Frequency Analysis...";
        else if (progress < 85)
            progressText.innerText = "Analyzing Facial Landmarks...";
        else
            progressText.innerText = "Fusing Results...";

        if (progress >= 100) {
            clearInterval(interval);
            runDeepfakeCheck();
        }

    }, 100);

    async function runDeepfakeCheck() {

    try {
        console.log("Calling deepfake API...");

        const response = await fetch("/deepfake", {
            method: "POST"
        });

        const result = await response.json();

        console.log("Deepfake response:", result);

        if (result.error) {
            progressText.innerText = result.error;
            return;
        }

        sessionStorage.setItem("deepfakeResult", JSON.stringify(result));

        window.location.href = "/page5";

    } catch (err) {
        console.error("Deepfake error:", err);
        progressText.innerText = "❌ Deepfake engine failed.";
    }
}

});