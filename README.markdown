# P2P CLI Chat Application

A secure, serverless peer-to-peer (P2P) chat application written in Python. This application allows two users to communicate directly over a TCP connection, with messages encrypted using the `cryptography` library. It supports both local network and internet-based communication, with automatic port forwarding via UPnP for ease of use.

**Features**:

- End-to-end encrypted messages using Fernet (symmetric encryption).
- No server or message history, ensuring privacy.
- Displays peer IP addresses for sent and received messages.
- Automatic port forwarding with UPnP for internet connectivity.
- Simple command-line interface (CLI) for ease of use.
- Supports `/quit`, `/exit`, `/q` to exit and `/clear` to clear the screen.

## Prerequisites

- **Python 3.6+**: Ensure Python is installed on your system.
- **Dependencies**:
  - `cryptography`: For message encryption.
  - `miniupnpc`: For automatic port forwarding (optional for internet use).
- **Operating System**: Windows, Linux, or macOS.
- **Network**: For internet use, your router must support UPnP (enabled by default on most modern routers) or allow manual port forwarding.

## Installation

### Clone the Repository

1. Open a terminal (Linux/macOS) or Command Prompt/PowerShell (Windows).
2. Clone the repository:

   ```bash
   https://github.com/muhammadAbdulMannan2022/p2p-chat.git
   cd p2p-chat
   ```


### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

1. **Start the Application**:

   - Run the main script:

     ```bash
     python main.py
     ```
   - You’ll see a menu:

     ```
     🔥 Smart P2P CLI Chat
     🚫 No server. No tracking. No history.
     ----------------------------------------
     [1] Listen for connection
     [2] Connect to peer
     [3] Exit
     ```

2. **Listen for Connections** (Option 1):

   - Choose option `1` to start listening for incoming connections.
   - Enter a port number (default: `8080`) or press Enter to use the default.
   - The application will:
     - Attempt to forward the port using UPnP.
     - Display your public IP (e.g., `203.0.*.*`) and port.
     - Wait for a peer to connect.
   - Share the public IP and port with the peer who will connect to you.
   - Example output:

     ```
     Select option: 1
     Port (default 8080): 8080
     [*] UPnP: Port 8080 forwarded successfully
     [*] Your public IP: 203.0.*.*
     [*] Listening on 0.0.0.0:8080
     [*] Share your public IP (203.0.*.*) and port 8080 with peer to connect
     [*] Waiting for connection...
     ```

3. **Connect to a Peer** (Option 2):

   - Choose option `2` to connect to a listening peer.
   - Enter the peer’s public IP or hostname (e.g., `203.0.*.*`) and port (e.g., `8080`).
   - If the connection succeeds, you can start chatting.
   - Example output:

     ```
     Select option: 2
     Enter peer IP or hostname: 203.0.*.*
     Enter port (default 8080): 8080
     [*] Received key length: 44 bytes
     [+] Received encryption key from peer
     [+] Connected to peer 203.0.*.*:8080
     [*] Chat started. Type /quit to exit
     ```

4. **Chatting**:

   - Type messages and press Enter to send.
   - Sent messages are prefixed with your local IP (e.g., `[192.168.*.*] hello`).
   - Received messages are prefixed with the peer’s IP (e.g., `[198.51.*.*] hi`).
   - Use `/quit`, `/exit`, or `/q` to exit the chat.
   - Use `/clear` to clear the screen.

5. **Exit** (Option 3):

   - Choose option `3` to exit the application.

### Example Chat Session

**Listener**:

```
[+] Connected to peer 198.51.100.2:54321
[*] Sent key length: 44 bytes
[*] Chat started. Type /quit to exit

> hello
[192.168.100.1] hello
> 
[*] Received 64 bytes of encrypted data
[198.51.100.2] Hi from outside!
> /quit
[*] UPnP: Port 8080 mapping removed
[*] Connection closed. No trace left.
```

**Connector**:

```
[*] Received key length: 44 bytes
[+] Received encryption key from peer
[+] Connected to peer 203.0.*.*:8080
[*] Chat started. Type /quit to exit

> Hi from outside!
[192.168.1.101] Hi from outside!
> 
[*] Received 64 bytes of encrypted data
[203.0.*.*] hello
> /quit
[*] Connection closed. No trace left.
```

## Network Configuration for Internet Use

To use the application over the internet (outside your local network), the listener must be reachable via their router’s public IP. The application uses UPnP to automatically forward ports, but manual port forwarding may be required if UPnP fails.

### Automatic Port Forwarding with UPnP

- **How It Works**:
  - When you select the "Listen" option and enter a port (e.g., `8080`), the application uses the `miniupnpc` library to:
    - Discover your router.
    - Retrieve your public IP (e.g., `203.0.*.*`).
    - Forward the specified port to your device’s local IP (e.g., `192.168.1.100:8080`).
  - The public IP and port are displayed for you to share with the peer.
