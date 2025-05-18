import os
from flask import Flask, send_file, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(open("templates/index.html", encoding="utf-8").read())

@app.route('/download')
def download_file():
    # Path to your ZIP file
    zip_file_path = 'path_to_your_webcraft.zip'  # Make sure the file exists in this location
    if os.path.exists(zip_file_path):
        return send_file(zip_file_path, as_attachment=True, download_name="WebCraft.zip", mimetype='application/zip')
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
