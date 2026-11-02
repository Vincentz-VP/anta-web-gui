
---

# 🚀 Arista ANTA Web GUI

 Web Dashboard built with **Streamlit** that simplifies network test automation using the **Arista ANTA** (Arista Network Test Automation) framework.

This project enables network engineers to design, build, and execute Network Ready For Use (**NRFU**) validation suites across Arista EOS infrastructure without writing a single line of Python code or YAML manually.

---

## 🌟 Key Features

* **📋 Dynamic Test Catalog Builder:**
* Interactive UI to select and configure predefined ANTA tests (Hardware, Interfaces, BGP, EVPN, VXLAN, MLAG, STP, System, and more).
* Real-time generation and auto-saving of valid `catalog.yml` files.
* Native support for dynamic `VerifyRunningConfig` rules with custom match conditions.

* **📂 Device catalog directory:**
* Run pre-generated per-device ANTA catalogs from a folder (`<hostname>.json` or `.yaml`).
* Matches the layout produced by [Arista AVD `anta_runner`](https://avd.arista.com/latest/docs/installation/anta/index.html) (`avd/anta/avd_catalogs/`).
* Configure with the **Device Catalogs** tab or set `ANTA_DEVICE_CATALOGS_DIR` (also accepts `AVD_CATALOGS_DIR`).


* **🎯 Test Profile Presets:**
* Switch between testing profiles on the fly (e.g., *Basic NRFU Quick Check*, *Deep NRFU Full Audit*).
* Create, edit, and persist custom profiles saved directly into settings.


* **🌐 Real-Time Inventory Management:**
* Interactive tables to define targets by specific **Hosts**, **Subnets (CIDR)**, or **IP Ranges**.
* Dynamic metadata tagging and eAPI parameter configuration.


* **📊 Interactive Results Dashboard:**
* High-level metrics summary (Pass, Fail, Errors).
* Direct device-level failure grouping with detailed error messages.


* **🛠️ Ad-Hoc EOS Command Runner:**
* Built-in debugging CLI tab to run direct eAPI commands (`show mac address-table`, etc.) against managed devices and visualize structured JSON tables.


* **🐳 Fully Dockerized Environment:**
* Clean, reproducible deployment powered by Docker & Docker Compose.



---

## 🛠️ Tech Stack

* **Frontend / UI:** Python, Streamlit, Pandas
* **Core Framework:** Arista ANTA (`anta`)
* **Configuration & Storage:** PyYAML, JSON
* **Containerization:** Docker (Python 3.11 Slim)

---

## 🚀 Quick Start

### Prerequisites

* Docker installed on your host system.
* Access to Arista switches with eAPI enabled.

### Installation & Run

1. **Clone the repository:**
```bash
git clone https://github.com/YonatanPorat/anta-web-gui.git
cd anta-web-gui

```


2. **Build and start the container:**
```bash
chmod +x restart.sh
./restart.sh

```

3. **Access the Web Dashboard:**
Open your browser and navigate to `http://localhost:8501`.

---

## 📂 Project Structure

```text
├── app.py                 # Main Streamlit Dashboard Application
├── device_catalog_dir.py  # Per-device catalog directory NRFU runner
├── Dockerfile             # Container build specifications
├── restart.sh             # Automation script for container rebuilds
├── entrypoint.sh          # Docker initialization script
├── inventory.yml          # Auto-generated ANTA Inventory
└── .gitignore             # Git exclusion rules

```

### Device catalog directory (Docker)

Mount a read-only directory of per-device catalog files and point the app at it:

```bash
docker run -p 8501:8501 \
  -e ANTA_DEVICE_CATALOGS_DIR=/catalogs \
  -v /path/to/avd/anta/avd_catalogs:/catalogs:ro \
  anta-web-gui
```

Inventory host **names** must match catalog filenames (e.g. `leaf1.json` → host name `leaf1`).
