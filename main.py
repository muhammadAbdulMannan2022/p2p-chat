#!/usr/bin/env python3
import sys
from p2p_chat import P2PChat

def main():
    print("🔥 Smart P2P CLI Chat")
    print("🚫 No server. No tracking. No history.")
    print("-" * 40)
    print("[1] Listen for connection")
    print("[2] Connect to peer")
    print("[3] Exit")
    
    try:
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            port = input("Port (default 8080): ").strip()
            port = int(port) if port else 8080
            
            chat = P2PChat()
            chat.listen(port)
            
        elif choice == "2":
            host = input("Enter peer IP: ").strip()
            port = input("Enter port (default 8080): ").strip()
            port = int(port) if port else 8080
            
            if not host:
                print("[!] IP address required")
                return
                
            chat = P2PChat()
            chat.connect(host, port)
            
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
            
        else:
            print("[!] Invalid option")
            
    except KeyboardInterrupt:
        print("\n[*] Exiting...")
        sys.exit(0)
    except ValueError:
        print("[!] Invalid port number")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
