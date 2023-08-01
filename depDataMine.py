import requests
import json
import semantic_version as semver


def parse():
    with open("pkgContent.json", "r+", encoding="utf8") as f:
        try:
            parsed = json.load(f)
            f.seek(0)
            f.write(json.dumps(parsed, indent=4)) 
            f.close()
        except ValueError:
            print ("getRepoURL: parse JSON object issue")

def getURL():
    #reads repoInfo and finds the URl of a package
    with open("pkgContent.json", "r", encoding="utf8") as f:
        try:
            text = f.read()
            info = json.loads(text)
            if 'repository' in info:
                link = info['repository']['url']
                #print(link)
                return link
        except json.decoder.JSONDecodeError:
            print ("getRepoURL: getURL JSON object issue")  
    
def getDepData(pkgName):
    #takes package name as input
    #writes the package's json file to repoInfo.txt
    if "/" in pkgName:
        pkgName= pkgName.replace("/", "%2F")
    r = requests.get('https://replicate.npmjs.com/registry/'+pkgName)
    with open('pkgContent.json', "w", encoding="utf8") as f:
        f.write(r.text)
        f.close()
    parse()

def getDeps(v):
    #returns dictionary of dependencies
    deps = []
    go = False
    try:
        with open("pkgContent.json", "r") as f:
            #v = v.replace("~", '').replace('^', '')
            text = f.read()
            info = json.loads(text)
            if 'versions' in info:
                if v in info['versions']:
                    if 'dependencies' in info['versions'][v]:
                            dep = info['versions'][v]['dependencies']
                            for d in dep:
                                v = dep[d]#.replace("~", '').replace('^', '')
                                deps.append((d,v))
                            return deps
                    else:
                        #print('no deps')
                        return
                else:
                    go = True
                    for version in info['versions']:
                        if semver.match(v, version) and go:
                            #print('found version')
                            if 'dependencies' in info['versions'][version]:
                                dep = info['versions'][version]['dependencies']
                                #print('found deps')
                                go = False
                                for d in dep:
                                    version = dep[d]
                                    deps.append((d,version))
                                return deps
                            else:
                                break
            elif 'dependencies' in info:
                dep = info['dependencies']  
                for d in dep:
                    v = dep[d]
                    deps.append((d,v))
                print("getDeps: using elif (NOT GOOD)")
                return deps 
    except ValueError:
        print("dependencyReader: value error")
        return "dependencyReader: value error"

#getDeps("13.9.0")

def getDevDeps(v):
    devs = []
    try:
        with open("pkgContent.json", "r") as f:
            #v = v.replace("~", '').replace('^', '')
            text = f.read()
            info = json.loads(text)
            if 'versions' in info:
                if v in info['versions']:
                    if 'devDependencies' in info['versions'][v]:
                            dev = info['versions'][v]['devDependencies']
                            for d in dev:
                                v = dev[d]
                                devs.append((d,v))
                            return devs
                    else:
                        #print('no dev deps')
                        return ''
                else:
                    go = True
                    for version in info["versions"]:
                        if semver.match(v, version) and go:
                            #print("found version")
                            if 'devDependencies' in info['versions'][version]:
                                dev = info['versions'][version]['devDependencies']
                                #print("found dev deps")
                                go = False
                                for d in dev:
                                    v = dev[d]#.replace("~", '').replace('^', '')
                                    devs.append((d,v))
                                return devs
            elif 'devDependencies' in info:
                dev = info['devDependencies']  
                for d in dev:
                    v = dev[d]
                    devs.append((d,v))
                print("getDevDeps: using elif (NOT GOOD)")
                return devs
    except ValueError:
        print("dependencyReader: value error")
    



