import requests 
import USERINFO

token = USERINFO.token

def getPackage(repo):
    owner, repo = extract_owner_repo(repo)
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    with open("pkgContent.json", "w", encoding='utf8') as f:
        if response.status_code == 200:
            contents = response.json()
            for item in contents:
                if item['name'] == 'package.json':
                    download_url = item['download_url']
                    package_json_content = requests.get(download_url, headers=headers).text
                    f.write(package_json_content)
                    f.close()
                    break
        else:
            print("getSourceCode: Error retrieving repository contents.")

def extract_owner_repo(repo):
    parts = repo.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1].replace(".git", "")
    return owner, repo


getPackage('https://github.com/express-validator/express-validator')