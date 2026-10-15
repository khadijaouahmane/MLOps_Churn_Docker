const form = document.getElementById("churn-form");
const resultDiv = document.getElementById("result");
const resultLabel = document.getElementById("result-label");
const resultProba = document.getElementById("result-proba");
const resultTime = document.getElementById("result-time");
const submitBtn = form.querySelector('button[type="submit"]');

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.textContent = "Prédiction en cours...";

    // Construire le payload
    const formData = new FormData(form);
    const payload = {};
    for (const [key, value] of formData.entries()) {
        // Convertir les champs numériques
        if (["tenure", "SeniorCitizen", "MonthlyCharges", "TotalCharges"].includes(key)) {
            payload[key] = Number(value);
        } else {
            payload[key] = value;
        }
    }

    try {
        const t0 = performance.now();
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const t1 = performance.now();

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Erreur API");
        }

        const data = await res.json();
        showResult(data, (t1 - t0).toFixed(0));
    } catch (err) {
        resultDiv.classList.remove("hidden");
        resultLabel.textContent = "❌ Erreur";
        resultLabel.className = "churn";
        resultProba.textContent = err.message;
        resultTime.textContent = "";
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Prédire";
    }
});

function showResult(data, clientTimeMs) {
    resultDiv.classList.remove("hidden");
    const isChurn = data.prediction === 1;
    resultLabel.textContent = isChurn ? "⚠️ " + data.label : "✅ " + data.label;
    resultLabel.className = isChurn ? "churn" : "no-churn";
    resultProba.textContent = `Probabilité de churn : ${(data.probability_churn * 100).toFixed(2)} %`;
    resultTime.textContent = `Temps (client) : ${clientTimeMs} ms`;
    resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
}