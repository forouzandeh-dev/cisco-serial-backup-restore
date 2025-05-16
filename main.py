

import serial
import time
import os


def main():
    print("====Cisco Serial Backup Restore Tool starting====")

    # --- Get COM Port------

    com_port = input("Enter COM port (e.g, COM3): ").strip()

    # ---Get Config File Path--
    config_path = input(
        "Enter path to config file(e.g., default_config.txt): ").strip()

    if not os.path.exists(config_path):
        print(f"File not found: {config_path}")
        return

    # --- Serial Settings ----

    baud_rate = 9600

    try:
        ser = serial.Serial(port=com_port, baudrate=baud_rate, timeout=3)
        time.sleep(2)
        print(f"\nConnected to {com_port} at {baud_rate} baud.\n")

    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")
        return

    try:
        with open(config_path, 'r') as file:
            lines = file.readlines()
            print(f"Sending {len(lines)} lines....\n")

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
