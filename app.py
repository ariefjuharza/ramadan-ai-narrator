import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def build_prompt(pov, situasi, mode):

    base_instruction = f"""
Kamu adalah penulis satire Gen Z Indonesia yang cerdas dan peka budaya.

Tugasmu adalah membuat konten media sosial bertema Ramadan berdasarkan:

Sudut Pandang: {pov}
Situasi: {situasi}

Aturan umum:
- Gunakan Bahasa Indonesia sebagai bahasa utama.
- Boleh sisipkan sedikit istilah English jika natural (Gen Z tone).
- Humor harus relevan dengan kebiasaan Ramadan di Indonesia.
- Jangan menghina agama, ibadah, atau keyakinan.
- Hindari vulgaritas, politik, dan isu sensitif.
- Konten harus terasa original, kreatif, dan kontekstual.
"""

    if mode == "chaos":
        style_instruction = """
MODE: HIGH VIRAL CHAOS

- Narasi harus absurd, berisik, dan hiperbolik.
- Gunakan metafora tak terduga dan overreaction.
- Boleh breaking the fourth wall.
- Meme harus sangat punchy dan chaos.
- Prioritaskan energi komedi dibanding kedalaman emosi.
"""
    elif mode == "overdramatic":
        style_instruction = """
MODE: OVERDRAMATIC PARODY

- Hal sepele harus terasa seperti tragedi epik.
- Gunakan gaya trailer film atau dokumenter serius untuk situasi receh.
- Dramatisasi harus terasa sengaja berlebihan.
- Buat terasa seperti parodi film blockbuster.
"""
    else:
        style_instruction = """
MODE: CINEMATIC REFLECTIVE

- Narasi harus puitis, atmosferik, dan emosional.
- Humor halus dan tidak berisik.
- Fokus pada monolog internal dan suasana.
- Utamakan kedalaman rasa dibanding chaos.
"""

    output_instruction = """
Format output WAJIB seperti ini:

1. MONOLOG
2. PLOT TWIST
3. MEME ONE-LINER
4. INSTAGRAM CAPTION
5. CINEMATIC TRAILER VERSION
6. HASHTAGS

PENTING:
- Semua bagian harus terisi.
- Gunakan Bahasa Indonesia sebagai bahasa utama.
- HASHTAGS minimal 5 dan relevan (mudah dicari).
- Jangan berhenti di tengah kalimat.
- Pastikan perbedaan antar mode terasa jelas.
"""

    return f"""
{base_instruction}

{style_instruction}

{output_instruction}
"""

def call_model_studio(prompt):
    api_key = os.getenv("MODEL_STUDIO_API_KEY")

    url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen-plus",
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "temperature": 0.8,
            "top_p": 0.9,
            "max_tokens": 1200
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    pov = data.get("pov")
    situasi = data.get("situasi")
    mode = data.get("mode")

    prompt = build_prompt(pov, situasi, mode)
    ai_response = call_model_studio(prompt)

    try:
        output_text = ai_response["output"]["text"]
    except:
        return jsonify({"error": "AI response error", "details": ai_response})

    sections = {
        "monolog": "",
        "twist": "",
        "meme": "",
        "caption": "",
        "trailer": "",
        "hashtags": ""
    }

    current_key = None

    for line in output_text.split("\n"):
        if "1. MONOLOG" in line:
            current_key = "monolog"
            continue
        elif "2. PLOT TWIST" in line:
            current_key = "twist"
            continue
        elif "3. MEME ONE-LINER" in line:
            current_key = "meme"
            continue
        elif "4. INSTAGRAM CAPTION" in line:
            current_key = "caption"
            continue
        elif "5. CINEMATIC TRAILER VERSION" in line:
            current_key = "trailer"
            continue
        elif "6. HASHTAGS" in line:
            current_key = "hashtags"
            continue

        if current_key:
            sections[current_key] += line + "\n"

    if not sections["hashtags"].strip():
        sections["hashtags"] = "#Ramadan2026 #SahurKesiangan #DramaSahur #GenZRamadan #PuasaStory#NgabuburitLife"

    if not sections["trailer"].strip():
        sections["trailer"] = "Versi trailer belum tersedia. Coba generate ulang untuk hasil lebih sinematik."

    return jsonify(sections)

if __name__ == "__main__":
    app.run(debug=True)