import sys
import os
import json
import subprocess
import threading
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
                             QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QProgressBar, QGroupBox, QSplitter,
                             QStatusBar, QMessageBox, QMenuBar, QAction, QComboBox,
                             QLineEdit, QToolBar, QFrame)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings


class CustomWebEnginePage(QWebEnginePage):
    """Custom WebEngine page with enhanced error handling"""

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        """Handle JavaScript console messages with filtering"""
        # Filter out noisy messages
        if "Content-Security-Policy" in message:
            return  # Suppress CSP warnings
        if "recaptcha" in message.lower():
            return  # Suppress recaptcha warnings
        if "SyntaxError" in message and "Unexpected token" in message:
            return  # Suppress common JS syntax errors from services

        # Only log important errors
        if level > 0:  # Only warnings and errors, not info messages
            print(f"JS Console [{level}]: {message}")


class DockerComposeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DemoForge - AI/ML Stack Manager")
        self.setGeometry(100, 100, 1400, 900)

        # Set application icon and styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e8e8e8;
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2e3440;
            }
            QPushButton {
                background-color: #5e81ac;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #81a1c1;
            }
            QPushButton:pressed {
                background-color: #4c566a;
            }
            QPushButton:disabled {
                background-color: #d8dee9;
                color: #a0a0a0;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #5e81ac;
            }
            QWebEngineView {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QProgressBar {
                border: none;
                height: 4px;
                background-color: #e8e8e8;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #5e81ac;
                border-radius: 2px;
            }
        """)

        # Service configuration
        self.services = {
            'ollama': {
                'name': 'Ollama',
                'description': 'AI Model Server (Llama, Mistral, etc.)',
                'port': 11434,
                'url': 'http://localhost:11434',
                'color': '#ff6b6b'
            },
            'n8n': {
                'name': 'N8N',
                'description': 'Workflow Automation Platform',
                'port': 5678,
                'url': 'http://localhost:5678',
                'color': '#4ecdc4'
            },
            'twenty': {
                'name': 'Twenty CRM',
                'description': 'Open Source Pipeline Tracker',
                'port': 8080,
                'url': 'http://localhost:8080',
                'color': '#45b7d1'
            },
            'hexabot': {
                'name': 'Typebot',
                'description': 'Chatbot Builder Platform',
                'port': 3001,
                'url': 'http://localhost:3001',
                'color': '#f39c12'
            },
            'bentoml': {
                'name': 'BentoML',
                'description': 'Model Serving Microservices',
                'port': 5000,
                'url': 'http://localhost:5000',
                'color': '#2ecc71'
            },
            'portainer': {
                'name': 'Portainer',
                'description': 'Docker Management UI',
                'port': 9000,
                'url': 'http://localhost:9000',
                'color': '#e74c3c'
            }
        }

        self.supporting_services = ['postgres_n8n', 'postgres_twenty', 'redis', 'mongo']

        # Initialize UI
        self.init_ui()
        self.init_menu()
        self.init_status_bar()

        # Start monitoring thread
        self.monitoring_thread = ContainerMonitor(self)
        self.monitoring_thread.status_updated.connect(self.update_container_status)
        self.monitoring_thread.start()

        # Auto-refresh every 5 seconds
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_all_data)
        self.refresh_timer.start(5000)

    def init_ui(self):
        """Initialize the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Dashboard tab
        self.dashboard_tab = self.create_dashboard_tab()
        self.tab_widget.addTab(self.dashboard_tab, "🏠 Dashboard")

        # Services tab
        self.services_tab = self.create_services_tab()
        self.tab_widget.addTab(self.services_tab, "🔧 Services")

        # Browser tab
        self.browser_tab = self.create_browser_tab()
        self.tab_widget.addTab(self.browser_tab, "🌐 Browser")

        # Logs tab
        self.logs_tab = self.create_logs_tab()
        self.tab_widget.addTab(self.logs_tab, "📋 Logs")

        # Settings tab
        self.settings_tab = self.create_settings_tab()
        self.tab_widget.addTab(self.settings_tab, "⚙️ Settings")

        layout.addWidget(self.tab_widget)

    def init_menu(self):
        """Initialize the menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')
        refresh_action = QAction('Refresh', self)
        refresh_action.triggered.connect(self.refresh_all_data)
        file_menu.addAction(refresh_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        docker_action = QAction('Open Docker Desktop', self)
        docker_action.triggered.connect(self.open_docker_desktop)
        tools_menu.addAction(docker_action)

        tools_menu.addSeparator()
        external_browser_action = QAction('Open in External Browser', self)
        external_browser_action.triggered.connect(self.open_in_external_browser)
        tools_menu.addAction(external_browser_action)

        # Browser menu
        browser_menu = menubar.addMenu('Browser')
        refresh_browser_action = QAction('Refresh Browser', self)
        refresh_browser_action.triggered.connect(self.browser_refresh)
        browser_menu.addAction(refresh_browser_action)

        browser_menu.addSeparator()
        for service_id, service_info in self.services.items():
            service_action = QAction(f'Open {service_info["name"]}', self)
            service_action.triggered.connect(lambda checked, url=service_info['url']: self.open_service_url(url))
            browser_menu.addAction(service_action)

    def init_status_bar(self):
        """Initialize the status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # Add connection status
        self.connection_label = QLabel("Docker: Disconnected")
        self.connection_label.setStyleSheet("color: red; font-weight: bold;")
        self.status_bar.addPermanentWidget(self.connection_label)

    def create_dashboard_tab(self):
        """Create the dashboard tab with overview information"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("🤖 DemoForge - AI/ML Stack Dashboard")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Services grid
        services_group = QGroupBox("Services Status")
        services_layout = QGridLayout(services_group)

        self.service_labels = {}
        self.service_status_indicators = {}

        for i, (service_id, service_info) in enumerate(self.services.items()):
            # Service name and description
            service_label = QLabel(f"<b>{service_info['name']}</b><br><small>{service_info['description']}</small>")
            service_label.setWordWrap(True)

            # Status indicator
            status_indicator = QLabel("●")
            status_indicator.setStyleSheet(f"color: {service_info['color']}; font-size: 16px; font-weight: bold;")
            status_indicator.setAlignment(Qt.AlignCenter)

            # Service button
            service_button = QPushButton(f"Open {service_info['name']}")
            service_button.clicked.connect(lambda checked, url=service_info['url']: self.open_service_url(url))
            service_button.setStyleSheet(f"background-color: {service_info['color']};")

            # Add to grid
            services_layout.addWidget(service_label, i, 0)
            services_layout.addWidget(status_indicator, i, 1)
            services_layout.addWidget(service_button, i, 2)

            self.service_labels[service_id] = service_label
            self.service_status_indicators[service_id] = status_indicator

        layout.addWidget(services_group)

        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QHBoxLayout(actions_group)

        start_all_btn = QPushButton("🚀 Start All Services")
        start_all_btn.clicked.connect(self.start_all_services)
        actions_layout.addWidget(start_all_btn)

        stop_all_btn = QPushButton("⏹️ Stop All Services")
        stop_all_btn.clicked.connect(self.stop_all_services)
        actions_layout.addWidget(stop_all_btn)

        restart_all_btn = QPushButton("🔄 Restart All Services")
        restart_all_btn.clicked.connect(self.restart_all_services)
        actions_layout.addWidget(restart_all_btn)

        layout.addWidget(actions_group)

        # Spacer
        layout.addStretch()
        return widget

    def create_services_tab(self):
        """Create the services management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Services table
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(6)
        self.services_table.setHorizontalHeaderLabels(["Service", "Status", "Port", "Container", "CPU %", "Memory"])

        # Set column widths
        self.services_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.services_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.services_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.services_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.services_table.setColumnWidth(1, 100)
        self.services_table.setColumnWidth(2, 80)
        self.services_table.setColumnWidth(3, 120)

        # Style the table
        self.services_table.setAlternatingRowColors(True)
        self.services_table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addWidget(self.services_table)

        # Service controls
        controls_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_services_table)
        controls_layout.addWidget(refresh_btn)

        controls_layout.addStretch()

        # Service action buttons
        start_service_btn = QPushButton("▶️ Start Service")
        start_service_btn.clicked.connect(self.start_selected_service)
        controls_layout.addWidget(start_service_btn)

        stop_service_btn = QPushButton("⏹️ Stop Service")
        stop_service_btn.clicked.connect(self.stop_selected_service)
        controls_layout.addWidget(stop_service_btn)

        restart_service_btn = QPushButton("🔄 Restart Service")
        restart_service_btn.clicked.connect(self.restart_selected_service)
        controls_layout.addWidget(restart_service_btn)

        layout.addLayout(controls_layout)

        return widget

    def create_logs_tab(self):
        """Create the logs viewing tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Service selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Select Service:"))

        self.log_service_combo = QComboBox()
        self.log_service_combo.addItem("Select a service...")
        for service_id in self.services.keys():
            self.log_service_combo.addItem(self.services[service_id]['name'])
        self.log_service_combo.currentTextChanged.connect(self.load_service_logs)
        selector_layout.addWidget(self.log_service_combo)

        # Log controls
        tail_lines_label = QLabel("Lines:")
        selector_layout.addWidget(tail_lines_label)

        self.tail_lines_combo = QComboBox()
        self.tail_lines_combo.addItems(["100", "200", "500", "1000", "All"])
        self.tail_lines_combo.setCurrentText("200")
        selector_layout.addWidget(self.tail_lines_combo)

        refresh_logs_btn = QPushButton("🔄 Refresh Logs")
        refresh_logs_btn.clicked.connect(self.load_service_logs)
        selector_layout.addWidget(refresh_logs_btn)

        selector_layout.addStretch()
        layout.addLayout(selector_layout)

        # Logs display
        self.logs_text = QTextEdit()
        self.logs_text.setFont(QFont("Consolas", 9))
        self.logs_text.setReadOnly(True)
        layout.addWidget(self.logs_text)

        return widget

    def create_settings_tab(self):
        """Create the settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        settings_group = QGroupBox("Application Settings")
        settings_layout = QVBoxLayout(settings_group)

        # Auto-refresh interval
        refresh_layout = QHBoxLayout()
        refresh_layout.addWidget(QLabel("Auto-refresh interval (seconds):"))

        self.refresh_interval_combo = QComboBox()
        self.refresh_interval_combo.addItems(["1", "2", "5", "10", "30"])
        self.refresh_interval_combo.setCurrentText("5")
        self.refresh_interval_combo.currentTextChanged.connect(self.change_refresh_interval)
        refresh_layout.addWidget(self.refresh_interval_combo)
        refresh_layout.addStretch()
        settings_layout.addLayout(refresh_layout)

        layout.addWidget(settings_group)
        layout.addStretch()

        return widget

    def create_browser_tab(self):
        """Create the browser tab with embedded web view"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Browser toolbar
        toolbar_layout = QHBoxLayout()

        # URL input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL or select a service...")
        self.url_input.returnPressed.connect(self.load_url)
        url_layout.addWidget(self.url_input)

        # Service selector
        service_layout = QHBoxLayout()
        service_layout.addWidget(QLabel("Quick Access:"))
        self.browser_service_combo = QComboBox()
        self.browser_service_combo.addItem("Select service...")
        for service_id, service_info in self.services.items():
            self.browser_service_combo.addItem(f"{service_info['name']} ({service_info['url']})")
        self.browser_service_combo.currentTextChanged.connect(self.on_service_selected)
        service_layout.addWidget(self.browser_service_combo)
        service_layout.addStretch()

        toolbar_layout.addLayout(url_layout)
        toolbar_layout.addLayout(service_layout)

        # Navigation buttons
        nav_layout = QHBoxLayout()

        back_btn = QPushButton("⬅️ Back")
        back_btn.clicked.connect(self.browser_back)
        nav_layout.addWidget(back_btn)

        forward_btn = QPushButton("➡️ Forward")
        forward_btn.clicked.connect(self.browser_forward)
        nav_layout.addWidget(forward_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.browser_refresh)
        nav_layout.addWidget(refresh_btn)

        home_btn = QPushButton("🏠 Home")
        home_btn.clicked.connect(self.browser_home)
        nav_layout.addWidget(home_btn)

        nav_layout.addStretch()
        toolbar_layout.addLayout(nav_layout)

        layout.addLayout(toolbar_layout)

        # Create custom page with error handling
        self.browser_page = CustomWebEnginePage(self)
        self.browser_view = QWebEngineView()
        self.browser_view.setPage(self.browser_page)
        self.browser_view.loadProgress.connect(self.update_progress)

        # Enable context menu for browser
        self.browser_view.setContextMenuPolicy(Qt.DefaultContextMenu)

        # Configure web engine settings for better compatibility
        settings = self.browser_view.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)

        # Disable web security for local development (if needed)
        settings.setAttribute(QWebEngineSettings.WebSecurityEnabled, False)
        settings.setAttribute(QWebEngineSettings.CorsEnabled, True)

        layout.addWidget(self.browser_view)

        # Progress bar
        self.browser_progress = QProgressBar()
        self.browser_progress.setVisible(False)
        layout.addWidget(self.browser_progress)

        # Load default page (Portainer as it's the management interface)
        default_url = self.services['portainer']['url']
        self.browser_view.load(QUrl(default_url))
        self.url_input.setText(default_url)

        return widget

    def load_url(self):
        """Load URL from input field"""
        url_text = self.url_input.text().strip()
        if url_text:
            if not url_text.startswith(('http://', 'https://')):
                url_text = 'http://' + url_text
            self.browser_view.load(QUrl(url_text))

    def on_service_selected(self, text):
        """Handle service selection from dropdown"""
        if text and text != "Select service...":
            # Extract URL from the selected text
            for service_id, service_info in self.services.items():
                if f"{service_info['name']} ({service_info['url']})" == text:
                    self.open_service_url(service_info['url'])
                    break

    def browser_back(self):
        """Go back in browser history"""
        if self.browser_view.history().canGoBack():
            self.browser_view.back()

    def browser_forward(self):
        """Go forward in browser history"""
        if self.browser_view.history().canGoForward():
            self.browser_view.forward()

    def browser_refresh(self):
        """Refresh current page"""
        self.browser_view.reload()

    def browser_home(self):
        """Go to home page (Portainer)"""
        default_url = self.services['portainer']['url']
        self.browser_view.load(QUrl(default_url))
        self.url_input.setText(default_url)

    def update_progress(self, progress):
        """Update browser loading progress"""
        if progress < 100:
            self.browser_progress.setVisible(True)
            self.browser_progress.setValue(progress)
        else:
            self.browser_progress.setVisible(False)

            # Update URL input with current URL
            current_url = self.browser_view.url().toString()
            if current_url != self.url_input.text():
                self.url_input.setText(current_url)

    def _handle_js_console(self, level, message, line, source):
        """Handle JavaScript console messages - suppress noisy errors"""
        # Only show critical errors, suppress warnings and CSP messages
        if level == 0:  # Info level
            return
        if "Content-Security-Policy" in message:
            return  # Suppress CSP warnings
        if "recaptcha" in message.lower():
            return  # Suppress recaptcha warnings
        if "SyntaxError" in message and "Unexpected token" in message:
            return  # Suppress common JS syntax errors from services

        # Only print important errors
        print(f"JS [{level}]: {message} (line {line}, {source})")

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if self.tab_widget.currentWidget() == self.browser_tab:
            # Browser shortcuts
            modifiers = event.modifiers()
            key = event.key()

            if modifiers == Qt.ControlModifier:
                if key == Qt.Key_R:
                    self.browser_refresh()
                    event.accept()
                    return
                elif key == Qt.Key_L:
                    self.url_input.selectAll()
                    self.url_input.setFocus()
                    event.accept()
                    return
                elif key == Qt.Key_H:
                    self.browser_home()
                    event.accept()
                    return
                elif key == Qt.Key_Left:  # Ctrl+Left for back
                    self.browser_back()
                    event.accept()
                    return
                elif key == Qt.Key_Right:  # Ctrl+Right for forward
                    self.browser_forward()
                    event.accept()
                    return

        super().keyPressEvent(event)

    def refresh_all_data(self):
        """Refresh all data in the application"""
        self.refresh_services_table()
        self.update_connection_status()

    def update_connection_status(self):
        """Update Docker connection status"""
        try:
            result = subprocess.run(['docker', 'info'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.connection_label.setText("Docker: Connected")
                self.connection_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.connection_label.setText("Docker: Error")
                self.connection_label.setStyleSheet("color: red; font-weight: bold;")
        except:
            self.connection_label.setText("Docker: Disconnected")
            self.connection_label.setStyleSheet("color: red; font-weight: bold;")

    def update_container_status(self, status_data):
        """Update container status indicators"""
        for service_id, status in status_data.items():
            if service_id in self.service_status_indicators:
                indicator = self.service_status_indicators[service_id]
                if status == 'running':
                    indicator.setText("●")
                    indicator.setStyleSheet(f"color: {self.services[service_id]['color']}; font-size: 16px; font-weight: bold;")
                elif status == 'stopped':
                    indicator.setText("●")
                    indicator.setStyleSheet("color: #999; font-size: 16px; font-weight: bold;")
                else:
                    indicator.setText("●")
                    indicator.setStyleSheet("color: #ff6b6b; font-size: 16px; font-weight: bold;")

    def refresh_services_table(self):
        """Refresh the services table with current container information"""
        try:
            # Get container information
            result = subprocess.run(['docker', 'ps', '-a', '--format',
                                   'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}'],
                                  capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                self.services_table.setRowCount(0)
                lines = result.stdout.strip().split('\n')

                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split('\t')
                        if len(parts) >= 4:
                            container_name = parts[0]
                            status = parts[1]
                            ports = parts[2] if parts[2] != '<no value>' else 'N/A'
                            image = parts[3]

                            # Map container names to services
                            service_id = None
                            for sid, sname in [('postgres_n8n', 'postgres_n8n'),
                                              ('postgres_twenty', 'postgres_twenty'),
                                              ('portainer', 'portainer_demoforfe')]:
                                if sid in container_name or sname in container_name:
                                    service_id = sid
                                    break

                            if not service_id:
                                for sid in self.services.keys():
                                    if sid in container_name:
                                        service_id = sid
                                        break

                            if service_id:
                                row = self.services_table.rowCount()
                                self.services_table.insertRow(row)

                                # Service name
                                service_info = self.services.get(service_id, {'name': service_id, 'port': 'N/A'})
                                self.services_table.setItem(row, 0, QTableWidgetItem(service_info['name']))

                                # Status
                                status_item = QTableWidgetItem(status)
                                if 'Up' in status:
                                    status_item.setForeground(QColor('green'))
                                else:
                                    status_item.setForeground(QColor('red'))
                                self.services_table.setItem(row, 1, status_item)

                                # Port
                                self.services_table.setItem(row, 2, QTableWidgetItem(str(service_info.get('port', 'N/A'))))

                                # Container name
                                self.services_table.setItem(row, 3, QTableWidgetItem(container_name))

                                # CPU and Memory (placeholder)
                                self.services_table.setItem(row, 4, QTableWidgetItem("N/A"))
                                self.services_table.setItem(row, 5, QTableWidgetItem("N/A"))

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to refresh services: {str(e)}")

    def load_service_logs(self):
        """Load logs for the selected service"""
        service_name = self.log_service_combo.currentText()
        if service_name == "Select a service...":
            self.logs_text.clear()
            return

        # Find the actual container name
        container_name = None
        for service_id, service_info in self.services.items():
            if service_info['name'] == service_name:
                container_name = service_id
                break

        if not container_name:
            self.logs_text.setPlainText(f"Container not found for service: {service_name}")
            return

        try:
            tail_lines = self.tail_lines_combo.currentText()
            if tail_lines == "All":
                tail_param = ""
            else:
                tail_param = f"--tail {tail_lines}"

            result = subprocess.run(['docker', 'logs', tail_param, container_name],
                                  capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                self.logs_text.setPlainText(result.stdout)
                self.logs_text.moveCursor(self.logs_text.textCursor().End)
            else:
                self.logs_text.setPlainText(f"Error getting logs: {result.stderr}")

        except Exception as e:
            self.logs_text.setPlainText(f"Error: {str(e)}")

    def start_all_services(self):
        """Start all services"""
        try:
            subprocess.run(['docker-compose', 'up', '-d'],
                         cwd=os.path.dirname(__file__), check=True)
            QMessageBox.information(self, "Success", "All services started successfully!")
            self.refresh_all_data()
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"Failed to start services: {e}")

    def stop_all_services(self):
        """Stop all services"""
        try:
            subprocess.run(['docker-compose', 'down'],
                         cwd=os.path.dirname(__file__), check=True)
            QMessageBox.information(self, "Success", "All services stopped successfully!")
            self.refresh_all_data()
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"Failed to stop services: {e}")

    def restart_all_services(self):
        """Restart all services"""
        try:
            subprocess.run(['docker-compose', 'restart'],
                         cwd=os.path.dirname(__file__), check=True)
            QMessageBox.information(self, "Success", "All services restarted successfully!")
            self.refresh_all_data()
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"Failed to restart services: {e}")

    def start_selected_service(self):
        """Start the selected service"""
        self.execute_service_action('up', 'd')

    def stop_selected_service(self):
        """Stop the selected service"""
        self.execute_service_action('stop')

    def restart_selected_service(self):
        """Restart the selected service"""
        self.execute_service_action('restart')

    def execute_service_action(self, action, *args):
        """Execute a docker-compose action on the selected service"""
        current_row = self.services_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Warning", "Please select a service first.")
            return

        service_name = self.services_table.item(current_row, 0).text()
        container_name = self.services_table.item(current_row, 3).text()

        try:
            cmd = ['docker-compose', action] + list(args) + [container_name]
            subprocess.run(cmd, cwd=os.path.dirname(__file__), check=True)
            QMessageBox.information(self, "Success", f"Service {service_name} {action}ed successfully!")
            self.refresh_all_data()
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"Failed to {action} service {service_name}: {e}")

    def open_service_url(self, url):
        """Open a service URL in the internal browser"""
        try:
            # Check if browser components are initialized
            if not hasattr(self, 'browser_view') or not hasattr(self, 'browser_tab'):
                # Fallback to external browser if internal browser not ready
                import webbrowser
                webbrowser.open(url)
                return

            self.browser_view.load(QUrl(url))
            self.tab_widget.setCurrentWidget(self.browser_tab)
            self.url_input.setText(url)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to open URL: {e}")

    def open_in_external_browser(self):
        """Open current browser URL in external browser"""
        try:
            current_url = self.browser_view.url().toString()
            if current_url:
                import webbrowser
                webbrowser.open(current_url)
            else:
                QMessageBox.information(self, "Info", "No URL loaded in browser")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to open in external browser: {e}")

    def open_docker_desktop(self):
        """Open Docker Desktop"""
        try:
            if sys.platform == "win32":
                subprocess.run(['start', 'docker-desktop:'], shell=True)
            elif sys.platform == "darwin":
                subprocess.run(['open', '-a', 'Docker Desktop'])
            else:
                subprocess.run(['xdg-open', 'docker-desktop://'])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to open Docker Desktop: {e}")

    def change_refresh_interval(self):
        """Change the auto-refresh interval"""
        interval = int(self.refresh_interval_combo.currentText())
        self.refresh_timer.stop()
        self.refresh_timer.start(interval * 1000)

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About DemoForge Manager",
                         "DemoForge - AI/ML Stack Manager\n\n"
                         "A PyQt5 GUI for managing Docker Compose AI/ML services.\n\n"
                         "Services managed:\n"
                         "• Ollama - AI Model Server\n"
                         "• N8N - Workflow Automation\n"
                         "• Twenty CRM - Pipeline Tracker\n"
                         "• Typebot - Chatbot Builder\n"
                         "• BentoML - Model Serving\n"
                         "• Portainer - Docker Management\n\n"
                         "Built with PyQt5 and Docker Compose")

    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(self, 'Exit',
                                   "Are you sure you want to exit?",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Stop monitoring thread
            if hasattr(self, 'monitoring_thread'):
                self.monitoring_thread.stop()
                self.monitoring_thread.wait()
            event.accept()
        else:
            event.ignore()


class ContainerMonitor(QThread):
    """Thread for monitoring container status"""
    status_updated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True

    def run(self):
        """Monitor container status in a loop"""
        while self.running:
            try:
                # Get container status
                result = subprocess.run(['docker', 'ps', '--format',
                                       '{{.Names}}\t{{.Status}}'],
                                      capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    status_data = {}
                    lines = result.stdout.strip().split('\n')

                    for line in lines:
                        if line.strip():
                            parts = line.split('\t')
                            if len(parts) >= 2:
                                container_name = parts[0]
                                status = 'running' if 'Up' in parts[1] else 'stopped'

                                # Map container names to service IDs
                                for service_id in ['ollama', 'n8n', 'twenty', 'hexabot',
                                                 'bentoml', 'portainer', 'portainer_demoforfe',
                                                 'postgres_n8n', 'postgres_twenty', 'redis', 'mongo']:
                                    if service_id in container_name:
                                        status_data[service_id] = status
                                        break

                    self.status_updated.emit(status_data)

            except Exception as e:
                print(f"Monitoring error: {e}")

            # Wait 5 seconds before next check
            for _ in range(50):  # 5 seconds * 10 = 50 iterations of 100ms
                if not self.running:
                    break
                time.sleep(0.1)

    def stop(self):
        """Stop the monitoring thread"""
        self.running = False


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("DemoForge Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("DemoForge")

    # Create and show the main window
    window = DockerComposeManager()
    window.show()

    # Run the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
