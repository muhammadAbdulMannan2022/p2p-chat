import socket
import threading
import sys
import os
import miniupnpc
from crypto_utils import encrypt, decrypt, generate_key

class P2PChat:
    def __init__(self):
        self.socket = None
        self.key = generate_key()
        self.running = False
        self.conn = None
        self.peer_addr = None
        self.local_ip = socket.gethostbyname(socket.gethostname())

    def setup_upnp(self, port):
        """Set up UPnP port forwarding and get public IP"""
        try:
            upnp = miniupnpc.UPnP()
            upnp.discoverdelay = 200
            discover_count = upnp.discover()
            if discover_count == 0:
                print("[!] No UPnP-capable router found. Manual port forwarding required.")
                return None, None
            
            upnp.selectigd()  # Select the Internet Gateway Device
            public_ip = upnp.externalipaddress()
            local_ip = upnp.lanaddr
            
            # Add port mapping (external port -> internal port)
            mapping_added = upnp.addportmapping(
                port,           # External port
                'TCP',          # Protocol
                local_ip,       # Internal IP
                port,           # Internal port
                'P2P Chat',     # Description
                ''              # Remote host (empty for any)
            )
            
            if mapping_added:
                print(f"[*] UPnP: Port {port} forwarded successfully")
                return public_ip, port
            else:
                print("[!] UPnP: Failed to forward port. Manual port forwarding required.")
                return public_ip, None
                
        except Exception as e:
            print(f"[!] UPnP Error: {type(e).__name__}: {str(e)}")
            return None, None

    def listen(self, port=8080):
        """Listen for incoming connections with automatic port forwarding"""
        try:
            # Set up UPnP port forwarding
            public_ip, forwarded_port = self.setup_upnp(port)
            if public_ip:
                print(f"[*] Your public IP: {public_ip}")
            if forwarded_port is None:
                print(f"[*] Please manually forward port {port} to {self.local_ip} on your router")
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('0.0.0.0', port))
            self.socket.listen(1)
            
            print(f"[*] Listening on 0.0.0.0:{port}")
            print(f"[*] Share your public IP ({public_ip or 'unknown'}) and port {port} with peer to connect")
            print(f"[*] Waiting for connection...")
            
            conn, addr = self.socket.accept()
            self.peer_addr = addr
            print(f"[+] Connected to peer {addr[0]}:{addr[1]}")
            
            # Send encryption key to peer
            conn.send(self.key)
            print(f"[*] Sent key length: {len(self.key)} bytes")
            print(f"[*] Chat started. Type /quit to exit\n")
            
            self.start_chat(conn)
            
        except Exception as e:
            print(f"[!] Error: {type(e).__name__}: {str(e)}")
        finally:
            # Clean up UPnP port mapping
            try:
                upnp = miniupnpc.UPnP()
                upnp.discover()
                upnp.selectigd()
                upnp.deleteportmapping(port, 'TCP')
                print(f"[*] UPnP: Port {port} mapping removed")
            except:
                pass
    
    def connect(self, host, port=8080):
        """Connect to a peer"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10-second timeout for connection
            self.socket.connect((host, port))
            self.peer_addr = (host, port)
            
            # Receive encryption key from peer
            self.key = self.socket.recv(4096)
            print(f"[*] Received key length: {len(self.key)} bytes")
            print(f"[+] Received encryption key from peer")
            print(f"[+] Connected to peer {host}:{port}")
            print(f"[*] Chat started. Type /quit to exit\n")
            
            self.start_chat(self.socket)
            
        except socket.timeout:
            print(f"[!] Connection timed out: Unable to reach {host}:{port}")
        except Exception as e:
            print(f"[!] Connection failed: {type(e).__name__}: {str(e)}")
    
    def start_chat(self, conn):
        """Start the chat session"""
        self.conn = conn
        self.running = True
        
        # Start receiver thread
        receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receiver_thread.start()
        
        # Main input loop
        try:
            while self.running:
                message = input("> ")
                
                if message.lower() in ['/quit', '/exit', '/q']:
                    break
                elif message.lower() == '/clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    continue
                elif message.strip() == '':
                    continue
                
                # Encrypt and send message
                encrypted = encrypt(message.encode('utf-8'), self.key)
                conn.send(encrypted)
                print(f"\r[{self.local_ip}] {message}")
                print("> ", end="", flush=True)
                
        except KeyboardInterrupt:
            print("\n[*] Interrupted by user")
        except Exception as e:
            print(f"\n[!] Error: {type(e).__name__}: {str(e)}")
        finally:
            self.cleanup()
    
    def receive_messages(self):
        """Receive and decrypt messages"""
        self.conn.settimeout(1.0)  # Set 1-second timeout for recv
        while self.running:
            try:
                data = self.conn.recv(4096)
                if not data:
                    print(f"\n[*] Peer {self.peer_addr[0]}:{self.peer_addr[1]} disconnected")
                    self.running = False
                    break
                print(f"[*] Received {len(data)} bytes of encrypted data")  # Debug log
                
                # Decrypt message
                decrypted = decrypt(data, self.key)
                try:
                    message = decrypted.decode('utf-8')
                except UnicodeDecodeError:
                    print("\n[!] Received invalid message data")
                    continue
                
                # Print message with peer's IP
                print(f"\r[{self.peer_addr[0]}] {message}")
                print("> ", end="", flush=True)
                
            except socket.timeout:
                continue
            except ConnectionResetError:
                if self.running:
                    print(f"\n[!] Peer {self.peer_addr[0]}:{self.peer_addr[1]} unexpectedly disconnected")
                break
            except ConnectionError:
                if self.running:
                    print("\n[!] Network error occurred")
                break
            except Exception as e:
                if self.running:
                    print(f"\n[!] Receive error: {type(e).__name__}: {str(e)}")
                break
    
    def cleanup(self):
        """Clean up resources and wipe memory"""
        self.running = False
        
        if self.conn:
            self.conn.close()
        if self.socket:
            self.socket.close()
            
        # Wipe encryption key from memory
        self.key = b'\x00' * len(self.key)
        
        print("\n[*] Connection closed. No trace left.")
        sys.exit(0)