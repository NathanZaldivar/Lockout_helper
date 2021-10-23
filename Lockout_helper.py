# Nathans Active Directory Account unlock tool!
from subprocess import run
import pyperclip
from colorama import Fore
import datetime
import time
import J_builder




options = f'''
{Fore.CYAN}OPTIONS:
[0] : Unlock
[1] : Restart
[2] : Print manager tree
[3] : Refresh
[4] : Print VPN permissions
[5] : Journal builder
{Fore.WHITE}'''

class Common:
    def __init__(self, properties):
        self.properties = properties

    def check_password(self):
        if self.properties['PasswordExpired'] == 'False':
            return f'{Fore.GREEN}[*] {Fore.WHITE}Accounts password is not expired'
        elif self.properties['PasswordExpired'] == 'True':
            return f'{Fore.RED}[CRITICAL] {Fore.WHITE}Password is expired'
        else:
            return f'{Fore.YELLOW}[WARNING] {Fore.WHITE}Password expiration status unsure'


    def check_lockout(self):
        if self.properties['Lockedout'] == 'False':
            return f'{Fore.GREEN}[*] {Fore.WHITE}Account is not locked'
        elif self.properties['Lockedout'] == 'True':
            try:
                lockout_time = datetime.datetime.strptime(self.properties['AccountLockoutTime'], '%m/%d/%Y %I:%M:%S %p')
                current_time = datetime.datetime.now()
                time_left = current_time - lockout_time
            except:
                time_left = 'Unkown Time'
            return f'{Fore.RED}[CRITICAL] {Fore.WHITE}Account is locked, {time_left} has passed since lockout'
        else:
            return f'{Fore.YELLOW}[WARNING] {Fore.WHITE}Lockout status unsure'

    def check_logon(self):
        if self.properties['logonhours'] == '{255, 255, 255, 255...}':
            return f'{Fore.GREEN}[*] {Fore.WHITE}Logon hours are set'
        elif self.properties['logonhours'] == '{0, 0, 0, 0...}':
            return f'{Fore.RED}[CRITICAL] {Fore.WHITE}Logon hours are NOT set'
        else:
            return f'{Fore.YELLOW}[WARNING] {Fore.WHITE}Logon hours status unsure'

    def choices(self, PID):
        print(options)
        while True:
            choice = input('#:')
            if choice == '0':
                run(['powershell', '-Command', 'Unlock-ADAccount', '-Identity', "'{}'".format(PID)])
                return f'{Fore.GREEN}[*] {Fore.WHITE}Done'
            elif choice == '1':
                return f'{Fore.GREEN}[*] {Fore.WHITE}Restarting'
            elif choice == '2':
                print(self.manager_tree())
            elif choice == '3':
                return PID
            elif choice == '4':
                print(self.check_vpn(PID))
            elif choice == '5':
                self.jbuilder()
                print(options) # Text to long, options get coverd
            else:
                print(f'{Fore.RED}[CRITICAL] {Fore.WHITE}Invalid option')


    def manager_tree(self):
        backup = 'Dummy variable is dumb'
        manager  = self.properties['Manager']
        lst = []
        for i in range(3):
            x = manager.index(' (')
            y = manager.index('),')
            z = manager.index('CN=')
            username = manager[x+2:y]
            manager_name = manager[z+3:y+1]
            search = run(['powershell', '-Command', 'Get-ADUser', '-Identity', "'{}'".format(username), '-Properties', 'Manager', '|', 'Select-Object', 'Manager'], capture_output=True)
            manager = search.stdout.decode().strip().split('\n')[2]
            if backup == manager_name:
                lst.append('END OF HIERARCHY')
                break
            else:
                lst.append(manager_name)
            backup = manager_name
        return self.properties['Name'] + "".join([f' {Fore.YELLOW}---> {Fore.WHITE}{i}' for i in lst])

    def check_vpn(self, PID):
        print(f'{Fore.GREEN}[*] {Fore.WHITE}Getting VPN permissions...')
        search = run(['powershell', '-Command', 'Get-ADUser', '-Identity', "'{}'".format(PID), '-Properties', 'MemberOf', '|', 'select', '-ExpandProperty', 'MemberOf'], capture_output=True)
        results = search.stdout.decode().strip()
        results_lst = results.split('\n')
        end_lst = []
        for i in results_lst:
            tmp_lst = i.split(',')
            memberof = tmp_lst[0]
            if 'VPN' in memberof.upper():
                print(memberof)
                end_lst.append(memberof)
        if len(end_lst) == 0:
            print(f'{Fore.RED}[CRITICAL] {Fore.WHITE}No VPN rights found')
            choice = input('Print all permissions for investigation? [y or n]: ').lower()
            if choice == 'y':
                print(results)
        return f'{Fore.GREEN}[*] {Fore.WHITE}Done'

    def jbuilder(self):
        J_builder.jmod()
        print(f'{Fore.GREEN}[*] {Fore.WHITE}Notes saved to clipboard')

def dict_builder(stdout):
    properties = {}
    backup = 'Dummy variable is dumb'
    for i in stdout:
        if ' : ' not in i:
            properties[backup] += i.strip()
            continue
        else:
            chunks = i.split(' : ')
            properties[chunks[0].strip()] = chunks[1].strip()
        backup = chunks[0].strip()
    return properties


def main():
    print('Welcome to Nathans Lockout helper, please ensure that you are running this as a Admin.')
    backup = False
    while True:
        if backup != False:
            PID = backup
            backup = False
        else:
            PID = input('$:')
        search = run(['powershell', '-Command', 'Get-ADUser', '-Identity', "'{}'".format(PID), '-Properties', 'Lockedout,', 'Manager,', 'Mail,', 'logonhours,', 'AccountLockoutTime,', 'Name,', 'PasswordExpired,', 'PasswordLastSet,', 'Title,', 'employeeType,', 'Enabled', '|', 'Select-Object', 'Name,', 'Lockedout,', 'logonhours,', 'Mail,', 'AccountLockoutTime,', 'Manager,', 'PasswordExpired,', 'PasswordLastSet,', 'Title,', 'employeeType,', 'Enabled'], capture_output=True)
        results = search.stdout.decode()
        results_template = results.lower()
        PID_template = PID.lower()
        if PID_template not in results_template and 'adm' not in results_template:
            error = search.stderr.decode()
            if 'A connection to the directory on which to process the request was unavailable.' in error:
                print(f'{Fore.RED}[CRITICAL] {Fore.WHITE}Connection to the active directory server is unavailable, this is a common issue. Please use backup tools in the meantime, Lockout helper will temporarily be unavailable for 15 minute.')
                for i in range(1, 901):
                    time.sleep(1)
                    print(f'Restarting in {900 - i}', end=' \r')
                print(f'{Fore.GREEN}[*] {Fore.WHITE}Restarting... If this problem continues please contact me')
            else:
                print(f'{Fore.RED}[CRITICAL] {Fore.WHITE}Username not found in domain, could the user have a diffrent username?')
            continue    
        pyperclip.copy(PID)
        print(f'{Fore.GREEN}[*] {Fore.WHITE}PID saved to clipboard')
        print(results)
        properties = dict_builder(results.strip().split('\n'))
        checker = Common(properties)
        print(checker.check_logon())
        print(checker.check_lockout())
        print(checker.check_password())
        choice = checker.choices(PID)
        if choice == PID:
            backup = choice
        else:
            print(choice)



if __name__ == '__main__':
    main()
