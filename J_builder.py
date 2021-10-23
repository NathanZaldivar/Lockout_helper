import pyperclip

#builder for final output
def journal_builder(template, input_lst):
    notes = template.format(*input_lst)
    return notes

#builder for questions 
def input_builder(template):
    input_lst = []
    qna_lst = template.split('\n')
    for i in qna_lst:
        if '{}' not in i:
            continue
        choice = input(i.replace('{}', ''))
        input_lst.append(choice)
        
    return input_lst


def print_options(options):
    for x, i in enumerate(options):
        print('[*] OPTION {}: \n'.format(str(x)) + i.strip())
    choice = int(input('$: '))
    return choice

#Templates, must be added by hand
descriptions = {0 : 'REDACTED', 1 : 'REDACTED', 2: 'REDACTED', 3 : 'REDACTED'}


template = {0 : ['''
=============================
Password Reset\Account Unlock
=============================
''', '''System(s): {}
Who was Verified (Network ID): {}
Reset or Unlock: {}
 - Repeat Lockout (if lockout) {}
Additional Notes\Comments: {}'''], 1: ['''
========================================
Standard Issue Information
========================================
''', '''Summary of Issue: {} 
URL or Application Name: {}
Username/Login ID: {}
User Verification?: {}
Error Received: {}
When did the issue last work as expected? {}
Number of Users Impacted? {}
How are you connected to the network? {} 
Can this be duplicated by the Support Desk? {}
Troubleshooting / Escalation Actions Taken including any workarounds (Include Screenshots as Attachments): {}
========================================
User Information
========================================
Contact Phone Number: {}
Best Method of Contact: {}
Full Address of Location Impacted: {} 
Computer Name or Asset Tag Number: {}
IP Address: {}'''], 2: ['''
========================================
VPN Performance Troubleshooting
========================================''', '''
Summary of Issue: {}
Username/Login ID: {}
Error Received: {}
When did the issue last work as expected? {} 
Troubleshooting / Escalation Actions Taken including any workarounds (Include Screenshots as Attachments): {}
========================================
User Information
========================================
Contact Phone Number: {}
Best Method of Contact: {}
Computer Name or Asset Tag Number: {}
IP Address: {}
========================================
Computer Information
========================================
RAM: {}
Processor: {}
Free Space on the C: drive: {} 
IPv6 Enabled?: {}
========================================
VPN Tests
========================================
Off-VPN Upload Speed: {}
Off-VPN Download Speed: {}
Off-VPN CPU Usage %: {}
VPN Upload Speed: {}
VPN Download Speed: {}
VPN CPU Usage %: {}
'''], 3 : ['''
==============================
Walk Out Request
==============================
''','''
 - REDACTED: {}
 - REDACTED? {}
 - REDACTED? {}
 - REDACTED? {}
 - REDACTED? {}
 - REDACTED? {}
 - REDACTED? {}'''], 4 : ['''
========================================
Standard Application issues
========================================
''','''
Summary of Issue: {}
URL or Application Name: {} 
Username/Login ID: {}
User Verification?: {}
Error Received: {}
When did the issue last work as expected? {}
Number of Users Impacted? {}
How are you connected to the network? {}
Can this be duplicated by the Support Desk? {}
Troubleshooting / Escalation Actions Taken including any workarounds (Include Screenshots as Attachments): {}
========================================
User Information
========================================
Contact Phone Number: {}
Best Method of Contact: {}
Full Address of Location Impacted: {} 
Computer Name or Asset Tag Number: {}
IP Address: {}
''', [['''
========================================
Billing Outage Additional Information
========================================''','''
Error message received by IT Support Desk completing steps to access program: {}
Example Account Numbers for billing outages affecting customer accounts (at least 1, 2 is preferred): {}
Associate Usernames for logging into the program: {}
'''],['''
========================================
Application Outage Additional Information
========================================''','''
Error message received by IT Support Desk completing steps to access program: {}
Associate Usernames for logging into the program: {}
'''],[ '''
========================================
Network/Internet Outage
========================================''','''
How many people are in the office are affected? {}
How many people in total are in the office? {}
Any power outages/surges? Is power currently on? {}
Any recent maintenance/work/construction done locally? {}
'''], ['''
========================================
Spectrum Mobile Outage
========================================''','''
Subscriber Number(s) reporting the issue: {}
''']]]}
def jmod():
    choice = print_options([template[i][0] for i in template.keys()])
    if len(template[choice]) > 2:
        choice2 = print_options([i[0] for i in template[choice][2]])
        template_final = template[choice][0] + template[choice][1] + ''.join(template[choice][2][choice2])
        input_lst = input_builder(template_final)
        notes = journal_builder(template_final, input_lst)
    else:
        template_final = template[choice][0] + template[choice][1]
        input_lst = input_builder(template_final)
        notes = journal_builder(template_final, input_lst)
    pyperclip.copy(notes)



def main():
    # God put me on this earth to write code thats unreadable even to me...
    print('Welcome to Nathans Journal Builder! Please choose out of the templates below: \n')
    mode = print_options(['Journal Templates', 'Description/resoultion'])
    if mode == 0:
        choice = print_options([template[i][0] for i in template.keys()])
        if len(template[choice]) > 2:
            choice2 = print_options([i[0] for i in template[choice][2]])
            template_final = template[choice][0] + template[choice][1] + ''.join(template[choice][2][choice2])
            input_lst = input_builder(template_final)
            notes = journal_builder(template_final, input_lst)
        else:
            template_final = template[choice][0] + template[choice][1]
            input_lst = input_builder(template_final)
            notes = journal_builder(template_final, input_lst)
    else:
        choice = print_options([i for i in descriptions.values()])
        notes = descriptions[choice].strip()
    print(notes)
    pyperclip.copy(notes)
    print('[*] Text copied to clipboard')
    choice2 = input('Start again?[y or n]: ').lower()
    if choice2 == 'y':
        main()
    else:
        quit()

if __name__ == '__main__':
    main()
