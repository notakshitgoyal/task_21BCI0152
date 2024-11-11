from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
import secrets
import os
from pyngrok import ngrok
import fitz  # PyMuPDF
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app)

# Store active sessions
active_sessions = {}

# Define upload folder as an absolute path
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

print(f"Upload folder path: {UPLOAD_FOLDER}")  # Debug print

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/presenter-login', methods=['GET', 'POST'])
def presenter_login():
    if request.method == 'POST':
        session_code = secrets.token_hex(3)  # 6 character code
        session['role'] = 'presenter'
        session['room'] = session_code
        active_sessions[session_code] = {'file_path': None}
        return redirect(url_for('presenter_view', room=session_code))
    return render_template('presenter_login.html')

@app.route('/viewer-login', methods=['GET', 'POST'])
def viewer_login():
    if request.method == 'POST':
        session_code = request.form.get('session_code')
        if session_code in active_sessions:
            session['role'] = 'viewer'
            session['room'] = session_code
            return redirect(url_for('viewer_view', room=session_code))
        return "Invalid session code"
    return render_template('viewer_login.html')

@app.route('/presenter/<room>')
def presenter_view(room):
    if session.get('role') != 'presenter' or session.get('room') != room:
        return redirect(url_for('index'))
    return render_template('presenter.html', room=room)

@app.route('/viewer/<room>')
def viewer_view(room):
    if session.get('role') != 'viewer' or session.get('room') != room:
        return redirect(url_for('index'))
    return render_template('viewer.html', room=room)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Upload request received")
    
    if 'file' not in request.files:
        return 'No file part', 400
    
    room = session.get('room')
    if not room or room not in active_sessions:
        return 'Invalid session', 403
        
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
        
    if file and allowed_file(file.filename):
        try:
            # Save the PDF file
            filename = f"{room}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(f"File saved at: {filepath}")
            
            # Convert PDF pages to images
            pdf_document = fitz.open(filepath)
            print(f"PDF opened. Pages: {pdf_document.page_count}")
            
            images = []
            for page_num in range(pdf_document.page_count):
                print(f"Processing page {page_num + 1}")
                page = pdf_document[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                
                # Convert PyMuPDF pixmap to PIL Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Save image to bytes
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                
                # Convert to base64
                img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()
                images.append(f"data:image/png;base64,{img_base64}")
                print(f"Page {page_num + 1} converted")
            
            pdf_document.close()
            print("PDF processing completed")
            
            # Store images in active session
            active_sessions[room]['images'] = images
            active_sessions[room]['current_page'] = 0
            
            # Emit first page to all clients in the room
            socketio.emit('pdf_loaded', {
                'total_pages': len(images),
                'current_page': 0,
                'image_data': images[0]
            }, room=room)
            
            return 'File uploaded successfully'
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return f'Error processing PDF: {str(e)}', 500
    
    return 'Invalid file type', 400

@app.route('/uploads/<filename>')
def serve_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        print(f"Error serving file {filename}: {e}")
        return "File not found", 404

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)

@socketio.on('presenter-change-page')
def handle_presenter_change(data):
    room = session.get('room')
    if session.get('role') == 'presenter':
        emit('page-change', data['page'], room=room)

# Add SocketIO event handler for page changes
@socketio.on('change_page')
def handle_page_change(data):
    room = session.get('room')
    if not room or room not in active_sessions:
        return
    
    page_num = data.get('page', 0)
    images = active_sessions[room].get('images', [])
    
    print(f"Page change request - Room: {room}, Page: {page_num}")  # Debug log
    
    if images and 0 <= page_num < len(images):
        active_sessions[room]['current_page'] = page_num
        
        # Emit to all clients in the room
        socketio.emit('page_changed', {
            'current_page': page_num,
            'image_data': images[page_num],
            'total_pages': len(images)  # Add total pages to the response
        }, room=room)
        
        print(f"Page changed to {page_num + 1} of {len(images)}")  # Debug log

# ... existing code ... 

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    try:
        # Kill any existing ngrok processes
        ngrok.kill()
        
        # Set up ngrok
        ngrok.set_auth_token("2R18hFSNDWfNHx3Bmmta07KI4H1_328t6xKPC52PR6X172Zsw")
        
        # Connect with specific options
        public_url = ngrok.connect(
            addr="3000",
            proto="http",
            bind_tls=True
        )
        print(f" * Public URL: {public_url}")
    except Exception as e:
        print(f"Failed to start ngrok: {e}")
        print("Running without ngrok tunnel...")
    
    # Run the app
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)