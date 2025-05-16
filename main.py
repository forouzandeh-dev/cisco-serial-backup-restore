

import serial
import time
import os
import getpass


def main():
    print("====Cisco Serial Backup Restore Tool starting====")

    # --- Get COM Port------

    com_port = input("Enter COM port (e.g, COM3): ").strip()

    # ---Get Config File Path--
    config_path = input(
        "Enter path to config file(e.g., default_config.txt): ").strip()
    username = input("Enter switch username: ").strip()
    password = getpass.getpass("Enter switch password: ")
    enable_password = getpass.getpass("Enter enable password: ")

    if not os.path.exists(config_path):
        print(f"❌File not found: {config_path}")
        return

    # --- Serial Settings ----

    baud_rate = 9600

    try:
        ser = serial.Serial(port=com_port, baudrate=baud_rate, timeout=3)
        time.sleep(2)
        print(f"\n✅Connected to {com_port} at {baud_rate} baud.\n")

        # -- Handle Login--
        print("⌛ Waiting for login prompt...\n")
        time.sleep(2)
        ser.write((username+'\r\n').encode('utf-8'))
        time.sleep(3)
        ser.write((password+'\r\n').encode('utf-8'))
        time.sleep(3)  # Give switch time to respond
        # --Enter enable mode----
        ser.write(b'enable\r\n')
        time.sleep(3)

        # if enable password is required
        ser.write((enable_password+'\r\n').encode('utf-8'))
        time.sleep(3)

        # ---Read the Switch response---
        response = ser.read(ser.in_waiting).decode(errors='ignore')
        print(f"\n📟 Switch response after login:\n{response}\n")
        if "Login invalid" in response or "Authentication failed" in response:
            print("❌ Login failed! Please check your username or password.")
            ser.close()
            return
        print("🔐 Login accepted.\n")

        # Enter config terminal
        ser.write(b'conf t\r\n')
        time.sleep(3)

    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")
        return

    try:
        # --send Config --
        with open(config_path, 'r') as file:
            lines = file.readlines()
            print(f"📤Sending {len(lines)} lines....\n")

            for line in lines:
                line = line.strip()
                if line:
                    ser.write((line + '\r\n').encode('utf-8'))
                    print(f">{line}")
                    time.sleep(0.5)

        print("\n✅ Config sent successfully.")

    except Exception as e:
        print(f"Error reading or sending file: {e}")

    finally:
        ser.close()
        print("Serial connection closed.")


if __name__ == "__main__":
    main()
