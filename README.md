# Nathans Lockout helper tool developed in Python3!
**NOTE THIS IS NOT MENT FOR PRODUCTION THIS IS SIMPLY A DEMENSTARTION OF THIS TOOLS FUNCTIONS IN THE WORKPLACE, MANY PARTS OF THIS PROGRAM HAVE BEEN ALTERD TO KEEP THE SECRECY OF INNER HELPDESK HIDDEN FOR SECURITY REASONS.**

Available functions:
- Retrieving and printing user information
- Unlocking accounts
- Restarting search
- Printing manager tree
- Refreshing search
- Printing VPN permissions
- Journal builder for pre ticket creation

## Retrieving and printing user information
Lockout helper utilizes windows active directory module to retrieve user information and will then print that information to the terminal in a table format.

![image](https://user-images.githubusercontent.com/72000765/138569663-a96bcb5d-302d-4ab5-839d-1a0782fcf46e.png)

Lockout helper will first ask for the users username, once enterd lockout helper will first retrieve the information using the **Get-ADuser** command and will then format using the **Select-Object** command.
```
powershell -Command Get-ADUser -Identity <USERNAME_HERE> -Properties Lockedout, Manager, Mail, logonhours, AccountLockoutTime, Name, PasswordExpired, PasswordLastSet, Title, employeeType, Enabled | Select-Object Name, Lockedout, logonhours, Mail, AccountLockoutTime, Manager, PasswordExpired, PasswordLastSet, Title, employeeType, Enabled

```
Lockout helper will then print the information to the terminal and save the username to your clipboard for use during the troubleshooting process.

![Capture](https://user-images.githubusercontent.com/72000765/138569969-61ca7c7d-f724-4b7c-947e-d4fc0fd9a6f4.PNG)

When processing the information gathered from Get-ADuser Lockout helper will also check for three common issues, whether the user is locked out, whether the users logon hours are correctly set, and whether the users account is disabled.

