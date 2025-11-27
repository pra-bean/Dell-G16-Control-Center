import os
import sys
import fcntl
import psutil
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import QTimer, Qt

from monitor import get_cpu_stats, get_gpu_stats, get_fan_rpm
from performance import get_platform_profile
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu



# --- Prevent multiple instances ---
lock_file = '/tmp/g16control.lock'
fp = open(lock_file, 'w')

try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print("G16 Control Center is already running.")
    sys.exit(0)
    
# -------------------------------
# MAIN WINDOW
# -------------------------------
class G16ControlCenter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("G16 Control Center")
        self.setMinimumWidth(450)

        layout = QVBoxLayout()
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Tabs
        self.monitor_tab = self.build_monitor_tab()
        self.performance_tab = self.build_performance_tab()
        self.system_tab = self.build_system_tab()

        tabs.addTab(self.monitor_tab, "Monitor")
        tabs.addTab(self.performance_tab, "Performance")
        tabs.addTab(self.system_tab, "System Info")

        self.setLayout(layout)
        self.init_tray()

        # Timer for monitor refresh
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_monitor)
        self.timer.start(1000)  # refresh every 1 second

    # -------------------------------
    # MONITOR TAB
    # -------------------------------
    def build_monitor_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU: Loading...")
        self.gpu_label = QLabel("GPU: Loading...")
        self.fan_label = QLabel("Fans: Loading...")

        self.cpu_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.gpu_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.fan_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.gpu_label)
        layout.addWidget(self.fan_label)

        tab.setLayout(layout)
        return tab

    def update_monitor(self):
        cpu = get_cpu_stats()
        gpu = get_gpu_stats()
        fan = get_fan_rpm()

        self.cpu_label.setText(
            f"CPU: {cpu['temp']}°C,  {cpu['usage']}% usage"
        )

        self.gpu_label.setText(
            f"GPU: {gpu['temp']}°C,  {gpu['usage']}% usage,  {gpu['clock']} MHz"
        )

        self.fan_label.setText(
            "Fans:  " + ", ".join([f"{name}: {rpm} RPM" for name, rpm in fan.items()])
        )

    # -------------------------------
    # PERFORMANCE TAB
    # -------------------------------
    def build_performance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.current_profile_label = QLabel(
            f"Current Profile: {get_platform_profile()}"
        )

        btn_quiet = QPushButton("Quiet Mode")
        btn_balanced = QPushButton("Balanced Mode")
        btn_perf = QPushButton("Performance Mode")
        btn_gmode = QPushButton("G-Mode")

        btn_quiet.clicked.connect(lambda: self.apply_mode("quiet"))
        btn_balanced.clicked.connect(lambda: self.apply_mode("balanced"))
        btn_perf.clicked.connect(lambda: self.apply_mode("performance"))
        btn_gmode.clicked.connect(lambda: self.apply_mode("gmode"))


        layout.addWidget(self.current_profile_label)
        layout.addWidget(btn_quiet)
        layout.addWidget(btn_balanced)
        layout.addWidget(btn_perf)
        layout.addWidget(btn_gmode)

        tab.setLayout(layout)
        return tab


    def apply_mode(self, mode):
        """
        Calls pkexec to run the privileged profile switcher.
        """
        script_path = "/home/smurfy/g16-control-center/change_profile.py"
        try:
            subprocess.run(
                ["pkexec", script_path, mode],
                check=True
            )
        except Exception as e:
            print("Error:", e)

        # Update UI
        self.current_profile_label.setText(
            f"Current Profile: {get_platform_profile()}"
        )


    # -------------------------------
    # SYSTEM INFO TAB
    # -------------------------------
    def build_system_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        cpu_info = QLabel(f"CPU: {psutil.cpu_count()} cores")
        gpu_info = QLabel("GPU: NVIDIA GPU detected")
        ram_info = QLabel(f"RAM: {round(psutil.virtual_memory().total/1e9, 2)} GB")
        kernel_info = QLabel(f"Kernel: {sys.platform}")

        layout.addWidget(cpu_info)
        layout.addWidget(gpu_info)
        layout.addWidget(ram_info)
        layout.addWidget(kernel_info)

        tab.setLayout(layout)
        return tab
        
        
    def init_tray(self):
        tray_icon_path = "/home/smurfy/g16-control-center/icons/tray.png"
    
        self.tray = QSystemTrayIcon(QIcon(tray_icon_path))
        self.tray.setToolTip("G16 Control Center")
    
        # STORE MENU AS AN INSTANCE VARIABLE (IMPORTANT)
        self.menu = QMenu()
    
        self.open_action = QAction("Open")
        self.quit_action = QAction("Quit")
    
        self.open_action.triggered.connect(self.show_normal)
        self.quit_action.triggered.connect(self.close_app)
    
        self.menu.addAction(self.open_action)
        self.menu.addAction(self.quit_action)
    
        self.tray.setContextMenu(self.menu)
    
        self.tray.activated.connect(self.on_tray_activated)
    
        self.tray.show()
    


    def show_normal(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_normal()

    def close_app(self):
        self.tray.hide()
        QApplication.quit()
    
    def closeEvent(self, event):
        QApplication.quit()



# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = G16ControlCenter()
    window.show()
    sys.exit(app.exec())


