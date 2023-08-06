import os

def saveAsFile(response, filePath: str, fileName: str, overwrite: bool):
    """
    Saves the file downloaded in the response object, in the outPath, with filename
    If overwrite, will overwrite files with the same name
    """
    # Create outPath directory if not exists
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    
    # Save file in outPath if it doesn't exist yet
    fullPath = filePath + '/' + fileName
    if overwrite or (not os.path.exists(fullPath)):
        try:
            file = open(fullPath, 'wb+')
            file.write(response.content)
            file.close()
            
        except Exception:
            raise
    else:
        raise IOError('Skipping "{:s}": File already exists.'.format(fullPath))


def printErrorMessage(response, parameters: dict, showUrl: bool=False, showValue: bool=False):
    '''
    Method to print an error message from an ONC web service call to the console.
    '''
    if (response.status_code == 400):
        if showUrl: print('Error Executing: {:s}'.format(response.url))
        payload = response.json()
        if len(payload) >= 1:
            print("")
            for e in payload['errors']:
                code = e['errorCode']
                msg  = e['errorMessage']
                parm = e['parameter']

                matching = [p for p in parm.split(',') if p in parameters.keys()]
                if len(matching) >= 1:
                    for p in matching: print("  Error {:d}: {:s}. Parameter '{:s}' with value '{:s}'".format(code, msg, p, parameters[p]))
                else:
                    print("  '{}' for {}".format(msg, parm))

                if showValue:
                    for p in parm.split(','):
                        parmValue = parameters[p]
                        print("  {} for {} - value: '{}'".format(msg, p, parmValue))
            print("")

    else:
        msg = '\nError {:d} - {:s}\n'.format(response.status_code, response.reason)
        print(msg)
