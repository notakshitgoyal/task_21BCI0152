# PDF Co-Viewer 🚀

Live Demo: [https://task-21bci0152.onrender.com/](https://task-21bci0152.onrender.com/)

## Overview
PDF Co-Viewer is a real-time PDF presentation tool built with Flask and Socket.IO. It enables presenters to share and control PDF presentations with multiple viewers simultaneously.

## Quick Start 🚀

### For Presenters:
1. Go to [https://task-21bci0152.onrender.com/](https://task-21bci0152.onrender.com/)
2. Click **"Presenter Login"**
3. Obtain a unique session code
4. Upload your PDF
5. Share the session code with viewers
6. Control the presentation using Previous/Next buttons

### For Viewers:
1. Go to [https://task-21bci0152.onrender.com/](https://task-21bci0152.onrender.com/)
2. Click **"Viewer Login"**
3. Enter the session code provided by the presenter
4. Watch the presentation in real time!

## Tech Stack 💻
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Real-time Communication**: Socket.IO
- **PDF Processing**: PyMuPDF
- **Deployment**: Docker, Render.com

## Local Development 🛠️

```bash
# Clone the repository
git clone [your-repo-url]
cd pdf-co-viewer

# Create a virtual environment
python -m venv venv
source venv/bin/activate # Unix/Mac
# OR for Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Visit http://localhost:8080 in your browser
```

## Project Structure 📁

```plaintext
pdf-co-viewer/
├── app.py                 # Main application file
├── requirements.txt       # Dependencies
├── Dockerfile             # Docker configuration
├── templates/             # HTML templates
│   ├── home.html
│   ├── presenter.html
│   ├── viewer.html
│   ├── presenter_login.html
│   ├── viewer_login.html
│   └── shared_styles.html
└── uploads/               # PDF storage
```

## Key Features ✨
- **Real-time PDF Synchronization**: Viewers see page changes as the presenter navigates.
- **No Registration Required**: Quick, easy access for presenters and viewers.
- **Dark Mode UI**: Comfortable viewing for extended periods.
- **Mobile Responsive**: Compatible with various devices.
- **Secure Session Management**: Unique session codes ensure controlled access.
- **Easy-to-Share Session Codes**: Share a single code to grant access to the presentation.

## Deployment 🌐

### Required Packages

```plaintext
flask
flask-socketio
PyMuPDF
python-engineio==4.5.1
python-socketio==5.8.0
gunicorn
eventlet
Pillow
```

### Environment Variables

```plaintext
SECRET_KEY=your-secret-key
PORT=8080
```

## Docker Deployment 🐳

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn --worker-class eventlet -w 1 --bind "0.0.0.0:$PORT" app:app
```

## Future Enhancements 🚀
- [ ] Session Password Protection
- [ ] PDF Annotation Tools
- [ ] Chat Functionality
- [ ] Support for Multiple Presenters
- [ ] Presentation Recording

## Contributing 🤝
1. **Fork** the repository
2. **Create** a new branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

## License 📝
This project is licensed under the MIT License.

## Live Demo 🌐
[https://task-21bci0152.onrender.com/](https://task-21bci0152.onrender.com/)

## Acknowledgments 🙏
- **Flask-SocketIO** for real-time functionality
- **PyMuPDF** for PDF processing
- **Render.com** for hosting services
```