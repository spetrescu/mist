# mist
Middleware for LLMs.

<div align="left">
   <p>
    <img width="200" alt="mist" src="https://github.com/user-attachments/assets/ce44265d-dac4-421c-9b77-583973d63d0b">
   </p>
   <p>
     <a href="">
       <img alt="First release" src="https://img.shields.io/badge/release-v0.0.0-darkgreen.svg" />
     </a>
   </p>
 </div>

## Features
- **Conversation History:** Persist and retrieve conversation histories using Memcached.
- **User Authentication:** Simple user authentication for secure access.
- **Multiple Client Support:** Supports multiple clients simultaneously with active thread management.

## Setup

### Prerequisites
1. **Memcached:** Ensure you have a running `memcached` instance. This is required for enabling conversation histories.
2. **Python Environment:** Python 3.x is required.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-repo/mist.git
cd mist
```
2. Set up a virtual environment:
```bash
python3 -m venv mist
source mist/bin/activate
```
3. Install the required Python packages:
```bash
pip install -e .
```
4. Start the Memcached server (if not already running):
```bash
memcached -d -m 1024 -l 127.0.0.1 -p 11211
```

## Starting the Server
To start the LLM server and load the model into memory, run:
```bash
python3 server_conversation_history_logging.py
```

## Starting the Client
In a new terminal instance, start a client session:
```bash
python3 client_session_conversation_history.py
```
Use the credentials `user1` and `password1` to authenticate.
