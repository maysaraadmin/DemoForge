# DemoForge - AI/ML Stack Manager

A comprehensive PyQt5 GUI application for managing your Docker Compose AI/ML services stack.

## 🚀 Features

### 📊 Dashboard
- **Real-time Service Monitoring**: Live status updates for all services
- **Quick Access**: Direct links to open services in your browser
- **Visual Status Indicators**: Color-coded status for each service
- **Quick Actions**: Start, stop, and restart all services with one click

### 🔧 Services Management
- **Detailed Service Table**: View container status, ports, CPU, and memory usage
- **Individual Service Control**: Start, stop, restart individual services
- **Container Information**: View container names and detailed status
- **Auto-refresh**: Configurable auto-refresh intervals

### 🌐 **NEW: Embedded Browser**
- **Internal Web Browser**: View all services without leaving the application
- **Quick Service Access**: Direct navigation to any service with one click
- **Navigation Controls**: Back, forward, refresh, and home buttons
- **URL Management**: Direct URL input and service dropdown selector
- **Progress Tracking**: Visual loading progress for pages
- **External Browser Option**: Open current page in system default browser
- **Keyboard Shortcuts**: Ctrl+R (refresh), Ctrl+L (focus URL), Ctrl+H (home)

### 📋 Logs Viewer
- **Service-specific Logs**: View logs for any service
- **Configurable Log Depth**: Choose how many lines to display (100, 200, 500, 1000, or all)
- **Real-time Log Monitoring**: Live log updates
- **Easy Log Navigation**: Scroll through logs with syntax highlighting

### ⚙️ Settings
- **Auto-refresh Configuration**: Adjust refresh intervals (1-30 seconds)
- **Docker Connection Status**: Real-time Docker connectivity monitoring
- **Application Settings**: Customize GUI behavior

## 🛠️ Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: PyQt5-WebEngine requires additional system dependencies:
   - **Windows**: Install Visual C++ Build Tools or Visual Studio
   - **macOS**: Install XCode command line tools
   - **Linux**: Install Qt5 WebEngine development packages

2. **Run the GUI**:
   ```bash
   python launch_gui.py
   ```
   or
   ```bash
   python gui_manager.py
   ```

## 🔧 Services Managed

| Service | Description | Port | URL |
|---------|-------------|------|-----|
| **Ollama** | AI Model Server (Llama, Mistral, etc.) | 11434 | http://localhost:11434 |
| **N8N** | Workflow Automation Platform | 5678 | http://localhost:5678 |
| **Twenty CRM** | Open Source Pipeline Tracker | 8080 | http://localhost:8080 |
| **Typebot** | Chatbot Builder Platform | 3001 | http://localhost:3001 |
| **BentoML** | Model Serving Microservices | 5000 | http://localhost:5000 |
| **Portainer** | Docker Management UI | 9000 | http://localhost:9000 |

## 📱 Usage Guide

### Getting Started
1. **Ensure Docker Desktop is Running**: The GUI requires Docker to be running
2. **Launch the GUI**: Run `python launch_gui.py`
3. **Check Connection**: Verify Docker connection status in the bottom-right corner

### 🌐 Browser Tab
- **Select Service**: Use the dropdown to quickly navigate to any service
- **Direct URL Entry**: Type any URL in the input field and press Enter
- **Navigation**: Use back/forward buttons or Ctrl+Left/Ctrl+Right
- **Quick Refresh**: Press Ctrl+R or click the refresh button
- **Focus URL**: Press Ctrl+L to quickly focus the URL input
- **Home Button**: Return to Portainer (Docker management) anytime
- **External Browser**: Right-click or use Tools menu to open in external browser
- **Menu Access**: Use Browser menu for quick service access

### Services Tab
- **View Details**: See comprehensive information about each container
- **Individual Control**: Select a service and use the control buttons to manage it
- **Refresh Data**: Click the Refresh button to update all information

### Logs Tab
- **Select Service**: Choose a service from the dropdown menu
- **Configure Display**: Select how many log lines to show
- **View Logs**: Click Refresh Logs to load the latest logs
- **Monitor**: Logs update in real-time with syntax highlighting

### Settings Tab
- **Auto-refresh**: Adjust how often the GUI updates (1-30 seconds)
- **Performance**: Lower intervals provide more frequent updates but use more resources

## 🔍 Troubleshooting

### Common Issues

**"Docker: Disconnected" Error**
- Ensure Docker Desktop is running
- Check if Docker daemon is accessible
- Try restarting Docker Desktop

**Service Won't Start**
- Check Docker Compose logs: `docker-compose logs [service-name]`
- Verify ports are not in use by other applications
- Check if required images are available

**PyQt5-WebEngine Installation Issues**
- Ensure Visual C++ Build Tools are installed (Windows)
- Install Qt5 WebEngine system packages (Linux)
- Try: `pip install PyQtWebEngine --no-cache-dir`
- If issues persist, use system package manager to install Qt5 WebEngine

**Browser Not Loading Pages**
- Check if services are actually running
- Verify port numbers and URLs are correct
- Check firewall settings for service ports
- Try accessing the URL directly in external browser first

### Docker Commands Reference

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs for a specific service
docker-compose logs [service-name]

# Restart a specific service
docker-compose restart [service-name]

# View service status
docker-compose ps

# Rebuild and restart services
docker-compose up -d --build
```

## 🏗️ Architecture

The GUI is built with:
- **PyQt5**: Modern Python GUI framework with WebEngine support
- **QWebEngineView**: Embedded Chromium-based web browser
- **Docker Compose Integration**: Direct integration with docker-compose commands
- **Multi-threading**: Background monitoring without blocking the UI
- **Real-time Updates**: Live status monitoring and log streaming
- **Responsive Design**: Modern styling with comprehensive keyboard shortcuts

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📞 Support

For support and questions:
1. Check the troubleshooting section above
2. Review Docker Compose logs
3. Verify Docker Desktop is running properly
4. Check system requirements and dependencies
