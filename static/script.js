function formatText(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/\n/g, "<br>");
}

function generateContent() {
  const pov = document.getElementById("pov").value;
  const situasi = document.getElementById("situasi").value;
  const mode = document.getElementById("mode").value;

  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("outputSection").classList.add("hidden");

  fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pov, situasi, mode }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("monolog").innerHTML = formatText(data.monolog);
      document.getElementById("twist").innerHTML = formatText(data.twist);
      document.getElementById("meme").innerHTML = formatText(data.meme);
      document.getElementById("caption").innerHTML = formatText(data.caption);
      document.getElementById("trailer").innerHTML = formatText(data.trailer);
      document.getElementById("hashtags").innerHTML = formatText(data.hashtags);

      document.getElementById("loading").classList.add("hidden");
      document.getElementById("outputSection").classList.remove("hidden");
      document.getElementById("outputSection").classList.add("fade-in");
    });
}

function copyText(id) {
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text);

  const toast = document.getElementById("toast");
  toast.classList.remove("opacity-0");
  toast.classList.add("opacity-100");

  setTimeout(() => {
    toast.classList.remove("opacity-100");
    toast.classList.add("opacity-0");
  }, 1500);
}
