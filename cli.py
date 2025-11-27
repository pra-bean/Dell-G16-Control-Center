from monitor import get_cpu_stats, get_gpu_stats, get_fan_rpm
from performance import get_platform_profile, get_governors
from profile_manager import (
    apply_quiet,
    apply_balanced,
    apply_performance,
    apply_g_mode
)


def main():
    while True:
        print("\n=== G16 CONTROL CENTER ===")
        print("1. Show CPU stats")
        print("2. Show GPU stats")
        print("3. Show Fan RPM")
        print("4. Show Platform Profile")
        print("5. Show CPU Governors")
        print("--------------------------")
        print("6. Apply QUIET mode")
        print("7. Apply BALANCED mode")
        print("8. Apply PERFORMANCE mode")
        print("9. Apply G-MODE")
        print("--------------------------")
        print("0. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            print("CPU:", get_cpu_stats())
        elif choice == "2":
            print("GPU:", get_gpu_stats())
        elif choice == "3":
            print("Fans:", get_fan_rpm())
        elif choice == "4":
            print("Platform Profile:", get_platform_profile())
        elif choice == "5":
            print("Governors:", get_governors())
        elif choice == "6":
            print(apply_quiet())
        elif choice == "7":
            print(apply_balanced())
        elif choice == "8":
            print(apply_performance())
        elif choice == "9":
            print(apply_g_mode())
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
