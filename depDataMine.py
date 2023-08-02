import requests
import json
import semantic_version as semver


def parse():
    """
    opens pkgContent.json, parses the json content
    """
    with open("pkgContent.json", "r+", encoding="utf8") as f:
        try:
            parsed = json.load(f)
            f.seek(0)
            f.write(json.dumps(parsed, indent=4)) 
            f.close()
        except ValueError:
            print ("getRepoURL: parse JSON object issue")

def getURL():
    '''
    reads pkgContent.json and returns repository link
    '''
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
    """
    param: str pkgName, must be a valid npm package name
    writes the package's json file to repoInfo.txt
    parse() to parse json file datat
    """
    if "/" in pkgName:
        pkgName= pkgName.replace("/", "%2F")
    r = requests.get('https://replicate.npmjs.com/registry/'+pkgName)
    with open('pkgContent.json', "w", encoding="utf8") as f:
        f.write(r.text)
        f.close()
    parse()

def getDeps(v):
    """
    param: str v, package version number
    reads pkgContent.json
    finds version and returns a list of tuples
    tuples are pkgName,version
    if not a valid version, returns latest dependencies in a list of tuples, (pkgName, version)
    """
    deps = [] #list for dependency, version tuple
    go = False
    try:
        with open("pkgContent.json", "r") as f:
            text = f.read()
            info = json.loads(text)
            if 'versions' in info: #checks for versions dictionary
                if v in info['versions']: #if v is valid version number
                    if 'dependencies' in info['versions'][v]: #finds deps for version number
                            dep = info['versions'][v]['dependencies']
                            for d in dep:
                                v = dep[d]
                                deps.append((d,v)) #pkgName, version tuple 
                            return deps
                    else:
                        #print('no deps')
                        return
                else:
                    go = True
                    for version in info['versions']:
                        if semver.match(v, version) and go: #finds a valid version match
                            if 'dependencies' in info['versions'][version]:
                                dep = info['versions'][version]['dependencies']
                                go = False #stops at first version match
                                for d in dep:
                                    version = dep[d]
                                    deps.append((d,version))
                                return deps
                            else:
                                break
            elif 'dependencies' in info: #finds earliest mention of deps
                dep = info['dependencies']  
                for d in dep:
                    v = dep[d]
                    deps.append((d,v))
                print("getDeps: using elif") #should only be used during first dep call
                return deps 
    except ValueError:
        print("dependencyReader: value error")
        return "dependencyReader: value error"

def getDevDeps(v):
    """
    param: str v, package version number
    same exact function as above except looking for devDependencies
    returns list of tuples, (pkgName,version)
    """
    devs = []
    try:
        with open("pkgContent.json", "r") as f:
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
                        return ''
                else:
                    go = True
                    for version in info["versions"]:
                        if semver.match(v, version) and go:
                            if 'devDependencies' in info['versions'][version]:
                                dev = info['versions'][version]['devDependencies']
                                go = False
                                for d in dev:
                                    v = dev[d]
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
    



