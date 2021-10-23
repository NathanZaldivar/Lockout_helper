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

Lockout helper will first ask for the users username, once entered lockout helper will first retrieve the information using the **Get-ADuser** command and will then format using the **Select-Object** command.
```
powershell -Command Get-ADUser -Identity <USERNAME_HERE> -Properties Lockedout, Manager, Mail, logonhours, AccountLockoutTime, Name, PasswordExpired, PasswordLastSet, Title, employeeType, Enabled | Select-Object Name, Lockedout, logonhours, Mail, AccountLockoutTime, Manager, PasswordExpired, PasswordLastSet, Title, employeeType, Enabled

```
Lockout helper will then print the information to the terminal and save the username to your clipboard for use during the troubleshooting process.

![Capture](https://user-images.githubusercontent.com/72000765/138569969-61ca7c7d-f724-4b7c-947e-d4fc0fd9a6f4.PNG)

When processing the information gathered from Get-ADuser Lockout helper will also check for three common issues, whether the user is locked out, whether the users logon hours are correctly set, and whether the users account is disabled.

## Unlocking users accounts
Lockout helper as the name implies will unlock users accounts using the 0 option, this is done with the **Unlock-ADAccount** powershell command.
```
powershell -Command Unlock-ADAccount -Identity <USERNAME HERE>

```
Once done Lockout helper will simply print done.

![image](https://user-images.githubusercontent.com/72000765/138570563-a1cd9905-4adf-42dd-9c13-780bcab2d0d4.png)

## Restarting search

As the function name implies this simply restarts lockout helper and you will be able to input a new username.

![image](https://user-images.githubusercontent.com/72000765/138570595-14407a82-84ba-41d3-949f-29752f257739.png)

## Printing manager tree

This function will print the current selected users manager tree up to 3 positons above the current user, this implements the same command powershell command **Get-ADuser** but will only retrieve information on the users manager.

![Capture](https://user-images.githubusercontent.com/72000765/138570716-7540573a-e7e9-4dba-97cd-0cd881ecea22.PNG)

## Refreshing search

This function simply restarts the search on the current selected user, this is useful if you want to check is the users lockout timer has expired.

## Printing VPN permissions
When troubleshooting VPN issues one of the common reasons for connection issues is incorrect permissions, this function will search the users permissions using the **Get-ADuser** command and print to the terminal.

![Capture](https://user-images.githubusercontent.com/72000765/138570853-269c479e-4892-49b4-89a3-7497ae569b29.PNG)

## Journal builder for pre-ticket creation

This function is used after the call has ended and you must create your notes for incident ticket, this function doesn’t use any special powershell command and is imported from another script named J_builder.py

![image](https://user-images.githubusercontent.com/72000765/138570928-b1731e3b-2265-4abd-9d80-6835b26701ef.png)

Lockout helper will then copy the notes to your clipboard.
