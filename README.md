![Screenshot 4](assets/screenshot4.png)
# PersonaAI  

## Description

PersonaAI is a command-line and web-based tool designed to perform psychological profiling of individuals based on their Facebook ID. Leveraging advanced AI technology and the People Search IRBIS API, PersonaAI provides valuable insights for marketers and OSINT (Open Source Intelligence) enthusiasts. The tool supports both Command Line Interface (CLI) and User Interface (UI) versions.

## Features

- **Psychological Profiling:** Generate AI-based psychological profiles from Facebook IDs.
- **Export to PDF:** Export detailed profiles to PDF for easy sharing and archiving.
- **CLI and UI Versions:** Available as a command-line tool and a web-based application.
- **IRBIS API Integration:** Utilizes IRBIS API services for data retrieval and analysis.

## Prerequisites

- Python 3.6 or higher
- Git (for version control)
- Access to IRBIS API with a valid API key

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

4. **Install `reportlab` Dependency:**
    - Download the pre-built `reportlab` wheel file from the repository or a provided link.
    - Install the `reportlab` package using the downloaded wheel:
      ```powershell
      pip install .\windows_dependencies\reportlab-4.2.2-py3-none-any.whl
      ```

5. **Install Remaining Dependencies:**
    - After installing the `reportlab` wheel, install the remaining dependencies from `requirements.txt`:
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

## Video Tutorial

For a step-by-step guide on how to install and use PersonaAI, watch the video tutorial below:

[![PersonaAI Video Tutorial](https://img.youtube.com/vi/n_nUhYlrww4/hqdefault.jpg)](https://www.youtube.com/watch?v=n_nUhYlrww4)

Click the image above to watch the tutorial on YouTube.
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

## Screenshots

![Screenshot 1](assets/screenshot1.png)
![Screenshot 2](assets/screenshot2.png)
![Screenshot 3](assets/screenshot3.png)

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
