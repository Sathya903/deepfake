function handleFile(input, type) {
    const file = input.files[0];
    if (!file) return;

    // Store file globally
    window.selectedFile = file;

    document.getElementById("selectedFile").style.display = "block";
    document.getElementById("proceedBtn").style.display = "inline-block";

    document.getElementById("fileName").textContent = file.name;
    document.getElementById("fileType").textContent = "Type: " + type;
    document.getElementById("fileSize").textContent =
        "Size: " + (file.size / (1024 * 1024)).toFixed(2) + " MB";

    const preview = document.getElementById("preview");

    if (file.type.startsWith("image")) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    } else {
        preview.style.display = "none";
    }
}


async function goToPage3() {

    if (!window.selectedFile) {
        alert("No file selected");
        return;
    }

    const formData = new FormData();
    formData.append("file", window.selectedFile);

    try {
        const response = await fetch("/authenticate", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        console.log("RESULT:", result);

        sessionStorage.setItem("authResult", JSON.stringify(result));

        window.location.href = "/page3";

    } catch (error) {
        alert("Backend connection failed");
        console.error(error);
    }
}