- **Requirements**:
  - Your router must support UPnP and have it enabled (default on most modern routers).
  - Check your router’s admin interface (e.g., `192.168.1.1`) under “Advanced,” “NAT,” or “Port Forwarding” to enable UPnP.
- **If UPnP Fails**:
  - The application will display:

    ```
    [!] No UPnP-capable router found. Manual port forwarding required.
    ```
  - Follow the manual port forwarding instructions below.

### Manual Port Forwarding

If UPnP is unavailable or fails, you must manually forward the port on your router to allow incoming connections.

#### Find Your Local IP

- **Linux**:

  ```bash
  ip addr show | grep inet
  ```

  Look for your local IP (e.g., `192.168.1.100`) under your network interface (e.g., `wlan0` or `eth0`).
- **Windows**:

  ```cmd
  ipconfig
  ```

  Look for “IPv4 Address” under your active network adapter (e.g., `192.168.1.100`).

#### Find Your Public IP

- Visit `whatismyipaddress.com` or run:

  ```bash
  curl ifconfig.me
  ```
- Share this public IP (e.g., `203.0.*.*`) with the peer.

#### Configure Port Forwarding

1. **Access Your Router**:
   - Open a browser and go to your router’s admin interface (e.g., `192.168.1.1` or `192.168.0.1`).
   - Log in with your admin credentials (check your router’s manual or sticker for defaults).
2. **Navigate to Port Forwarding**:
   - Look for a section like “Port Forwarding,” “Virtual Servers,” or “NAT.”
3. **Add a Port Forwarding Rule**:
   - **External Port**: The port you chose (e.g., `8080`).
   - **Internal IP**: Your device’s local IP (e.g., `192.168.1.100`).
   - **Internal Port**: Same as the external port (e.g., `8080`).
   - **Protocol**: TCP.
   - **Description**: “P2P Chat” (optional).
4. **Save and Apply**:
   - Save the settings and restart your router if required.
5. **Verify the Port**:
   - Use `canyouseeme.org` to check if the port is open on your public IP.

#### Open Firewall Ports

Ensure your device’s firewall allows incoming TCP connections on the chosen port.

- **Linux**:

  ```bash
  sudo ufw allow 8080/tcp
  sudo ufw status
  ```
- **Windows**:
  1. Open Windows Defender Firewall with Advanced Security.
  2. Create a new inbound rule:
     - Type: Port
     - Protocol: TCP
     - Specific Ports: 8080
     - Action: Allow the connection
     - Profile: All
     - Name: “P2P Chat”
  3. Save and apply the rule.

### Testing

1. **Local Network Test**:

   - Run the listener on one device: `python main.py`, select option 1, use port `8080`.
   - Run the connector on another device in the same network: `python main.py`, select option 2, enter `127.0.0.1` and port `8080`.
   - Send messages to verify two-way communication.

2. **Internet Test**:

   - Run the listener on your device and note the public IP and port.
   - Share the public IP and port with a peer outside your network.
   - Have the peer run the connector with your public IP and port.
   - Test sending and receiving messages.

3. **Debugging**:

   - If you can’t connect, check for errors like:
     - `[!] UPnP: Failed to forward port`: Enable UPnP or manually forward the port.
     - `[!] Connection timed out`: Verify the public IP and port; test with `telnet <public_ip> 8080`.
     - `[!] Receive error: TimeoutError`: Ensure the peer’s firewall allows outgoing TCP traffic on the port.
   - Check debug messages like `[*] Received X bytes of encrypted data` to confirm data is arriving.

## Security Notes

- **Encryption**: Messages are encrypted with Fernet, but the encryption key is sent in plaintext during the initial connection. For production use, implement a secure key exchange protocol (e.g., Diffie-Hellman).
- **UPnP Security**: UPnP can pose security risks if misused. Ensure only trusted applications use it, and disable it when not needed.
- **Dynamic IPs**: If your public IP changes frequently, consider using a Dynamic DNS (DDNS) service (e.g., No-IP) to provide a stable hostname.
- **Firewall**: Always configure your firewall to allow only the necessary ports.

## Troubleshooting

- **Connection Refused**:
  - Ensure the listener is running and the port is forwarded (via UPnP or manually).
  - Verify the public IP and port with `canyouseeme.org`.
- **Messages Not Received**:
  - Check debug logs for `[*] Received X bytes of encrypted data`.
  - Ensure the peer’s firewall allows outgoing TCP traffic on the port.
  - Verify the encryption key exchange (`[*] Sent key length: 44 bytes` and `[*] Received key length: 44 bytes`).
- **UPnP Fails**:
  - Enable UPnP in your router’s admin interface.
  - Manually forward the port as described above.
- **Dynamic IP Changes**:
  - Use a DDNS service and enter the hostname in the connector.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.