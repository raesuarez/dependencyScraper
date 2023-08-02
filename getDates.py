import requests
from datetime import datetime
import USERINFO


token = USERINFO.token

def get_latest_commit(repo):
    """
    param: str repo, valid javascript/npm Github repository link
    returns int, number of days since last commit
    """
    if repo!=None and repo !='':

        repoOwner = repo.split("/")[-2]

        repoName = repo.split("/")[-1]
        repoName = repoName.replace(".git", "")

        path = f"https://api.github.com/repos/{repoOwner}/{repoName}/commits"
        headers = {"Authorization": f"Bearer {token}"}
        url = requests.get(path, headers=headers)
        
        commits = url.json()
        if url.status_code == 200:
            if commits:
                try:
                    latest_commit = commits[0]
                    commit_date = latest_commit['commit']['author']['date']

                    commit_date = commit_date.split("T")[0]
                    commit_date = commit_date.split("-")

                    year = int(commit_date[0])
                    month = int(commit_date[1])
                    day = int(commit_date[2])

                    today = datetime.now().date()
                    target = datetime(year, month, day).date()
                    diff = today - target

                    return diff.days
                except KeyError:
                    print("getDates: key error")
                
            else:
                print("getDates: No commits found")
        else:
            print("getDates: response error")
    