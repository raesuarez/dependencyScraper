from getSourceCode import getPackage
from depDataMine import getDepData, getURL, getDeps, getDevDeps
from getDates import get_latest_commit
from datetime import datetime
from operator import itemgetter
import USERINFO


allDeps = [] #global list of package names to check if repository has been written to

def loadDepsList(repo):
    """
    param: str repo, must be valid javascript/npm Github repository link
    returns list, a list of the dependencies of the repo's direct dependencies (1st level of indirect dependencies)
    writesdirect dependency table sorted by latest commit to testSite.html
    gets dependency data of the direct dependencies
    """
    getPackage(repo) #loads package.json for the repository file
    table=[]
    indirectDeps=[]
    directDeps = getDeps('0') #call using 0 bc there is no version number in the initial pkgContent.json
    directDeps += getDevDeps('0')
    with open('testSite.html', 'w') as f:
        #initializing html document
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang= "en">\n')
        f.write(f'<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n<meta name="description" content="">\n<meta name="author" content="">\n<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" \ncrossorigin="anonymous">\nThis is {repo.split("/")[-1]}\'s dependency list.\n</head>\n')
        f.write('<body>\n<div class="container-fluid">\n<div class="row">\n<div class="p-1 col-sm-12 sortable-table">\n<table class="table table-hover table-bordered" id="my-table1">')
        f.write(f"<thead>\n  <tr>\n    <th>Direct Dependecy</th>\n    <th>Repo Link</th>\n    <th>Date Since Last Commit</th>\n  </tr>\n</thead>\n<tbody>\n")
        for dep in directDeps:
            #getting data for the table
            getDepData(dep[0])
            url = getURL()
            date = int(get_latest_commit(getURL()))
            table.append([dep[0], url, int(date)])
            if getDeps(dep[1]) != None and getDevDeps(dep[1]) != None:
                #gets indirect dependency data to return from current dep
                indirectDeps+=getDeps(dep[1]) 
                indirectDeps+=getDevDeps(dep[1])

        table = sorted(table, key = itemgetter(2)) #sorts list by most recenelty updated/committed to

        for item in table:
            #writes X days/months/years ago to item(3)
            daysAgo = item[2]
            monthsAgo = item[2] // 30
            yearsAgo = monthsAgo // 12
    
            if monthsAgo > 12:
                item[2]= f"{yearsAgo} years ago"
            elif daysAgo > 30:
                item[2]=  f"{monthsAgo} months ago"
            elif daysAgo < 30:
                item[2]= f"{daysAgo} days ago"
    
            item[1] = item[1].replace('git+', '').replace(".git", '').replace('git:', 'https:').replace('ssh:', 'https:')
        
            #writes data to table
            f.write(f"  <tr>\n    <td>{item[0]}</td>\n    <td><a href={item[1]}>{item[1]}</a></td>\n    <td>{item[2]}</td>\n  </tr>\n")
        #closes direct dependency table
        f.write('</tbody>\n</table>\n</div>\n')
    return indirectDeps

def depsTest(deps):
    """
    param: list of tuples deps, list of packageName,version tuples
    returns None
    recursive, calls itself until no more indirect dependencies can be found
    """
    global allDeps
    indirectDeps = []
    with open("test.txt", "a+", encoding="utf8") as f:
        if deps != None:
            for dep in deps:
                if dep[0] not in allDeps: #if dependency has not already been added to global list of dependencies, avoids double checking deps/getting stuck in a loop
                    allDeps.append(dep[0])
                    getDepData(dep[0]) 
                    url = getURL()
                    date = get_latest_commit(url)
                    if getDeps(dep[1]) != None and getDevDeps(dep[1]) != None and url!= None and date!=None:
                        f.write(f"{dep[0]}, {url}, {date}\n")
                        indirectDeps += getDeps(dep[1])
                        indirectDeps += getDevDeps(dep[1])
                else:
                    print(f' deps test {dep[0]} already in list')
        if indirectDeps and indirectDeps != None:
            depsTest(indirectDeps)
        else:
            print("done")
            f.close()

