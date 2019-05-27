from github import Github
import sys


def lst_repos(g):
    repo_lst = []
    for repo in g.get_user().get_repos():
        repo_lst.append(repo)
    return repo_lst

def get_docs(repo_lst, g):
    for repo in repo_lst:
        print(repo.name)
        contents = repo.get_contents("")
        for content_file in contents:
            if content_file.name == 'docs':
                print(f'  {content_file.name}')
            if content_file.type == 'dir' and content_file.name == 'docs':
                folder = repo.get_contents(content_file.path)
                while len(folder) > 1:
                    file_content = folder.pop(0)
                    if file_content.type == "dir":
                        folder.extend(repo.get_contents(file_content.path))
                    else:
                        print(f'    {file_content.name}')

    
def usage():
    print("Work in progress")

def main():
    g = Github("e18c17fcfed708d69ee630af894d134f6df666d1")
    repo_lst = lst_repos(g)
    get_docs(repo_lst, g)


if __name__ == '__main__':
    main()
