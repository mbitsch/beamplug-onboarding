# pip install zxing-cpp

import cv2
from zxingcpp import read_barcodes
import time

camera_adr = 1 # hw adresse for webcam

def read_barcode_from_camera():
    """
    Læser stregkoder fra webcam.
    Stopper scanningen, når en stregkode er fundet.
    """
    camera = cv2.VideoCapture(camera_adr)

    if not camera.isOpened():
        print("Fejl: Kunne ikke åbne kamera.")
        return

    # Sætter kameraopløsning for bedre performance.
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Indsæt forsinkelse for at kameraet kan initialiseres.
    time.sleep(1)

    while True:
        # Læs en ramme fra kameraet.
        ret, frame = camera.read()
        if not ret:
            print("Fejl: Kunne ikke læse en ramme.")
            break

        # Konverter rammen til gråtoner for at forbedre stregkodelæsningen.
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Brug zxing-cpp til at læse stregkoder.
        barcodes = read_barcodes(gray_frame)

        # Kontroller, om der er fundet stregkoder.
        if barcodes:
            for barcode in barcodes:
                # Udskriv de dekodede oplysninger.
                print(f"Stregkode fundet: {barcode.text} (Format: {barcode.format.name})")
                
                # Hent de fire hjørnepunkter direkte fra position-objektet.
                p1 = (int(barcode.position.top_left.x), int(barcode.position.top_left.y))
                p2 = (int(barcode.position.top_right.x), int(barcode.position.top_right.y))
                p3 = (int(barcode.position.bottom_right.x), int(barcode.position.bottom_right.y))
                p4 = (int(barcode.position.bottom_left.x), int(barcode.position.bottom_left.y))

                # Tegn en boks omkring stregkoden ved at forbinde hjørnepunkterne.
                cv2.line(frame, p1, p2, (0, 255, 0), 2)
                cv2.line(frame, p2, p3, (0, 255, 0), 2)
                cv2.line(frame, p3, p4, (0, 255, 0), 2)
                cv2.line(frame, p4, p1, (0, 255, 0), 2)

                # Vis rammen med den tegnede boks.
                cv2.imshow("Barcode Scanner", frame)
                
                # Evt. vent på et tastetryk for at afslutte
                # cv2.waitKey(0)

                # Frigør kameraet og luk vinduet
                camera.release()
                cv2.destroyAllWindows()
                return barcode.text # Returner den fundne stregkode.

        # Vis rammen i et vindue.
        cv2.imshow("Barcode Scanner", frame)

        # Vent på tastetryk ('q' for at afslutte).
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Frigør kameraet og luk alle vinduer.
    camera.release()
    cv2.destroyAllWindows()
    return None

if __name__ == "__main__":
    found_barcode = read_barcode_from_camera()
    if found_barcode:
        print(f"Scanning afsluttet. Den fundne stregkode var: {found_barcode}")
    else:
        print("Scanning afsluttet. Ingen stregkode fundet.")