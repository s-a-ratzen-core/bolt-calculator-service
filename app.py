import math
from sanic import Sanic, response
from sanic.request import Request

app = Sanic("BoltCalculator")
steel_density = 7850  # Плотность стали (кг/м^3)


@app.get("/health")
async def health(_request: Request):
    return response.json({"status": "ok"})


@app.post("/calculate")
async def calculate(request: Request):
    data = request.json or {}
    try:
        dk_mm = float(data["dk_mm"])
        hk_mm = float(data["hk_mm"])
        hr_mm = float(data["hr_mm"])
        sr_mm = float(data["sr_mm"])
        sh_mm = float(data["sh_mm"])
        hh_mm = float(data["hh_mm"])
    except (KeyError, TypeError, ValueError):
        return response.json(
            {"error": "Передайте числовые параметры: dk_mm, hk_mm, hr_mm, sr_mm, sh_mm, hh_mm"},
            status=400,
        )

    if any(val <= 0 for val in (dk_mm, hk_mm, hr_mm, sr_mm, sh_mm, hh_mm)):
        return response.json({"error": "Все размеры должны быть больше нуля"}, status=400)

    if hr_mm > hk_mm:
        return response.json({"error": "Длина резьбы не может превышать длину стержня"}, status=400)

    dk = dk_mm * 0.001
    hk = hk_mm * 0.001
    hr = hr_mm * 0.001
    sr = sr_mm * 0.001
    sh = sh_mm * 0.001
    hh = hh_mm * 0.001

    hs = hk - hr
    dr = dk - 0.65 * sr

    Vk = math.pi * dk**2 / 4 * hs
    Vt = math.pi * dr**2 / 4 * hr
    Vh = hh * math.sqrt(3) / 2 * sh**2
    Vg = Vk + Vt + Vh
    m = steel_density * Vg

    return response.json({
        "volume_m3": round(Vg, 9),
        "mass_kg": round(m, 4),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
