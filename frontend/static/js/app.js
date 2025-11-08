document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("fileInput");
    const uploadBox = document.getElementById("uploadBox");
    const imagePreview = document.getElementById("imagePreview");
    const uploadBtn = document.getElementById("uploadBtn");
    const uploadForm = document.getElementById("uploadForm");
    const resultsSection = document.getElementById("resultsSection");
    const resultContent = document.getElementById("resultContent");

    if (!fileInput || !uploadBox || !uploadForm) {
        console.error("❌ Upload elements missing in DOM.");
        return;
    }

    uploadBox.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (ev) => {
                imagePreview.src = ev.target.result;
                imagePreview.style.display = "block";
                imagePreview.style.maxWidth = "300px";
                imagePreview.style.margin = "1rem auto";

                const placeholder = document.getElementById("uploadPlaceholder");
                if (placeholder) placeholder.style.display = "none";
            };
            reader.readAsDataURL(file);
            uploadBtn.style.display = "inline-block";
        }
    });

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            alert("Please select an image first!");
            return;
        }

        const formData = new FormData(uploadForm);
        resultsSection.style.display = "block";
        resultContent.innerHTML = `<p>⏳ Analyzing image... Please wait.</p>`;

        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            console.log("🧠 Backend response:", data);

            if (!data.success) {
                resultContent.innerHTML = `
                    <div class="error-msg">
                        ⚠️ ${data.error || data.message || "Prediction failed!"}
                    </div>`;
                return;
            }

            const disease = data.predicted_disease || "Unknown";
            const confidence = data.confidence || 0;
            const isHealthy = disease.toLowerCase().includes("healthy");
            const rec = data.recommendation || {};

            // Build recommendation HTML
            let recommendationHTML = '';
            if (rec.fertilizer) {
                recommendationHTML += `
                    <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; margin: 1rem 0; text-align: left;">
                        <h4 style="color: #0284c7; margin-top: 0;">💊 Fertilizer Recommendation</h4>
                        <p style="margin: 0.5rem 0;">${rec.fertilizer}</p>
                    </div>`;
            }

            if (rec.immediate_actions && rec.immediate_actions.length > 0) {
                recommendationHTML += `
                    <div style="background: #fff7ed; padding: 1rem; border-radius: 8px; margin: 1rem 0; text-align: left;">
                        <h4 style="color: #ea580c; margin-top: 0;">⚡ Immediate Actions</h4>
                        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                            ${rec.immediate_actions.map(action => `<li>${action}</li>`).join('')}
                        </ul>
                    </div>`;
            }

            if (rec.treatment) {
                if (rec.treatment.organic && rec.treatment.organic.length > 0) {
                    recommendationHTML += `
                        <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; margin: 1rem 0; text-align: left;">
                            <h4 style="color: #16a34a; margin-top: 0;">🌿 Organic Treatment</h4>
                            <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                                ${rec.treatment.organic.slice(0, 3).map(t => `<li>${t}</li>`).join('')}
                            </ul>
                        </div>`;
                }
                if (rec.treatment.chemical && rec.treatment.chemical.length > 0) {
                    recommendationHTML += `
                        <div style="background: #fef2f2; padding: 1rem; border-radius: 8px; margin: 1rem 0; text-align: left;">
                            <h4 style="color: #dc2626; margin-top: 0;">🧪 Chemical Treatment</h4>
                            <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                                ${rec.treatment.chemical.slice(0, 3).map(t => `<li>${t}</li>`).join('')}
                            </ul>
                        </div>`;
                }
            }

            if (rec.prevention && rec.prevention.length > 0) {
                recommendationHTML += `
                    <div style="background: #fefce8; padding: 1rem; border-radius: 8px; margin: 1rem 0; text-align: left;">
                        <h4 style="color: #ca8a04; margin-top: 0;">🛡️ Prevention Tips</h4>
                        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                            ${rec.prevention.slice(0, 3).map(p => `<li>${p}</li>`).join('')}
                        </ul>
                    </div>`;
            }

            resultContent.innerHTML = `
                <div style="text-align:center;">
                    <h3 style="color:${isHealthy ? "#10b981" : "#ef4444"};">
                        ${isHealthy ? "✅ Healthy Plant!" : "⚠️ Disease Detected"}
                    </h3>
                    <p><strong>Disease:</strong> ${disease}</p>
                    <p><strong>Confidence:</strong> ${confidence}%</p>
                    
                    ${recommendationHTML}
                    
                    <div style="margin-top: 1.5rem;">
                        <button onclick="location.reload()" class="btn btn-primary">
                            Analyze Another Image
                        </button>
                    </div>
                </div>`;
        } catch (err) {
            console.error("⚠️ Prediction error:", err);
            resultContent.innerHTML = `
                <div class="error-msg">⚠️ Server error: ${err.message}</div>`;
        }
    });
});

const style = document.createElement("style");
style.innerHTML = `
.error-msg {
  color: #ef4444;
  background: #ffecec;
  font-weight: 600;
  margin: 1rem auto;
  padding: 0.8rem;
  border-radius: 8px;
  max-width: 400px;
}
`;
document.head.appendChild(style);

console.log("✅ New app.js loaded and initialized correctly");
