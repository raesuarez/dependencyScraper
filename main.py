from getSourceCode import getPackage
from depDataMine import getDepData, getURL, getDeps, getDevDeps
from getDates import get_latest_commit
from datetime import datetime
from operator import itemgetter
import USERINFO


allDeps = []

def loadDepsList(repo):
    getPackage(repo)
    table=[]
    indirectDeps=[]
    directDeps = getDeps('0')
    directDeps += getDevDeps('0')
    with open('testSite.html', 'w') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang= "en">\n')
        f.write(f'<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n<meta name="description" content="">\n<meta name="author" content="">\n<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" \ncrossorigin="anonymous">\nThis is {repo.split("/")[-1]}\'s dependency list.\n</head>\n')
        f.write('<body>\n<div class="container-fluid">\n<div class="row">\n<div class="p-1 col-sm-12 sortable-table">\n<table class="table table-hover table-bordered" id="my-table1">')
        f.write(f"<thead>\n  <tr>\n    <th>Direct Dependecy</th>\n    <th>Repo Link</th>\n    <th>Date Since Last Commit</th>\n  </tr>\n</thead>\n<tbody>\n")
        for dep in directDeps:
            print(dep[0])
            getDepData(dep[0])
            table += (dep[0], getURL(), get_latest_commit(getURL()))
            if getDeps(dep[1]) != None and getDevDeps(dep[1]) != None:
                indirectDeps+=getDeps(dep[1])
                indirectDeps+=getDevDeps(dep[1])

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
        
            f.write(f"  <tr>\n    <td>{item[0]}</td>\n    <td><a href={item[1]}>{item[1]}</a></td>\n    <td>{item[2]}</td>\n  </tr>\n")
        
        f.write('</tbody>\n</table>\n</div>\n')
    return indirectDeps

def depsTest(deps):
    global allDeps
    indirectDeps = []
    with open("test.txt", "a+", encoding="utf8") as f:
        if deps != None:
            #f.write("\n Indirect Dependencies: \n")
            for dep in deps:
                if dep[0] not in allDeps:
                    print(dep[0])
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
    global allDeps
    indirectDeps = []
    devs = devsList
    with open("test.txt", "a+", encoding="utf8") as f:
        if devs != None:
            f.write("\n indirect devDependencies: \n")
            for dev in devs:
                if dev[0] not in allDeps:
                    allDeps.append(dev[0])
                    #print(dev)
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
            #depsTest(indirectDeps)
            devsTest(indirectDeps)
        else:
            print("done")
            f.close()

def writeToSite():
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
devsTest(l1)
writeToSite()

# def loadDevsList(repo):
#     getPackage(repo)
#     directDevs = getDevDeps('0')
#     f=open("test.txt", 'a')
#     f.write(f"\n {repo}'s Direct Dev Dependencies\n")
#     for dev in directDevs:
#         if dev[0] in allDeps:
#             allDeps.remove(dev)
#         getDepData(dev[0])
#         # url = getURL()
#         f.write(f"{dev[0]},{getURL()},{get_latest_commit(getURL())}\n")
#     return directDevs
