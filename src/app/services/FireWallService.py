import subprocess
import os

class Utilities:
    
    @staticmethod
    def is_firewall_enabled():
        output = Utilities.cmd("netsh advfirewall show allprofiles state")
        return "OFF" not in output

    @staticmethod
    def set_firewall(state):
        if Utilities.check_firewall_rule() != state:
            if state:
                Utilities.enable_no_saving_mode()
            else:
                Utilities.disable_no_saving_mode()

    @staticmethod
    def add_firewall_rule():
        app = Utilities.get_app_info()
        command = f'netsh advfirewall firewall add rule name="{app["rule_name"]}" dir=out action=block remoteip={app["remote_ip"]} enable=yes'
        
        out = Utilities.cmd(command)
        print(out)
    @staticmethod
    def remove_firewall_rule():
        app = Utilities.get_app_info()
        command = f'netsh advfirewall firewall delete rule name="{app["rule_name"]}"'
        Utilities.cmd(command)

    @staticmethod
    def check_firewall_rule():
        app = Utilities.get_app_info()
        command = f'netsh advfirewall firewall show rule name="{app["rule_name"]}"'
        output = Utilities.cmd(command)
        return app["rule_name"] in output

    @staticmethod
    def cmd(line):
        result = subprocess.run(
            ['cmd.exe', '/C', line],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        error = result.stderr
        if error:
            print(f"Error: {error}")
        return output

    @staticmethod
    def get_app_info():
        # Here you can replace the static values with dynamic data or configuration
        return {
            "rule_name": "CustomRule",
            "remote_ip": "192.81.241.171"
        }
