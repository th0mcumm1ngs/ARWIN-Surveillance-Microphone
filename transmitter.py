import json, requests, os

# open json system settings file
systemSettings = json.load(open('settings.json', 'r'))

while True:
    try:
        for file in os.listdir('file_data'):
            name, ext = os.path.splitext(file)
            if ext == ".json":
                dataFile = json.load(open(f'file_data/{file}', 'r'))

                audioFileBytes = open(f'recordings/{dataFile["fileName"]}', 'rb').read()

                audioFileString = str(audioFileBytes, 'latin1')

                dataTransmission = {
                    'startTime': dataFile['startTime'],
                    'endTime': dataFile['endTime'],
                    'audioFileString': audioFileString
                }

                requests.post(url = f'http://{systemSettings["ip_addresses"]["ARWIN_Main_Server"]}', json = dataTransmission)

                os.rename(f'file_data/{file}', f'bin/transmitted_recordings/{file}')
                os.rename(f'recordings/{dataFile["fileName"]}', f'bin/transmitted_recordings/{dataFile["fileName"]}')

            elif name == ".blank":
                pass
            else:
                os.rename(f'file_data/{file}', f'bin/misplaced_files/{file}')
    except:
        pass