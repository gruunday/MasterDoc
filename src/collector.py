from github import Github
import urllib.request
import os

def lst_repos(g):
    repo_lst = []
    for repo in g.get_user().get_repos():
        repo_lst.append(repo)
    return repo_lst

def get_docs_urls(repo_lst):
    docs_urllst = []
    # Goes through every repo in organisation
    for repo in repo_lst:
        contents = repo.get_contents("")
        # For every root file/directory
        for content_file in contents:
            # Find docs folder
            if content_file.type == 'dir' and content_file.name == 'docs':
                # Recursive search to find all files in repo
                folder = repo.get_contents(content_file.path)
                while len(folder) > 1:
                    file_content = folder.pop(0)
                    if file_content.type == "dir":
                        folder.extend(repo.get_contents(file_content.path))
                    else:
                        docs_urllst.append(file_content.download_url)
            elif content_file.name == 'README.md':
                docs_urllst.append(content_file.download_url)
    return docs_urllst

def create_file_struct(url_lst):
    for url in url_lst:
        url = url.split('/')
        repo = url[4]
        if repo == 'docs':
            repo = 'legacy_docs'
        folder = ''.join(url[7:-1])
        path = f'docs/{repo}/{folder}'
        if not os.path.isdir(path):
            os.makedirs(path)

def download_files(url_lst):
    contents_dict = {}
    for url in url_lst:
        surl = url.split('/')
        repo = surl[4]
        if repo == 'docs':
            repo = 'legacy_docs'
        folder = ''.join(surl[7:-1])
        name = surl[-1]
        filename = f'docs/{repo}/{folder}/{name}'
        if repo not in contents_dict:
            contents_dict[repo] = [name]
        else:
            contents_dict[repo].append(f'{folder}/{name}')
        urllib.request.urlretrieve(url, filename)
    return contents_dict

def write_contents(contents):
    header = """---
site_name: Redbrick Docs
theme: readthedocs
repo_url: https://github.com/gruunday/MasterDoc
strict: False
markdown_extensions:
  - pymdownx.tasklist
extra_javascript:
  - js/github.js
  - js/viz-lite.js
  - js/graphviz.js
extra_css:
  - css/custom.css
nav:
  - Home: index.md\n"""
    with open('mkdocs.yml', 'w') as f:
        f.write(header)
        for repo in contents:
            f.write(f'  - {repo}:\n')
            for page in contents[repo]:
                if page.split('.')[-1] == 'md':
                    if page[0] == '/':
                        page = page[1:]
                    f.write(f'      - {page.split("/")[-1]}: {repo}/{page}\n')

    
def usage():
    print("Work in progress")

def main():
    import config
    g = Github(config.github_secret)
    repo_lst = lst_repos(g)
    urls_lst = get_docs_urls(repo_lst)
    create_file_struct(urls_lst)
    contents = download_files(urls_lst)
    write_contents(contents)


if __name__ == '__main__':
    main()
