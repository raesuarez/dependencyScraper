import json

def parse():
    #formats repoInfo.txt
    with open("pkgContent.json", "r+", encoding="utf8") as f:
        parsed = json.load(f)
        f.seek(0)
        f.write(json.dumps(parsed, indent=4)) 
        f.close()

