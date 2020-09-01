from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import io
import os
import json
from googleapiclient.http import MediaIoBaseDownload
import threading

try:
    from data.send_email import send_email
except ModuleNotFoundError:
    from send_email import send_email

def download_files_GDrive ():
    path_dir = (os.path.dirname(os.path.abspath(__file__))+'/').replace('/','//')

    # authorization boilerplate code
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage(f'{path_dir}token.json')
    creds = store.get()
    # The following will give you a link if token.json does not exist, the link allows the user to give this app permission
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(f'{path_dir}client_id.json', SCOPES)
        creds = tools.run_flow(flow, store, obj)

    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    def download_file(file_id,file_name):
        # if you get the shareable link, the link contains this id, replace the file_id below
        if len(file_id) < 40:
            request = DRIVE.files().get_media(fileId=file_id)
        else:
            request = DRIVE.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # replace the filename and extension in the first field below
        fh = io.FileIO(file_name, mode='w')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

    files = {
        '1YBNskOyZJv-TRHFPH5kE5ty_SQ7XdsJ6':f'{path_dir}quissama',
        '1y6iKyRtH6SwARaZmmoKsR3wAjU_HV1fcdhLcFeTvslU':f'{path_dir}Tabela Informes Região Norte final',
        '1bcCG-RCU-ayBIChwgyblpwQKI9F-hUEy':f'{path_dir}Social Distancing Index by Cities'
        #,'1bJjpKv2x-q5W8s48QFZiUqHEHsT10uXV':f'{path_dir}Social Distancing Index by States'
        }

    extensions = {
        '1YBNskOyZJv-TRHFPH5kE5ty_SQ7XdsJ6':'.xlsx',
        '1y6iKyRtH6SwARaZmmoKsR3wAjU_HV1fcdhLcFeTvslU':'.xlsx',
        '1bcCG-RCU-ayBIChwgyblpwQKI9F-hUEy':'.csv'
    }


    for i in files:
        try:
            download_file(i,f'{files[i]}_new{extensions[i]}')
            new  = os.path.getsize(f'{files[i]}_new{extensions[i]}')
            old = os.path.getsize(f'{files[i]}{extensions[i]}')
            if old == new:
                print(f'{files[i]}')
                os.remove(f'{files[i]}_new{extensions[i]}')
            else:
                with open(f'{path_dir}file_sizes.json','r',encoding='UTF-8') as json_file:
                    time_modified_check = json.loads(json_file.read())
                with open(f'{path_dir}file_sizes.json','w') as json_file:
                    time_modified = os.path.getsize(f'{files[i]}_new{extensions[i]}')
                    time_modified_check[f'{files[i]}{extensions[i]}'.replace(path_dir,'')] = time_modified
                    json.dump(time_modified_check,json_file)
                    
        except FileNotFoundError:
            os.rename(f'{files[i]}_new{extensions[i]}',f'{files[i]}{extensions[i]}')
                       
        except Exception as e:
            assunto = 'Alerta! - Erro ao Baixar Arquivo - GT - Covid19'
            print(assunto)
            mensagem = f'Ao tentar fazer download do arquivo {files[i]}{extensions[i]} o seguinte erro ocorreu: \n{e}'
            print(mensagem)
            send_email(assunto, mensagem)

download_files_GDrive()