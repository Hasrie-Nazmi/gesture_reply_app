# Gesture Reply 🤖✋

**Gesture Reply** is a desktop application built with **Python** and **Kivy** that leverages computer vision to recognize hand gestures in real-time and translate them into customizable, pre-set text replies. It features a dual-screen interface for real-time translation tracking and local configuration management.

---

## 🚀 Key Features

* **Real-Time Gesture Recognition:** Automatically captures webcam frames and processes hand gestures using a dedicated processor module.
* **Customizable Reply Mapping:** Assign custom text responses to specific gestures (Gesture 0–5, Thumbs Up) through an intuitive settings screen.
* **Persistent Configuration:** Automatically saves and loads your customized gesture replies locally via `config.json`.
* **Dynamic Text Assembly:** Append recognized gesture replies into a rolling text history box with built-in copy, delete, and clear utilities.
* **Reference Visual Guides:** Visual image guides corresponding to each gesture make configuration effortless.

---

## 🛠️ Tech Stack & Architecture

* **Framework:** Python, Kivy, Kivy Language (`.kv`)
* **Computer Vision / Processing:** OpenCV / MediaPipe via `GestureCameraProcessor`
* **Data Persistence:** JSON (`config.json`)
* **Architecture:** Multi-screen navigation (`MainScreen` & `ReplyEntry`) using Kivy's `ScreenManager`.

---

## 📁 Project Structure

```text
gesture_reply/
│
├── assets/                  # Reference gesture images (.jpg)
├── ui/                      # Kivy layout files (.kv)
│   ├── mainscreen.kv
│   └── replyentry.kv
│
├── src/                     # Python source files
│   ├── main.py              # Application entry point & ScreenManager
│   ├── main_screen.py       # Main camera feed & text generation logic
│   ├── reply_entry.py       # Configuration screen for gesture-to-text mapping
│   └── gesture_processor.py # Computer vision & gesture detection pipeline
│
├── config.json              # Local persistent configuration file
└── README.md
