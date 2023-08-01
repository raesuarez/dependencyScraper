from pydriller import Repository

def getSourceCode(path_to_repo):
    repo = Repository(path_to_repo, filepath='package.json', order= 'reverse', only_no_merge=False)
    go = True

    with open("pkgJSContent.json", "w", encoding="utf8") as f:
        for commit in repo.traverse_commits(): 
            print(commit)
            if go == True:
                for mod in commit.modified_files:
                    print(mod)
                    if mod.filename == "package.json" and go == True:
                        #print(mod.source_code)
                        f.write(mod.source_code)
                        go = False
                        f.close()
            elif go == False:
                f.close()
            break


getSourceCode("https://github.com/DefinitelyTyped/DefinitelyTyped.git")