# PersonaAI
    ____                                   ___    ____
   / __ \___  ______________  ____  ____ _/   |  /  _/
  / /_/ / _ \/ ___/ ___/ __ \/ __ \/ __ `/ /| |  / /  
 / ____/  __/ /  (__  ) /_/ / / / / /_/ / ___ |_/ /   
/_/    \___/_/  /____/\____/_/ /_/\__,_/_/  |_/___/   

## Description

PersonaAI is a command-line and web-based tool designed to perform psychological profiling of individuals based on their Facebook ID. Leveraging advanced AI technology and the People Search IRBIS API, PersonaAI provides valuable insights for marketers and OSINT (Open Source Intelligence) enthusiasts. The tool supports both Command Line Interface (CLI) and User Interface (UI) versions.

## Features

- Generate AI-based psychological profiles from Facebook IDs.
- Available in CLI and UI versions.
- Integrates with IRBIS API for data retrieval and analysis.
- Display information in various formats based on user preference.

## Prerequisites

- Python 3.6 or higher
- Git

## Installation

### Windows (PowerShell)

1. **Install Python**:
    - Download and install Python from [python.org](https://www.python.org/downloads/).
    - Verify the installation by running:
      ```powershell
      python --version
      ```

2. **Clone the Repository:**
    ```powershell
    git clone https://github.com/efiml/personaai.git
    cd personaai
    ```

3. **Set Up a Virtual Environment:**
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate
    ```

4. **Install Dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

### macOS

1. **Install Python**:
    - Download and install Python from [python.org](https://www.python.org/downloads/).
    - Verify the installation by running:
      ```bash
      python3 --version
      ```

2. **Clone the Repository:**
    ```bash
    git clone https://github.com/efiml/personaai.git
    cd personaai
    ```

3. **Set Up a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Linux

1. **Install Python**:
    - Install Python from your package manager.
    - Verify the installation by running:
      ```bash
      python3 --version
      ```

2. **Clone the Repository:**
    ```bash
    git clone https://github.com/efiml/personaai.git
    cd personaai
    ```

3. **Set Up a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Get Your API Key

1. **Register with IRBIS**:
    - Visit [IRBIS Registration Page](https://irbis.espysys.com/auth/register) and create an account.

2. **Choose a Subscription Package**:
    - Select the subscription package that best fits your needs.

3. **Navigate to the Developer Page**:
    - After logging in, go to the [Developer page](https://irbis.espysys.com/developer).

4. **Generate and Copy the API Key**:
    - Generate your API key and copy the value shown. Store it securely.

## Usage

### Command Line Interface (CLI)

1. **Show Available Commands**:
    ```bash
    python personaai.py -h
    ```

2. **Set API Key**:
    Replace `YOUR_API_KEY` with your actual API key.
    ```bash
    python personaai.py -k "YOUR_API_KEY"
    ```

3. **Show Current API Key**:
    ```bash
    python personaai.py -s
    ```

4. **Analyze a Facebook ID**:
    Replace `facebook_id` with the Facebook ID you want to analyze.
    ```bash
    python personaai.py -id "facebook_id"
    ```

5. **Enable Debug Mode**:
    ```bash
    python personaai.py -d
    ```

### User Interface (UI)

1. **Start the Application:**
    ```bash
    python app.py
    ```

2. **Open the Application in Your Browser:**
    Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## Notes

- Ensure Facebook IDs are valid and correctly formatted.
- The tool supports both CLI and UI interfaces.
- Use the `-d` option in CLI to enable debug mode and view raw data.

## Troubleshooting

If you encounter issues, ensure all dependencies are installed correctly, and you have a valid IRBIS API key. Check your environment setup if you experience problems.

## Dependencies

- Python 3.6 or higher
- `requests`
- `cryptography`
- `reportlab`
- `Flask`
- `Pillow`

Install dependencies using:
```bash
pip install -r requirements.txt
