
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

* **📂 Device catalog directory (profile):**
* When `ANTA_DEVICE_CATALOGS_DIR` is set, a built-in sidebar profile runs pre-generated per-device catalogs (`<hostname>.json` or `.yaml`).
* Matches [Arista AVD `anta_runner`](https://avd.arista.com/latest/docs/installation/anta/index.html) output (`avd/anta/avd_catalogs/`). Description via `ANTA_CATALOG_PROFILE_DESCRIPTION`.
* Execute from the **Dashboard** like other profiles (no separate tab).


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

Optional tuning (environment variables):

| Variable | Default | Meaning |
|---|---|---|
| `ANTA_DEVICE_CATALOG_WORKERS` | `4` | Devices run in parallel |
| `ANTA_DEVICE_CATALOG_TIMEOUT` | `300` | Seconds per device before it is marked as an error (capped by the global NRFU timeout) |
| `ANTA_DEVICE_CATALOG_ENABLE` | off | Set to `1` to pass `--enable` to `anta nrfu` for these runs |

AVD catalogs that inspect running configuration or run privileged commands need
`-e ANTA_DEVICE_CATALOG_ENABLE=1`. This remains opt-in for other deployments.

### Credential defaults

Set `ANTA_USERNAME` and `ANTA_PASSWORD` to seed credentials for a new browser.
Credentials saved in the GUI take precedence; without these variables the
defaults remain `admin` / `admin`.

### Regression checks

With the application dependencies installed, run:

```bash
python -m unittest discover -s tests -v
```

These checks use temporary browser settings and do not contact any devices.

