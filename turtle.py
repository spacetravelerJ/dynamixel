import time
from dynamixel_sdk import *

# --- Configurations ---
DEVICENAME          = '/dev/ttyACM0' # Port connected to OpenCR
BAUDRATE            = 1000000        # Default baudrate for TurtleBot3 (Try 57600 if it fails)
PROTOCOL_VERSION    = 2.0            # DXL Protocol 2.0 is used for X-series

# Address Table (XL430-W250)
ADDR_OPERATING_MODE = 11
ADDR_TORQUE_ENABLE  = 64
ADDR_GOAL_VELOCITY  = 104
ADDR_PRESENT_VELOCITY = 128

# Control Values
MODE_VELOCITY       = 1   # Velocity Control Mode
TORQUE_ENABLE       = 1
TORQUE_DISABLE      = 0
MOVE_SPEED          = 100 # Target speed (Safe range: 0~265)

# Initialize PortHandler & PacketHandler
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# 1. Open Port and Set Baudrate
if not portHandler.openPort() or not portHandler.setBaudRate(BAUDRATE):
    print("❌ Failed to open port or set baudrate! Check cables and power.")
    quit()

# 2. Scan Motor IDs (Checking ID 1 to 4)
print("🔍 Scanning for Dynamixels (ID 1~4)...")
found_ids = []
for dxl_id in range(1, 5):
    model_number, result, error = packetHandler.ping(portHandler, dxl_id)
    if result == COMM_SUCCESS:
        print(f"✅ Dynamixel Found! ID: {dxl_id}")
        found_ids.append(dxl_id)

if not found_ids:
    print("❌ No Dynamixels detected. Check if battery switch is ON.")
    quit()

# 3. Setup Found Motors (Change to Velocity Mode & Enable Torque)
for dxl_id in found_ids:
    # Disable Torque first to change operating mode
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    # Set to Velocity Control Mode
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_OPERATING_MODE, MODE_VELOCITY)
    # Enable Torque
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)

# 4. Movement Execution
try:
    print(f"\n🚀 Starting movement for IDs {found_ids} (Forward for 3s)...")
    
    # Forward: Motors on opposite sides usually need opposite directions
    for dxl_id in found_ids:
        # For TurtleBot3: Right wheel (usually ID 2) needs negative value to go forward
        speed = MOVE_SPEED if dxl_id == 1 else -MOVE_SPEED
        packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_GOAL_VELOCITY, speed)
    time.sleep(3)

    print("🛑 Stopping...")
    for dxl_id in found_ids:
        packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_GOAL_VELOCITY, 0)
    time.sleep(1)

    print("⏪ Moving Backward for 3s...")
    # Backward
    for dxl_id in found_ids:
        speed = -MOVE_SPEED if dxl_id == 1 else MOVE_SPEED
        packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_GOAL_VELOCITY, speed)
    time.sleep(3)

except KeyboardInterrupt:
    print("\nStopped by User")

finally:
    # 5. Stop All Motors and Disable Torque
    for dxl_id in found_ids:
        packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_GOAL_VELOCITY, 0)
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    
    portHandler.closePort()
    print("🏁 Finished.")
