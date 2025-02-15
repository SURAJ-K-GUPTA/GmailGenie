# GmailGenie

Welcome to **GmailGenie**! ✨ This tool automates the process of creating Gmail accounts using Python, seamlessly integrating with SMS activation services and CAPTCHA solvers to make the account creation process quicker and more efficient.

![GmailGenie](GmailGenieRed.png?raw=true)
---

## Features 🚀

- **Automated Gmail Account Creation**: Automatically create Gmail accounts with minimal input.
- **SMS Activation**: Support for SMS activation services like [JuicySMS](https://juicysms.com/).
- **CAPTCHA Solving**: Integration with [2Captcha](https://2captcha.com/) to bypass CAPTCHA challenges.
- **Proxy Support**: Enables the use of proxies for IP rotation, ensuring smooth, anonymous operations.
- **Modular Design**: Well-structured codebase for easy maintenance and contribution.

---

## File Structure 📂

```
GmailGenie/
├── .gitignore
├── README.md
├── chromedriver.exe
├── config.py
├── main.py
├── phone_verification.py
├── recaptcha_solver.py
├── requirements.txt
├── signup_helpers.py
├── signup_process.py
├── user_details.py
└── .env
```

---

## Setup 🛠️

### Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.8 or higher** 📌
- **ChromeDriver** (for browser automation)
- **API keys for**:
  - [2Captcha](https://2captcha.com/)
  - [JuicySMS](https://juicysms.com/)

### Installation 🔧

1. **Clone the Repository**:

```bash
git clone https://github.com/SURAJ-K-GUPTA/GmailGenie.git
cd GmailGenie
```

2. **Create a Virtual Environment**:

```bash
python -m venv venv
```

3. **Activate the Virtual Environment**:

- On **Windows**:

```bash
venv\Scripts\activate
```

- On **macOS/Linux**:

```bash
source venv/bin/activate
```

4. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

5. **Create a `.env` File**:

In the root directory, create a `.env` file and add your API keys and proxy details:

```
TWO_CAPTCHA_API_KEY=your_two_captcha_api_key_here
JUICYSMS_API_KEY=your_juicysms_api_key_here
PROXY_HOST=your_proxy_host_here
PROXY_PORT=your_proxy_port_here
PROXY_USER=your_proxy_username_here
PROXY_PASS=your_proxy_password_here
```

6. **Download ChromeDriver**:

- [Download ChromeDriver here](https://sites.google.com/a/chromium.org/chromedriver/).
- Place the `chromedriver.exe` file in the root directory of the project.

---

## Usage 🎬

To begin the Gmail account creation process, simply run the `main.py` script:

```bash
python main.py
```

---

## Contributing 🤝

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to your branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgments 🙏

- **2Captcha** for CAPTCHA solving service.
- **JuicySMS** as an alternative SMS activation provider.

---

Now you're ready to start automating Gmail account creation with GmailGenie! Happy coding! 🧙‍♂️✨

If you encounter any issues, feel free to open an issue on this repository or reach out for help.
