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
        step = request.form.get("step", "1")
    else:
        step = request.args.get("step", "1")

     # Kunde-id + velkomst
    if step == 1 and request.method == "GET":
        return render_template("step1.html", current_step=1)

    # ---------- STEP 1: Start (fra forsiden / QR) ----------
    # Vi starter bare direkte på radiator-step (step2.html)
    if step == 2 and request.method == "GET":
        customer_id = request.args.get("customer_id", "")  # kan komme fra QR
        return render_template(
            "step2.html",
            customer_id=customer_id,
            wifi_ssid="",
            wifi_password="",
            current_step=2,
        )

    # ---------- STEP 3: POST fra radiator-step (step2.html) -> vis WiFi-step ----------
    if step == 3 and request.method == "POST":
        customer_id = request.form.get("customer_id", "")
        radiator_setting = request.form.get("radiator_setting", "")

        # Hvis du på et tidspunkt vil have wifi-info tidligere med, kan de også hentes her:
        wifi_ssid = request.form.get("wifi_ssid", "")
        wifi_password = request.form.get("wifi_password", "")

        return render_template(
            "step3.html",
            customer_id=customer_id,
            radiator_setting=radiator_setting,
            wifi_ssid=wifi_ssid,
            wifi_password=wifi_password,
            current_step=3,
        )

    # ---------- STEP 4: POST fra WiFi-step (step3.html) / betalings-step (step4.html) ----------
    if step == 4 and request.method == "POST":
        customer_id = request.form.get("customer_id", "")
        wifi_ssid = request.form.get("wifi_ssid", "")
        wifi_password = request.form.get("wifi_password", "")
        radiator_setting = request.form.get("radiator_setting", "")
        payment_info = request.form.get("payment_info", "")

        # Første gang vi rammer step 4 (ingen payment_info endnu) -> vis betalingsform
        if not payment_info:
            return render_template(
                "step4.html",
                customer_id=customer_id,
                wifi_ssid=wifi_ssid,
                wifi_password=wifi_password,
                radiator_setting=radiator_setting,
                finished=False,
                current_step=4,
            )

        # Anden gang: betalingsform er udfyldt -> gem i DB og vis tak-side
        save_registration(
            customer_id=customer_id,
            wifi_ssid=wifi_ssid,
            wifi_password=wifi_password,
            radiator_setting=radiator_setting,
            payment_info=payment_info,
        )
        send_to_energinet_stub(customer_id)

        return render_template(
            "step4.html",
            customer_id=customer_id,
            wifi_ssid=wifi_ssid,
            wifi_password=wifi_password,
            radiator_setting=radiator_setting,
            finished=True,
            current_step=4,
        )

    # Hvis noget går galt: tilbage til start
    return redirect(url_for("onboarding", step=1))
