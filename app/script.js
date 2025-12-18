/* ================= NAVIGATION ================= */
function showSection(id) {
  document.getElementById("home").style.display = "none";
  document.querySelectorAll(".section").forEach(s => s.style.display = "none");
  document.getElementById(id).style.display = "block";
}

function goHome() {
  document.querySelectorAll(".section").forEach(s => s.style.display = "none");
  document.getElementById("home").style.display = "grid";
}

/* ================= LINK API ================= */
async function analyzeLink() {
  const url = document.getElementById("linkInput").value;
  const output = document.getElementById("linkResult");

  if (!url.trim()) {
    output.innerHTML = "<span class='error'>❌ URL is required</span>";
    return;
  }

  output.innerHTML = "<span class='loading'>⏳ Scraping & Analyzing...</span>";

  const formData = new FormData();
  formData.append("url", url);

  try {
    const res = await fetch("http://127.0.0.1:8000/analyze/link", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    displayResult(output, data);

  } catch (err) {
    output.innerHTML = "<span class='error'>❌ Server error</span>";
  }
}


/* ================= TEXT API ================= */
async function analyzeText() {
  const text = document.getElementById("textInput").value;
  const output = document.getElementById("textResult");

  if (!text.trim()) {
    output.innerHTML = "<span class='error'>❌ Text is required</span>";
    return;
  }

  output.innerHTML = "<span class='loading'>⏳ Analyzing...</span>";

  const formData = new FormData();
  formData.append("text", text);

  const res = await fetch("http://127.0.0.1:8000/analyze/text", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  displayResult(output, data);
}

/* ================= IMAGE API ================= */
async function analyzeImage() {
  const file = document.getElementById("imageInput").files[0];
  const output = document.getElementById("imageResult");

  if (!file || !file.type.startsWith("image/")) {
    output.innerHTML = "<span class='error'>❌ Invalid image file</span>";
    return;
  }

  output.innerHTML = "<span class='loading'>⏳ Analyzing...</span>";

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://127.0.0.1:8000/analyze/image", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  displayResult(output, data);
}

/* ================= VIDEO API ================= */
async function analyzeVideo() {
  const file = document.getElementById("videoInput").files[0];
  const output = document.getElementById("videoResult");

  if (!file || !file.type.startsWith("video/")) {
    output.innerHTML = "<span class='error'>❌ Invalid video file</span>";
    return;
  }

  output.innerHTML = "<span class='loading'>⏳ Analyzing...</span>";

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://127.0.0.1:8000/analyze/video", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  displayResult(output, data);
}

/* ================= RESULT UI ================= */
function displayResult(container, data) {
  const verdictClass =
    data.verdict.toLowerCase().includes("real") ? "verdict-real" :
    data.verdict.toLowerCase().includes("fake") ? "verdict-fake" :
    "verdict-uncertain";

  const confidence = (data.confidence * 100).toFixed(2);

  container.innerHTML = `
    <div class="result-card">
      <div class="result-header">
        <span class="verdict ${verdictClass}">
          ${data.verdict}
        </span>
        <span class="confidence">
          Confidence: ${confidence}%
        </span>
      </div>

      <div class="result-section">
        <h4>📌 Claim</h4>
        <p>${data.claim || "Not available"}</p>
      </div>

      <div class="result-section">
        <h4>🧠 Explanation</h4>
        <p>${data.explanation || "No explanation returned."}</p>
      </div>
    </div>
  `;
}
