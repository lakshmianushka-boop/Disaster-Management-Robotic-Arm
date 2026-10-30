
from arm_simulator import ArmSimulator


def main():
    arm = ArmSimulator()

    try:
        arm.connect()

        print("\n--- TEST 1: Clear debris ---")
        debris_ok = arm.send_command("PICK_RED")
        print("Debris action completed:", debris_ok)

        print("\n--- TEST 2: Rescue human ---")
        rescue_ok = arm.send_command("PICK_BLUE")
        print("Rescue action completed:", rescue_ok)

        print("\n--- RESULTS ---")
        print("Expected cycles: 2")
        print("Actual cycles:", arm.completed_cycles)

        if debris_ok and rescue_ok and arm.completed_cycles == 2:
            print("PASS: Simulated arm commands completed.")
        else:
            print("FAIL: Check the simulator output.")

    finally:
        arm.close()


if __name__ == "__main__":
    main()
