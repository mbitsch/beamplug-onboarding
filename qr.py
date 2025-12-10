import qrcode

# Skift denne til jeres rigtige URL, når I har domæne
url = "https://beamplug-onboarding.onrender.com"

print("URL i QR-kode:", url)

img = qrcode.make(url)
filename = "qr_beamplug_onboarding.png"
img.save(filename)

print("QR-kode gemt som:", filename)