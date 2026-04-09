# 🖥️ SSH Connect Ultimate v2.0

**SSH Connect** is a professional, cross-platform terminal-based SSH connection manager. It offers a secure TUI (Text User Interface) to manage multiple servers with automated Midnight Commander integration, AES-256 encryption, and real-time connectivity tracking.

---

## 🚀 Key Features

- **Modular Architecture**: Clean, organized code separated into functional modules.
- **Master Password Encryption**: Protect your server credentials with AES-256 (Fernet) encryption.
- **Smart Ping (One-Shot)**: Instantly see which servers are online/offline upon opening or returning to the app.
- **Group Management**: Categorize servers (e.g., Production, Dev, Personal) and filter views.
- **Midnight Commander Automation**: Open `mc` already logged into your remote server using `setsid` and `SSH_ASKPASS`.
- **System Sync**: Automatically manages your `~/.ssh/config` file for easy CLI access (e.g., `ssh myserver`).
- **Instant Search**: Filter through dozens of servers in real-time.

---

## 💻 Platform Support

### 🐧 Linux
Full native support for all features.
- **Prerequisites**: `sshpass`, `mc`, `util-linux` (for `setsid`).
- **Install**: `sudo apt install sshpass mc util-linux -y` (Debian/Ubuntu).

### 🍎 macOS
Full support (requires Homebrew).
- **Prerequisites**: `sshpass`, `midnight-commander`. Note: macOS already includes most TTY tools.
- **Install**: 
  ```bash
  brew tap esolitos/ipa
  brew install sshpass mc
  ```

### 🪟 Windows
Supported via **WSL (Windows Subsystem for Linux)**.
- **Why WSL?**: This app relies on Unix-native TTY handling and `setsid`. For the best experience, run it within an Ubuntu or Debian WSL instance.
- **Install (Inside WSL)**: `sudo apt update && sudo apt install sshpass mc util-linux -y`.

---

## 📦 Installation

1. **Clone and Enter Directory**:
   ```bash
   cd sshconnect
   ```

2. **Setup Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Grant Execution Permissions**:
   ```bash
   chmod +x sshc
   ```

---

## ⌨️ How to Use

Simply run the shortcut:
```bash
./sshc
```

### Keyboard Shortcuts
| Key | Action |
| :--- | :--- |
| **`ENTER`** | Connect via Standard SSH |
| **`m`** | Open Midnight Commander (MC) |
| **`c`** | Execute Quick Command Snippet |
| **`g`** | Cycle through Groups |
| **`/`** | Search / Filter by Name or IP |
| **`a`** / **`e`** | Add or Edit Connection |
| **`d`** | Delete selected connection |
| **`q`** | Exit |

---

## 📁 Project Structure

```text
sshconnect/
├── main.py              # Entry point
├── sshc                 # Bash launcher
├── modules/
│   ├── app.py           # TUI Logic & Loop
│   ├── network.py       # SSH, MC & Ping logic
│   ├── security.py      # AES Encryption & Master Pass
│   ├── storage.py       # JSON & SSH Config management
│   ├── ui.py            # Visual components & Menus
│   ├── utils.py         # Terminal & TTY helpers
│   └── constants.py     # Paths and markers
```

---

## 🔒 Security & Privacy

- **Data Privacy**: All passwords are encrypted using PBKDF2 key derivation.
- **Permissions**: Sensitive files are automatically locked to `chmod 600`.
- **Transparency**: Temporary auth scripts are deleted immediately after connection.

---

## 📄 License

Created for system administrators and power users. Feel free to fork and customize!
