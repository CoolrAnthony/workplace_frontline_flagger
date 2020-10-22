from dotenv import load_dotenv
import requests
import os
import json
import rules

if os.getenv('prodMode') == 'True':
    prodMode = True
    print('Running in PRODUCTION mode')
else:
    prodMode = False
    print('Running in TEST mode')

graphURL = 'https://graph.facebook.com/'
scimURL = 'https://www.facebook.com/scim/v1/'
headers = {
    'Authorization': 'Bearer ' + os.getenv('accessToken')
}


def percentage(part, whole):
    return round(100 * float(part)/float(whole), 1)


def getAllWorkplaceUsers():
    # Loads all users from Workplace
    allUsers = []

    url = graphURL + 'community/members?fields=name,title,department,primary_address,frontline,organization,division&limit=5000'
    while True:
        result = json.loads(requests.get(
            url, headers=headers).text)
        allUsers.extend(result['data'])
        paging = result.get('paging')
        if paging.get('next'):
            url = paging.get('next')
        else:
            break
    return allUsers


WPUsers = getAllWorkplaceUsers()

for WPUser in WPUsers:
    # Should the user be flaged as frontline?
    if rules.isFrontline(WPUser):
        # This is a frontline user. Are they already in the fronline peopleset?
        if WPUser['frontline']['is_frontline']:
            # Already in peopleset, no action needed
            continue
        else:
            if prodMode == False:
                print('Add', WPUser['name'], 'to the Frontline People set')
            else:
                # Add the user to the FL peopleset
                url = graphURL + WPUser.get('id')
                payload = {"frontline": {"is_frontline": True}}

                result = json.loads(requests.post(
                    url, headers=headers, json=payload).text)
                if result.get('success'):
                    print('Added', WPUser['name'],
                          'to the Frontline People set')
                else:
                    print('!!! Error adding',
                          WPUser['name'], 'to the Frontline People set. Failure message:', result['error']['error_user_msg'])
    else:
        if WPUser['frontline']['is_frontline']:
            if prodMode == False:
                print('Remove', WPUser['name'],
                      'from the Frontline People set')
            else:
                # We need to remove this user from the FL peopleset
                url = graphURL + WPUser.get('id')
                payload = {"frontline": {"is_frontline": False}}

                result = json.loads(requests.post(
                    url, headers=headers, json=payload).text)
                if result.get('success'):
                    print('Removed', WPUser['name'],
                          'from the Frontline People set')
                else:
                    print('!!! Error removing',
                          WPUser['name'], 'from the Frontline People set. Failure message:', result['error']['message'])

# Get all the users again so that we can create a report
newWPUsers = getAllWorkplaceUsers()
frontlineWorkers = 0
knowledgeWorkers = 0

for newWPUser in newWPUsers:
    if newWPUser['frontline']['is_frontline']:
        frontlineWorkers += 1
    else:
        knowledgeWorkers += 1
totalWorkers = frontlineWorkers + knowledgeWorkers

print("Frontline Workers:", str(frontlineWorkers),
      "(", percentage(frontlineWorkers, totalWorkers), "% )")
print("Knowledge Workers:", str(knowledgeWorkers),
      "(", percentage(knowledgeWorkers, totalWorkers), "% )")
print("Total Workers:", str(totalWorkers))
