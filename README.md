<p align="center">
    <img src="./assets/spyhole.png" align="center" width="30%">
</p>
<p align="center"><h1 align="center">OLHO_MAGICO</h1></p>
<p align="center">
	<em>See All, Know All, Secure All</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/dornelles08/olho_magico?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/dornelles08/olho_magico?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/dornelles08/olho_magico?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/dornelles08/olho_magico?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

## Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

## Overview

Project developed with the goal of functioning as a smart peephole using the ESP32-CAM. It enables person detection and facial recognition, with the option to upload known faces to its database.

Alternatively, it can be used as a standalone application for person detection or facial recognition, just implementing a function do get images from another source against the camera.

---

## Features

|     |      Feature      | Summary                                                                                                                                                                                                                                                                                                                                                                                |
| :-- | :---------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ⚙️  | **Architecture**  | <ul><li>Monolithic architecture with multiple components (e.g., `person_detection.py`, `face_detection_recognition.py`) interacting through HTTP endpoints.</li><li>Use of Python as the primary language.</li><li>Utilization of popular frameworks and libraries such as FastAPI, OpenCV, face_recognition, and PyTorch.</ul>                                                        |
| 🔩  | **Code Quality**  | <ul><li>Adherence to PEP 8 coding standards (e.g., consistent indentation, naming conventions).</li><li>Use of type hints and annotations (e.g., `person_detection.py` uses `annotated-types`).</ul>                                                                                                                                                                                   |
| 📄  | **Documentation** | <ul><li>Clear documentation for dependencies in `requirements.txt` file.</li><li>Reference to the primary language as Python with a specific version count.</ul>                                                                                                                                                                                                                       |
| 🔌  | **Integrations**  | <ul><li>Integration of multiple camera feeds using HTTP endpoints.</li><li>Use of IP cameras through HTTP endpoints in `person_detection.py` file.</li><li>Face recognition and detection system utilizing OpenCV and face_recognition libraries.</ul>                                                                                                                                 |
| 🧩  |  **Modularity**   | <ul><li>Separation of concerns with distinct components (e.g., `person_detection.py`, `face_detection_recognition.py`) handling specific tasks.</li><li>Use of functions to encapsulate image download and saving logic (`functions/download_image.py` and `functions/save_image.py`).</li><li>Modular design enables efficient setup and deployment across various environments.</ul> |
| 📊  |  **Performance**  | <ul><li>Utilization of popular libraries for computer vision tasks (e.g., OpenCV, face_recognition).</li><li>Use of PyTorch for image processing and analysis.</li><li>Optimized code structure for efficient execution and performance.</ul>                                                                                                                                          |
| 🚀  |  **Scalability**  | <ul><li>Designated directory for storing known faces in `receve_known_faces.py` file.</li><li>Use of timestamped filenames for saved images (`functions/save_image.py`).</li><li>Modular architecture enables easy addition or removal of components without affecting the overall system.</ul>                                                                                        |

---

## Project Structure

```sh
└── olho_magico/
    ├── README.md
    ├── exemplo.env
    ├── face_detection_recognition.py
    ├── functions
    │   ├── download_image.py
    │   └── save_image.py
    ├── person_detection.py
    ├── receve_known_faces.py
    └── requirements.txt
```

### Project Index

<details open>
	<summary><b><code>OLHO_MAGICO/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/dornelles08/olho_magico/blob/master/person_detection.py'>person_detection.py</a></b></td>
				<td>Here's a succinct summary of the main purpose and use of the `person_detection.py` file:

"Monitors cameras for person detection using YOLO model, enabling automatic people detection, logging, image saving, and integration with IP cameras through HTTP endpoints."</td>

</tr>
<tr>
<td><b><a href='https://github.com/dornelles08/olho_magico/blob/master/face_detection_recognition.py'>face_detection_recognition.py</a></b></td>
<td>- The `face_detection_recognition.py` file implements a face detection and recognition system using OpenCV and face_recognition libraries<br>- It detects faces in images from a camera endpoint, matches them against known faces, and logs detection events<br>- The system can also save detected face images and is configurable for check intervals.</td>
</tr>
<tr>
<td><b><a href='https://github.com/dornelles08/olho_magico/blob/master/receve_known_faces.py'>receve_known_faces.py</a></b></td>
<td>- Stores and validates images of known faces via API REST endpoints, ensuring secure upload and storage in a designated directory with unique file names based on person name and timestamp<br>- This module provides a FastAPI server for uploading face images, validating their format, and saving them to the specified directory.</td>
</tr>
</table>
</blockquote>
</details>
<details> <!-- functions Submodule -->
<summary><b>functions</b></summary>
<blockquote>
<table>
<tr>
<td><b><a href='https://github.com/dornelles08/olho_magico/blob/master/functions/download_image.py'>download_image.py</a></b></td>
<td>- Downloads images from camera endpoints via HTTP, converting the response into a numpy array for further processing<br>- This module provides error handling during the download process and utilizes dependencies such as numpy, requests, and opencv-python to achieve its functionality<br>- It is designed to be used in conjunction with other components of the project, which aims to integrate multiple camera feeds and provide real-time image processing capabilities.</td>
</tr>
<tr>
<td><b><a href='https://github.com/dornelles08/olho_magico/blob/master/functions/save_image.py'>save_image.py</a></b></td>
<td>Here's a succinct summary of the main purpose and use of the provided code file:

"Handles image saving functionality by storing processed images on disk with timestamped filenames, maintaining a temporal record of saved images."

(Note: I've kept it concise within the 50-70 word limit while avoiding technical implementation details.)</td>

</tr>
</table>
</blockquote>
</details>

</details>

---

## Getting Started

### Prerequisites

Before getting started with olho_magico, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip

### Installation

Install olho_magico using one of the following methods:

**Build from source:**

1. Clone the olho_magico repository:

```sh
❯ git clone https://github.com/dornelles08/olho_magico
```

2. Navigate to the project directory:

```sh
❯ cd olho_magico
```

3. Install the project dependencies:

**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```

### Usage

Run olho_magico using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

It can be executed in two ways: for person detection or facial recognition:

- For person detection:

```sh
❯ python person_detection.py
```

- For face recognition:

```sh
❯ python face_detection_recognition.py
```

And to receve the know faces run the api:

```sh
❯ python receve_known_faces.py
```

### ⚙️ Configuration

You can adjust the following parameters in `.env` file:

- CAMERA_ENDPOINT: The URL of the ESP32-CAM to retrieve images.
- CHECK_INTERVAL_SECONDS: The interval (in seconds) at which the script checks for new images.

---

## Project Roadmap

- [x] **`Script Person Detection`**
- [x] **`Script Face Recognition`**
- [x] **`API to send know faces`**
- [ ] **`Configuration Docker`**
