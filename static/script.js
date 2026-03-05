const loadingMessages = [
  "Menyusun narasi...",
  "Mengaduk drama sahur...",
  "Memanggil azan cinematic...",
  "Mengumpulkan plot twist...",
  "Mencari meme paling absurd...",
  "Menulis takdir sahurmu...",
];

let loadingInterval;

function startLoadingAnimation() {
  const loadingText = document.getElementById("loadingText");
  let i = 0;

  loadingInterval = setInterval(() => {
    loadingText.textContent = loadingMessages[i % loadingMessages.length];
    i++;
  }, 1800);
}

function stopLoadingAnimation() {
  clearInterval(loadingInterval);
}

async function generateContent() {
  const pov = document.getElementById("pov").value;
  const situasi = document.getElementById("situasi").value;
  const mode = document.getElementById("mode").value;

  const btn = document.getElementById("generateBtn");
  const loading = document.getElementById("loading");
  const output = document.getElementById("outputSection");

  btn.disabled = true;
  btn.classList.add("opacity-50", "cursor-not-allowed");

  loading.classList.remove("hidden");
  output.classList.add("hidden");

  startLoadingAnimation();

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ pov, situasi, mode }),
    });

    const data = await res.json();

    document.getElementById("monolog").innerHTML = formatText(data.monolog);
    document.getElementById("twist").innerHTML = formatText(data.twist);
    document.getElementById("meme").innerHTML = formatText(data.meme);
    document.getElementById("caption").innerHTML = formatText(data.caption);
    document.getElementById("trailer").innerHTML = formatText(data.trailer);
    document.getElementById("hashtags").innerHTML = formatText(data.hashtags);

    loading.classList.add("hidden");
    output.classList.remove("hidden");

    stopLoadingAnimation();

    output.scrollIntoView({
      behavior: "smooth",
    });
  } catch (err) {
    console.error(err);
  }

  btn.disabled = false;
  btn.classList.remove("opacity-50", "cursor-not-allowed");
}

function copyText(id) {
  const text = document.getElementById(id).innerText;

  navigator.clipboard.writeText(text);

  const toast = document.getElementById("toast");

  toast.classList.remove("opacity-0");

  setTimeout(() => {
    toast.classList.add("opacity-0");
  }, 2000);
}

function formatText(text) {
  return text.replace(/\n/g, "<br>").replace(/\*(.*?)\*/g, "<em>$1</em>");
}
