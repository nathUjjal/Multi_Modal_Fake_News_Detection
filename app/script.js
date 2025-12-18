  function showSection(id) {
    document.getElementById("home").style.display = "none";
    document.querySelectorAll(".section").forEach(s => s.style.display = "none");
    document.getElementById(id).style.display = "block";
  }

  function goHome() {
    document.querySelectorAll(".section").forEach(s => s.style.display = "none");
    document.getElementById("home").style.display = "grid";
  }

  function checkLink() {
    const link = linkInput.value;
    linkResult.innerHTML = link.startsWith("https")
      ? "<span class='success'>✅ Likely REAL link</span>"
      : "<span class='error'>❌ Suspicious link</span>";
  }

  function checkText() {
    const text = textInput.value.toLowerCase();
    const fakeWords = ["breaking", "shocking", "viral", "you won't believe"];
    const found = fakeWords.some(w => text.includes(w));

    textResult.innerHTML = found
      ? "<span class='error'>🔴 Likely FAKE (clickbait detected)</span>"
      : "<span class='success'>🟢 Likely REAL text</span>";
  }

  function checkImage() {
    const file = imageInput.files[0];
    imageResult.innerHTML = (!file || !file.type.startsWith("image/"))
      ? "<span class='error'>❌ Invalid image format</span>"
      : "<span class='success'>✅ Valid image</span>";
  }

  function checkVideo() {
    const file = videoInput.files[0];
    videoResult.innerHTML = (!file || !file.type.startsWith("video/"))
      ? "<span class='error'>❌ Invalid video format</span>"
      : "<span class='success'>✅ Valid video</span>";
  }