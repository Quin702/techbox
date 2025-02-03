import os
import subprocess
import winreg

class TechBox:
    def __init__(self):
        self.startup_locations = {
            'Registry': r'Software\Microsoft\Windows\CurrentVersion\Run',
            'Startup Folder': os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        }

    def list_startup_items(self):
        print("Startup Items in Registry:")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.startup_locations['Registry']) as reg_key:
            i = 0
            try:
                while True:
                    name, value, _ = winreg.EnumValue(reg_key, i)
                    print(f"{name}: {value}")
                    i += 1
            except OSError:
                pass

        print("\nStartup Items in Startup Folder:")
        for item in os.listdir(self.startup_locations['Startup Folder']):
            print(item)

    def add_startup_item(self, name, command):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.startup_locations['Registry'], 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, command)
            print(f"Added {name} to startup items.")

    def remove_startup_item(self, name):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.startup_locations['Registry'], 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.DeleteValue(reg_key, name)
                print(f"Removed {name} from startup items.")
        except FileNotFoundError:
            try:
                os.remove(os.path.join(self.startup_locations['Startup Folder'], name))
                print(f"Removed {name} from startup folder.")
            except FileNotFoundError:
                print(f"{name} not found in startup items.")

    def run(self):
        print("TechBox: Manage Startup Items\n")
        while True:
            print("1. List Startup Items")
            print("2. Add Startup Item")
            print("3. Remove Startup Item")
            print("4. Exit")
            
            choice = input("Enter your choice: ")
            if choice == '1':
                self.list_startup_items()
            elif choice == '2':
                name = input("Enter the name of the startup item: ")
                command = input("Enter the command to execute at startup: ")
                self.add_startup_item(name, command)
            elif choice == '3':
                name = input("Enter the name of the startup item to remove: ")
                self.remove_startup_item(name)
            elif choice == '4':
                print("Exiting TechBox.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    techbox = TechBox()
    techbox.run()