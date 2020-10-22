def isFrontline(user):
    jobTitle = str(user.get('title')).lower()
    department = str(user.get('department')).lower()
    division = str(user.get('organization')).lower()
    organisation = str(user.get('organization')).lower()
    office = str(user.get('primary_address')).lower()

    if \
        (jobTitle == 'general manager') or \
        (department == 'operations') or \
        (division == 'coolr workplace') or \
        (organisation == 'coolr') or \
            (office == 'soho'):
        return False
    else:
        return True
