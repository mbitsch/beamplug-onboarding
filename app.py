from flask import Flask, render_template, request, redirect, url_for
from db import init_db, save_registration, send_to_energinet_stub

app = Flask(__name__)


@app.route("/")
def index():
    # Forsiden – viser “start onboarding”-knap
    return render_template("index.html", current_step=1)


@app.route("/onboarding", methods=["GET", "POST"])
def onboarding():
    # Find aktuelt step (1–4)
    if request.method == "POST":
        step = int(request.form.get("step", "1"))
    else:
        step = int(request.args.get("step", "1"))

    # ========== STEP 1 ==========
    # Kunde-id + velkomst
    if step == 1 and request.method == "GET":
        return render_template("step1.html", current_step=1)

    # ========== STEP 2 ==========
    # (det der før var step 3)
    if step == 2:
        customer_id = request.form.get("customer_id", "")
        wifi_ssid = request.form.get("wifi_ssid", "")
        wifi_password = request.form.get("wifi_password", "")

        return render_template(
            "step2.html",          # <--- Læg mærke til: step3.html
            customer_id=customer_id,
            wifi_ssid=wifi_ssid,
            wifi_password=wifi_password,
            current_step=2,
        )

    # ========== STEP 3 ==========
    # (det der før var step 2)
    if step == 3:
        customer_id = request.form.get("customer_id", "")

        return render_template(
            "step3.html",          # <--- Læg mærke til: step2.html
            customer_id=customer_id,
            current_step=3,
        )

    # ========== STEP 4 ==========
    # Betalingsoplysninger + gem i DB
    if step == 4:
        # De værdier vi altid skal have i step 4
        customer_id = request.form.get("customer_id", "")
        wifi_ssid = request.form.get("wifi_ssid", "")
        wifi_password = request.form.get("wifi_password", "")
        radiator_setting = request.form.get("radiator_setting", "")

        # Hvis brugeren HAR indsendt payment_info (trykket på knappen)
        if request.method == "POST" and request.form.get("payment_info"):
            payment_info = request.form.get("payment_info", "")

            # GEM DATA I DB - alle 5 argumenter
            save_registration(
                customer_id=customer_id,
                wifi_ssid=wifi_ssid,
                wifi_password=wifi_password,
                radiator_setting=radiator_setting,
                payment_info=payment_info,
            )

            # Stub til Energinet
            send_to_energinet_stub(customer_id)

            # Vis tak-side
            return render_template(
                "step4.html",
                customer_id=customer_id,
                finished=True,
                current_step=4,
            )

        # Første gang vi viser step 4 (ingen payment_info endnu)
        return render_template(
            "step4.html",
            customer_id=customer_id,
            wifi_ssid=wifi_ssid,
            wifi_password=wifi_password,
            radiator_setting=radiator_setting,
            finished=False,
            current_step=4,
        )

    # Hvis noget går galt: tilbage til step 1
    return redirect(url_for("onboarding", step=1))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
