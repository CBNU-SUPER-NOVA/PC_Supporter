# PC Supporter: A Powerful Tool for Your Computer Needs

[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/CBNU-SUPER-NOVA/PC_Supporter?tab=MIT-1-ov-file)
[![Contributors](https://img.shields.io/badge/contributions-welcome-green)](https://github.com/CBNU-SUPER-NOVA/PC_Supporter/issues)
[![Python version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![WxPython version](https://img.shields.io/badge/wxPython-4.2.1-blue)](https://wxpython.org/)
[![openai version](https://img.shields.io/badge/openai-1.51.2-blue)](https://openai.com/index/openai-api/)
[![google-generativeai version](https://img.shields.io/badge/google_generativeai-0.8.3-blue)](https://github.com/google/generative-ai-python)
[![Release](https://img.shields.io/badge/release-NotYet-blue)](http://notyet.need.to.add.link)

<a href="#Introduction">Introduction</a> •
<a href="#Features">Features</a> •
<a href="#Project-Structure">Project Structure</a> •
<a href="#Getting-Started">Getting Started</a> •
<a href="#How-to-Use">How to Use</a> •
<a href="#Contributing">Contributing</a> •
<a href="#License">License</a> •
<a href="#Contact">Contact</a>

## Introduction

PC Supporter is an all-in-one utility designed to assist users with a variety of computer maintenance tasks. This program allows you to manage computer files through conversation with AI for simple, complex, and repetitive tasks in your local computer environment, and helps you manage files with a single button when you create WorkFlow by connecting continuous codes. Whether you need to perform routine maintenance or tackle specific problems, PC Supporter has the tools you need.

## Features

### 1. AI-Based File Management

PC Supporter allows users to manage files using conversational AI, making it easy to handle:

- File search, copy, move, and delete tasks
- Batch operations for repetitive tasks
- Creating automated workflows by chaining commands

### 2. Workflow Automation

- **Custom Workflows**: Create custom workflows that allow for the automation of multi-step processes with a single button.
- **Task Scheduling**: Set up automated schedules to handle routine maintenance tasks, such as file backups or disk cleanup.

Provides a comprehensive summary of your computer's hardware and software specifications, including:

### 3. User-Friendly Interface

Designed with simplicity in mind, the interface provides:

- A conversational interface for easy interaction with the AI
- Visual elements like graphs and progress indicators to show system health
- Step-by-step guidance for creating workflows and managing system tasks

## Project Structure

PC Supporter is organized into several key components:

1. **User Interface**: Provides a user-friendly graphical interface that allows users to interact with the system intuitively. This includes a conversational interface for issuing commands and visual elements for tracking system status.

2. **AI Command Interpretation**: This module interprets user commands, utilizing natural language processing to translate conversational inputs into executable tasks.

3. **Task Execution Module**: Handles the actual execution of user commands, whether they involve file management, workflow automation, or other system tasks.

4. **Database Management**: Manages persistent data storage, including workflow configurations, user preferences, and system logs.

### ERD

<img width="471" alt="스크린샷 2024-10-17 오전 1 56 22" src="https://github.com/user-attachments/assets/9c7b695e-8a5b-4939-9116-6b9d9c31ff01" width="120%" height="120%" />

### System Architecture

<img width="973" alt="스크린샷 2024-10-17 오전 4 32 23" src="https://github.com/user-attachments/assets/de02f4dc-7429-4e42-bc0f-b0d0cb4be2f9" width="70%" height="70%" />

## Getting Started

### Installation

1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/PC-Supporter/PC_Supporter.git
   ```
2. Navigate to the project directory:
   ```sh
   cd PC_Supporter
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### System Requirements

- **Operating System**: Windows 10 or higher, macOS
- **Python**: Python 3.12+
- **Additional Dependencies**: Please refer to `requirements.txt` for all required packages

## How to Use

1. **Launch PC Supporter**: Run the program using:
   ```sh
   python -m gui.main
   ```
2. **Explore Features**: Use the sidebar to navigate through different utilities such as AI-based File Management, Performance Optimizer, and Workflow Automation.
3. **Schedule Tasks**: You can set up automated system maintenance tasks like file backups and disk cleanup using the built-in scheduler.

## Contributing

We welcome contributions from the community! Please refer to [`CONTRIBUTING.md`](https://github.com/CBNU-SUPER-NOVA/PC_Supporter/blob/main/CONTRIBUTING.md) for more details on how to get involved in this project.

## License

This project is licensed under the MIT License. See the [`LICENSE`](https://github.com/CBNU-SUPER-NOVA/PC_Supporter?tab=MIT-1-ov-file) file for more information.

## Contact

If you have any questions, feel free to reach out to us:

- **Email**:
  - Park Sangjun: wns1169@gmail.com
  - Seo Beomsu: beom710@naver.com
  - Lee Hyungjin: gudwls2777@naver.com
  - Choi GaEun: chb7562@gmail.com
- **GitHub Issues**: [Issues Page](https://github.com/CBNU-SUPER-NOVA/PC_Supporter/issues)
