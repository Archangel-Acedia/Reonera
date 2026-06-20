**🌌 REONERA ENGINE**

**Expert High-Fidelity Desktop Automation & Vision Platform**

*REONERA is a frameless, hardware-accelerated desktop console that actively monitors target application windows, detects sub-pixel visual changes in real-time, and dispatches encrypted multi-channel alerts—all while wrapped in a completely customizable, immersive GLSL environment.*

[What is REONERA?](#what-is-reonera) • [Anti-Detection](#anti-detection) • [Vision Engine](#vision-engine) • [Quick Start](#quick-start) • [UI & Settings](#ui--settings) • [Advanced Architecture](#advanced-architecture)

## <a name="what-is-reonera"></a>**🎯 What is REONERA? (The Use-Case)**

REONERA was explicitly designed to monitor high-security, browser-based task queues and dashboards—such as AI training sites: Outlier, DataAnnotation, etc sites, freelance job boards, or rapid-response ticketing systems.

When you are waiting for tasks to drop, manually refreshing a page for hours is inefficient and exhausting. REONERA automates this process by visually scanning the webpage for you, instantly halting and pinging your phone or desktop the millisecond a new task appears.

However, because these platforms employ strict anti-bot telemetry, traditional automation tools (like Selenium or basic auto-clickers or auto-refreshers like Destill) lead to instant account bans. REONERA bypasses this by operating entirely at the **Operating System & Computer Vision level**. It does not inject code into the browser, it does not read the DOM, and it utilizes advanced human-emulation mathematics to ensure your web traffic looks 100% organic.

## <a name="anti-detection"></a>**🛡️ Stealth & Anti-Detection Mechanics**

REONERA employs a multi-layered humanization framework to avoid detection algorithms:

* **Browser Focus Spoofing:** Bots often click on windows that are out of focus, which is an immediate red flag. REONERA uses native OS hooks to silently pull your browser window into the active foreground milliseconds before a click, ensuring the site registers a legitimate focused interaction.  
* **The Circadian Engine:** No human works for 12 hours straight without pausing. The engine tracks your shift duration and calculates massive 30-to-45-minute "organic breaks" every \~3 hours, taking its hands off the keyboard completely to mimic human fatigue.  
* **Ballistic Decoy Clicks:** Instead of just refreshing the page, REONERA occasionally fires randomized "decoy clicks" into a designated Safe Zone (empty whitespace on the page). It uses eased, non-linear Bezier curves to move the mouse, proving to the website's telemetry that a physical mouse is moving around the page.  
* **Variable Asymmetric Timers:** Scan loops are never fixed. Every refresh cycle utilizes a randomized delay (e.g., waiting 5 minutes, then 7 minutes, then 4 minutes) offset by micro-millisecond floats, making it mathematically impossible for ban-filters to detect a pattern.

## <a name="vision-engine"></a>**👁️ How the Vision Engine Works**

Unlike web-scrapers, REONERA relies purely on what is physically rendered on your monitor.

1. **The Baseline Snip:** You draw a bounding box around the area of the screen where tasks normally appear (e.g., an empty queue message). REONERA saves this as target\_state.png.  
2. **The Dual-Match Process:** After every refresh, REONERA takes a live screenshot of that specific bounding box and compares it to the baseline using two algorithms:  
   * **Template Matching:** A high-speed pixel comparison to check for structural consistency.  
   * **Structural Similarity Index (SSIM):** A secondary pass that evaluates luminance, contrast, and structure. This prevents false positives caused by sub-pixel font rendering shifts or minor browser artifacts.  
3. **The Trigger:** If the live screen drastically deviates from the baseline (meaning a task has populated the empty space), the engine instantly halts the script to prevent refreshing over the task, locks the target, and fires your external alerts.

## <a name="asset-ecosystem"></a>**🎮 The Asset Ecosystem**

REONERA acts as a full desktop customization suite. It comes pre-loaded with:

* **10 Immersive Themes** (e.g., *Cyberpunk Glitch Matrix*, *Volcanic Magma*, *Deep Space Nebula*).  
* **17 Hardware-Accelerated Backgrounds:** Real-time OpenGL fragment shaders running in the UI background.  
* **82 Desktop Companions:** Choose from ninjas, slimes, werewolves, and more.  
* Each character pack contains anywhere from 4 to 20+ different sprite sheets.  
* **Draggable Anywhere:** Companions are rendered on frameless, transparent windows. You can click and drag them **anywhere across your desktop, placing them over your active browser window, taskbar, or a second monitor**. They will autonomously cycle through their animation states (Idle, Run, Attack) indefinitely.

*Note: The companion engine autonomously scans PNG sprite sheets, processing them into functional animations and generating the necessary manifest JSON files without manual input.*

For deep-dive details on filesystem organization, see the [Advanced Architecture](#advanced-architecture) section.

## <a name="quick-start"></a>**🚀 The 3-Step Workflow**

To begin monitoring, you must map the engine to your screen.

### **1\. Anchor the Layout**

Use the bottom buttons to assign your screen coordinates:

* 📍 Mark Refresh: Click the target website's reload button.  
* 📐 Drag Safe Zone: Drag a box in an empty, safe area of the website for decoy clicks.  
* 📸 Snip Target: Drag a box strictly around the UI element that changes when a task drops.

### **2\. Configure Overlays (Optional)**

* 🚫 Mask Exclude: Blind the vision engine to specific spots *inside* your target snip (like a ticking clock or changing ad) so they don't trigger false alerts.  
* 🔒 Snip Login Wall: Snip the "Session Expired" or "Logged Out" popup. If the engine sees this, it fires a critical alert and halts to prevent botting a dead page.

### **3\. Engage**

When the status reads **SYSTEM READY**, click **START ENGINE**.

## <a name="ui--settings"></a>**🎛️ Complete Interface & Settings Breakdown**

### **Main Dashboard Controls**

| Component | Function |
| :---- | :---- |
| **Profile Dropdown** | Switch between saved, encrypted .reonera\_profile layout files. |
| \+ New | Generate a fresh profile layout for a different website. |
| **Vision Preview (Top Right)** | A live 10-FPS thumbnail showing exactly what the script's eye sees. Click it to open the dedicated **Live Vision Map** window with Heatmaps and Flash Zone overlays. |
| **Telemetry Chart** | A dynamic line graph tracking the variable time delays between your recent refresh loops. |
| **TechWave Visualizer** | A theme-adaptive, multi-layered glowing wave synthesizer that animates while the engine is scanning. |
| Clear Masks | Deletes all orange Mask Exclude blind spots you have drawn. |
| Compact (Top Bar) | Shrinks the massive dashboard down to a tiny, always-on-top micro-strip showing only your current status and a Stop button. |

### **Settings Matrix: Engine Flags**

| Setting | What it does |
| :---- | :---- |
| **Browser Focus Spoofing** | Silently brings the target window to the front before clicking to bypass focus telemetry. |
| **Circadian Engine** | Enforces massive organic breaks every \~3 hours to mimic human fatigue. |
| **Minimize to Tray** | Closing the window hides it in the Windows System Tray to keep your taskbar clean. |
| **Auto-Run on Launch** | Skips the "Start" button and immediately begins scanning if coordinates are mapped upon opening the app. |
| **Always on Top** | Pins the REONERA console above all other windows on your desktop. |

### **Settings Matrix: Alerts & Routing**

*Note: All webhooks and tokens are encrypted locally via Fernet AES-128 before saving.*

| Setting | What it does |
| :---- | :---- |
| **Local Audio** | Plays a system beep or a custom selected .wav file. |
| **OS Toast** | Pushes a native notification banner into the Windows Action Center. |
| **Discord / Slack** | Paste your webhook URL. The engine will message your server. |
| **Telegram** | Paste your Bot Token and Chat ID to receive instant alerts directly to your phone. |
| Run Connection Diagnostics | Fires a test packet to all your configured URLs to ensure your firewall isn't blocking them. |

### **Settings Matrix: Cosmetics**

| Setting | What it does |
| :---- | :---- |
| **Theme & Background** | Select the color palette and assign the specific Shadertoy GLSL background file. |
| **Companion 1, 2, 3** | Select up to 3 sprites. Off disables the slot. |
| **Animation Dropdown** | Lock a companion to a specific state (e.g., attack), or leave it on **Cycle All** to automatically rotate through all of its available animations. |

### **Settings Matrix: Rendering & Performance**

| Setting | What it does |
| :---- | :---- |
| **Render Canvas Graphics** | Master switch. Turning this off disables all backgrounds and companions to save RAM. |
| **Allow Background Animations** | If off, the background and companions freeze on a single frame. |
| **Economy Mode** | Locks the OpenGL shader framerate to 30 FPS instead of 60 to lower GPU overhead. |
| **Combat Mode** | Spawns a Werewolf companion. When a task is detected, your primary companion will fire a fireball to "kill" the werewolf as a visual celebration. |
| **Disable Canvas Background** | Strips the heavy GLSL shader and replaces it with a flat, solid hex color. |

### **Settings Matrix: Developer**

| Setting | What it does |
| :---- | :---- |
| Bake Standalone .EXE | Uses PyInstaller to bundle your Python environment into a portable REONERA.exe file you can share or run without a terminal. |
| Deploy Shortcuts | Automatically wires shortcuts to your Windows Desktop and Start Menu. |
| Rebuild Manifests | If you drop new PNG sprite sheets into the assets/companion/ folder, clicking this auto-compiles the JSON maps so the engine can read them. |

# <a name="advanced-architecture"></a>**⚙️ REONERA: ADVANCED ARCHITECTURE**

**Developer Operations, Thread Safety, & Deployment Guide**

*This document serves as the technical companion to the main REONERA manual. It details the internal filesystem, execution threads, manual environment bootstrapping, and liability disclaimers for developers and contributors.*

This architecture supports the themes and companions defined in the [Asset Ecosystem](#asset-ecosystem).

## **📂 Project Architecture Tree**

REONERA relies on a strict asset ecosystem. If you are adding custom AI-generated UI skins, new Shadertoy JSON backgrounds, or custom PNG companion sprites, they must be placed in their exact respective directories to be dynamically hot-loaded by the engine.

REONERA/  
├── Reonera.py              \# Main GUI Controller & Layout Engine  
├── requirements.txt        \# Frozen Python dependency manifests  
├── generated\_themes/       \# Output directory for generative AI tools  
└── reonera/  
    ├── .bootstrapped       \# Pre-flight gate lifecycle anchor file  
    ├── .reonera.key        \# Locally compiled Fernet AES-128 cryptographic key  
    ├── default.reonera\_profile  \# Default encrypted binary database profile  
    └── assets/  
        ├── logo.png        \# Native title bar brand logo vector  
        ├── icon.ico        \# Native application OS handle icon  
        ├── icons/          \# Fallback UI vector layers (Tabler Icon hooks)  
        ├── background/     \# Immersive theme nodes (10 folders, 17 variants)  
        │   └── Volcanic Magma/  
        │       ├── llK3Dy.json  
        │       └── ui/     \# Core slice assets (border\_frame.png, button\_hover.png, etc.)  
        └── companion/      \# Data-driven companion directories (82 characters)  
            └── Warrior\_1/  
                ├── manifest.json   \# Auto-generated frame coordinate matrix  
                ├── Idle.png        \# Dynamic Sprite Sheets (4 to 20+ per character)  
                ├── Run.png  
                └── Attack.png

## **🧬 Core Architecture & Thread Safety**

To ensure the REONERA dashboard never freezes while performing intense visual calculations or network operations, the application strictly isolates tasks across independent processing pipelines.

┌────────────────────────────────────────────────────────┐  
│                   MAIN UI THREAD (PyQt6)               │  
│  \- Real-time QSS Layout Engine                         │  
│  \- 60 FPS QOpenGLWidget Hardware Shader Pipeline       │  
│  \- FSM Sprite Animation Renderer                       │  
└───────────┬────────────────────────────────┬───────────┘  
            │ ASYNC                          │ ASYNC  
            ▼ DISPATCH                       ▼ DISPATCH  
┌───────────────────────────┐    ┌───────────────────────────┐  
│     MONITOR THREAD        │    │ COMPANION COMPILER THREAD │  
│  \- PyAutoGUI Screenshots  │    │  \- Sequential Disk Scan   │  
│  \- OpenCV Template Match  │    │  \- Binary PNG Header Sniper│  
│  \- Scikit-Image SSIM      │    │  \- manifest.json Writer   │  
└───────────────────────────┘    └───────────────────────────┘

### **Technical Implementation Details**

* **Thread Isolation:** The heavy computer vision logic (screenshot scraping, pixel array conversions, and SSIM mathematics) runs entirely on a detached QThread. This guarantees the primary PyQt6 interface remains incredibly snappy, allowing the OpenGL shader canvas and your draggable companions to render smoothly at 60 FPS without micro-stuttering.  
* **Thread-Safe Signaling:** The background scanning pipeline never directly mutates the user interface. It utilizes thread-safe Qt signals (pyqtSignal) to safely queue logs, telemetry delays, and screen capture updates back to the main interface thread.  
* **Memory Management:** To prevent the severe memory leaks often associated with continuous Python screen capture, the Live Vision Map uses persistent C-level numpy memory blocks (np.ascontiguousarray), overwriting old frames rather than flooding the Python garbage collector.

## **🛠️ Step-by-Step Manual Deployment**

REONERA includes an automatic bootstrap sequence on launch. However, if you are deploying the engine to a secure workstation or prefer manual provisioning, follow these exact terminal commands.

### **1\. Environment Isolation (Highly Recommended)**

To prevent dependency version conflicts with your global Python installation, it is best practice to spin up an isolated virtual environment node.

\# Initialize the virtual environment node  
python \-m venv venv

\# Activate the isolated node layout  
\# On Windows:  
venv\\Scripts\\activate

\# On Linux/macOS:  
source venv/bin/activate

### **2\. Manual Dependency Provisioning**

Once your environment is active, install the required UI, graphics, and computer vision libraries:

\# Upgrade pip to ensure clean wheel downloads  
pip install \--upgrade pip

\# Install the engine matrices  
pip install PyQt6 PyOpenGL opencv-python numpy scikit-image pyautogui pygetwindow plyer cryptography requests pytablericons

### **3\. Launch**

python Reonera.py

## **🔮 Future Roadmap**

REONERA is a living platform. Current development goals include:

1. **Ongoing Stabilization & Bug Fixes:** Minor optimizations to the OpenGL compiler context and multi-monitor coordinate tracking to handle Windows scaling quirks more gracefully.  
2. **Dynamic Jitter Profiles:** Future updates will introduce customizable curve parameters for the ballistic decoy clicks.  
3. **Adding custom UI for each theme**
4. **The "Stripped Core" Version:** We are actively planning a lightweight, headless variant of REONERA. This version will strip out the PyQt6 UI, the OpenGL graphics engine, and the companions entirely—shipping as a pure, ultra-low-overhead command-line interface (CLI) for users who only want the raw detection mathematics running silently in the background on weaker hardware.

## **⚖️ Terms of Service & Security Disclaimer**

Because REONERA interfaces with third-party web platforms, freelance boards, and task queues that employ strict anti-bot telemetry, this legal disclaimer must be acknowledged before deploying the software.

**CRITICAL NOTICE:** This software framework is intended strictly for educational, research, and personal workflow optimization purposes.

Automating interactions, scraping screen data, or mimicking human traffic on third-party platforms may violate their specific Terms of Service (ToS), potentially resulting in account restrictions, suspensions, or permanent bans.

The developers and contributors of REONERA assume **absolute zero liability** for how individuals deploy this toolkit. You are entirely responsible for analyzing your target platform's automation guidelines, ensuring your own compliance, and assessing the risks associated with headless, computer-vision, or hardware-emulated screen-scraping techniques.

**Deploy at your own discretion.**
