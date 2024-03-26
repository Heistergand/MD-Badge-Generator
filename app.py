from flask import Flask, request, send_from_directory, render_template, jsonify, send_file
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
import os, io, zipfile

app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'
MD_OVERLAY = 'templates/img/overlay.png'
MD_FONT = 'templates/ttf/Orbitron-Bold.ttf'

WORKING_AREA_HEIGHT = 800
WORKING_AREA_WIDTH = 800
IMAGE_AREA_HEIGHT = 460


# Stelle sicher, dass UPLOAD_FOLDER und OUTPUT_FOLDER existieren
os.makedirs('templates', exist_ok=True)
os.makedirs('templates/img', exist_ok=True)
os.makedirs('templates/ttf', exist_ok=True)
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def scale_image(input_image, max_width, max_height):
    """
    Skaliert ein Bild proportional, so dass es die maximalen Abmessungen nicht überschreitet,
    ohne es unter die minimalen Abmessungen (800x500) zu verkleinern.
    """
    original_width, original_height = input_image.size
    
    # Verhältnis des Originalbildes berechnen
    original_ratio = original_width / original_height
    
    # Zielverhältnis basierend auf den maximalen Abmessungen berechnen
    target_ratio = max_width / max_height
    
    # Entscheiden, ob das Bild basierend auf der Breite oder Höhe skaliert werden soll
    if original_ratio < target_ratio:
        # Skaliere basierend auf der Breite
        new_width = min(original_width, max_width)
        new_height = int(new_width / original_ratio)
    else:
        # Skaliere basierend auf der Höhe
        new_height = min(original_height, max_height)
        new_width = int(new_height * original_ratio)
    
    # Stelle sicher, dass das Bild nicht kleiner als die Mindestgrößen wird
    #new_width = max(new_width, 800)
    #new_height = max(new_height, 500)
    
    # Skaliere das Bild unter Verwendung von Lanczos-Resampling für eine hochwertige Reduktion
    return input_image.resize((new_width, new_height), Image.LANCZOS)



def process_image(file_stream, text, font_size, original_filename):
    """
    Verarbeitet ein einzelnes Bild: Skaliert es, fügt ein Overlay hinzu und beschriftet es mit Text.
    Gibt den Pfad zum gespeicherten Bild zurück.
    """

    # Aktuelles Datum im Format yyyymmdd
    current_date = datetime.now().strftime("%Y%m%d")
    
    # Bereinige den Text für den Dateinamen
    safe_text = "".join([c if c.isalnum() else "_" for c in text])
    safe_filename = "".join([c if c.isalnum() else "_" for c in original_filename.rsplit('.', 1)[0]])
    
    
    # Erstelle den neuen Dateinamen
    # new_filename = f"{current_date}_{safe_text}_{original_filename}"
    new_filename = f"{current_date}_{safe_text}_{safe_filename}.png"

    
    # Pfad, unter dem das bearbeitete Bild gespeichert wird
    output_filename = os.path.join(OUTPUT_FOLDER, new_filename)

    # Bildverarbeitung
    canvas = Image.new("RGBA", (WORKING_AREA_WIDTH, WORKING_AREA_HEIGHT), (255, 255, 255, 255))
    
    image = Image.open(file_stream).convert("RGBA")

    # Skaliere das Bild, falls notwendig
    image = scale_image(image, WORKING_AREA_WIDTH, IMAGE_AREA_HEIGHT)
   
    # Der Mittelpunkt des oberen Bereiches liegt bei x=400, y=230
    # Füge das Bild mittig ein
    width, height = image.size
    
    paste_x = int((WORKING_AREA_WIDTH - width) / 2)
    paste_y = int((IMAGE_AREA_HEIGHT - height) / 2)

    canvas.paste(image, (paste_x, paste_y), image)
    # canvas.paste(image, (0, 0), image)
    
    overlay = Image.open(MD_OVERLAY).convert("RGBA")
    overlay = scale_image(overlay, WORKING_AREA_WIDTH, WORKING_AREA_HEIGHT)
    canvas.paste(overlay, (0, 0), overlay)
    
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(MD_FONT, font_size)
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    # Zentriere den Text bei y=515
    text_x = int((WORKING_AREA_WIDTH - text_width) / 2)
    text_y = int(515 - (text_height / 2))
    draw.text((text_x, text_y), text, font=font, fill="white")
    
    canvas = scale_image(canvas, 512, 512) # official mission day badge format

    canvas.save(output_filename)
    return new_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global IMAGE_AREA_HEIGHT   
    
    files = request.files.getlist('user-images')
    if not files or files[0].filename == '':
        return 'Keine Dateien ausgewählt', 400


    text = request.form.get('text', '')
    font_size = int(request.form.get('font-size', 20))
    IMAGE_AREA_HEIGHT = int(request.form.get('image-area-height', 460))
    
    result_filenames = [process_image(file.stream, text, font_size, file.filename) for file in files if file and allowed_file(file.filename)]

    if not result_filenames:
        return jsonify({'error': 'Ungültiges Dateiformat'}), 400
    
    return render_template('gallery.html', images=result_filenames)    
    # return jsonify({'images': result_paths}), 200


@app.route('/download-image/<filename>')
def download_image(filename):
    image_path = os.path.join(app.root_path, 'static', 'outputs', filename)
    response: Response = send_file(image_path, mimetype='image/png', as_attachment=True, download_name=filename)
    return response

@app.route('/download_all')
def download_all():
    # Erstelle eine Byte-Stream für die ZIP-Datei
    zip_buffer = io.BytesIO()

    # Initialisiere die ZIP-Datei
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for root, dirs, files in os.walk(OUTPUT_FOLDER):
            for file in files:
                zip_file.write(os.path.join(root, file), file)
    
    # Gehe zurück zum Anfang des Byte-Streams
    zip_buffer.seek(0)

    # Sende die ZIP-Datei als Download
    # return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, attachment_filename='images.zip')
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='images.zip')
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