def devsTest(devsList):
    """
    param: list of tuples deps, list of packageName,version tuples
    returns None
    recursive, calls itself until no more indirect dev dependencies can be found
    """
    global allDeps
    indirectDeps = []
    devs = devsList
    with open("test.txt", "a+", encoding="utf8") as f:
        if devs != None:
            for dev in devs:
                if dev[0] not in allDeps:
                    allDeps.append(dev[0])
                    getDepData(dev[0])
                    url = getURL()
                    date = get_latest_commit(url)
                    if getDeps(dev[1]) != None and getDevDeps(dev[1]) != None and url!= None and date!=None:
                        f.write(f"{dev[0]}, {url}, {date}\n")                  
                        indirectDeps += getDeps(dev[1])
                        indirectDeps += getDevDeps(dev[1])
                else:
                    print(f"devs test {dev[0]} already in list")
        if indirectDeps and indirectDeps != None:
            devsTest(indirectDeps)
        else:
            print("done")
            f.close()

def writeToSite():
    """
    returns list of lists table, a list of the dependency data written into the table
    """
    table = []
    with open('test.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'dependencies' not in line.lower() and line!= '\n':
                item = [line.split(',')[0], line.split(',')[1], line.split(',')[2].replace('\n', '')]
                item[2]=int(item[2])
                table.append(item)
    f.close()

    table = sorted(table, key = itemgetter(2))

    for item in table:
        daysAgo = item[2]
        monthsAgo = item[2] // 30
        yearsAgo = monthsAgo // 12

        if monthsAgo > 12:
            item[2]= f"{yearsAgo} years ago"
        elif daysAgo > 30:
            item[2]=  f"{monthsAgo} months ago"
        elif daysAgo < 30:
            item[2]= f"{daysAgo} days ago"

        item[1] = item[1].replace('git+', '').replace(".git", '').replace('git:', 'https:').replace('ssh:', 'https:')

    with open('testSite.html', 'a') as f:
        f.write('\n<div class="container-fluid">\n<div class="row">\n<div class="p-1 col-sm-12 sortable-table">\n<table class="table table-hover table-bordered" id="my-table1">')
        f.write(f"<thead>\n  <tr>\n    <th> Indirect Dependecy</th>\n    <th>Repo Link</th>\n    <th>Date Since Last Commit</th>\n  </tr>\n</thead>\n<tbody>\n")
        for item in table:
            f.write(f"  <tr>\n    <td>{item[0]}</td>\n    <td><a href={item[1]}>{item[1]}</a></td>\n    <td>{item[2]}</td>\n  </tr>\n")
        f.write('</tbody>\n</table>\n</div>\n</body>\n</html>')
    f.close()
    print('testSite.html is ready now')
    return table

repo = USERINFO.repo

l1 = loadDepsList(repo)
depsTest(l1)

def cleanDevsList(repo):
    """
    param: str repo
    returns indirect deps
    removes 1st level of indirect deps from the global allDeps list so devsTest can run on the list
    """
    indirectDeps=[]
    getPackage(repo) #loads package.json for the repository file
    directDeps = getDeps('0') #call using 0 bc there is no version number in the initial pkgContent.json
    directDeps += getDevDeps('0')
    for dep in directDeps:
        getDepData(dep[0])
        if getDeps(dep[1]) != None and getDevDeps(dep[1]) != None:
            #gets indirect dependency data to return from current dep
            indirectDeps+=getDeps(dep[1]) 
            indirectDeps+=getDevDeps(dep[1])
    for dep in indirectDeps:
         if dep[0] in allDeps:
            allDeps.remove(dep)
    return indirectDeps

cleanDevsList(repo)
devsTest(l1)
writeToSite()