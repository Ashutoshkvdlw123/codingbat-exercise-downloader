import requests
import os
import textwrap
from bs4 import BeautifulSoup

url = "http://codingbat.com/"
cwd = os.getcwd()

def get_exes():
    result = requests.get(url + "/python")
    if int(result.status_code) == 200:
        soup = BeautifulSoup(result.content, "html.parser")
        anchors = soup.find_all("a")

        exe_links = {}

        for anchor in anchors:
            link = anchor.attrs["href"]
            if "python/" in link:
                exe_links[anchor.text] = url + link
        return exe_links

    return result.status_code

def visit_exes(exe_links):
    all_links = {}
    for exe in exe_links:
        res = requests.get(exe_links[exe])
        if int(res.status_code) == 200:
            soup = BeautifulSoup(res.content, "html.parser")
            anchors = soup.find_all("a")

            links = {}

            for anchor in anchors:
                if "prob/" in anchor.attrs['href']:
                    links[anchor.text] = url+anchor.attrs['href']
            all_links[exe] = links
        else:
            return res.status_code
    return all_links

class Exercise:
    def __init__(self, exe_name, des, func_str):
        self.name = exe_name
        self.des = "\n#".join(textwrap.wrap(des))
        self.func_str = func_str
        self.file_text = '#{0}\n\n{1}'.format(self.des, self.func_str)
        
    def create_file(self, path):
        file = open(os.path.join(path, f"{self.name}.py"), "w")
        with file:
            file.write(self.file_text)

    def __repr__(self):
        return f"Exercise(name='{self.name}', des='{self.des[:10]}...', func_str='{self.func_str}')"

def get_info(all_links):
    exes = {}
    for exe in all_links:
        links = all_links[exe]
        exes2 = {}
        for link in links:
            res = requests.get(links[link])
            if int(res.status_code) == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                des = soup.find("p", class_="max2").text
                func_str = soup.find(id="ace_div").text
                exe_name = link
                exe_obj = Exercise(exe_name, des, func_str)
                exes2[exe_name] = exe_obj
            else:
                return res.status_code

        exes[exe] = exes2
    return exes

def create_files(info, master_dir="codingbat-practice"):
    master_dir_path = os.path.join(cwd, master_dir)
    os.mkdir(master_dir_path)
    for exe in info:
        info2 = info[exe]
        exe_path = os.path.join(master_dir_path, exe)
        os.mkdir(exe_path)
        for exe2 in info2:
            exe_obj = info2[exe2]
            exe_obj.create_file(exe_path)


if __name__ == "__main__":
    print("Stage 1 initiated...")
    exe_links = get_exes()
    print("Done.")
    print("Stage 2 initiated...")
    all_links = visit_exes(exe_links)
    print("Done")
    print("Stage 3 initiated...")
    info = get_info(all_links)
    print(info)
    create_files(info)
    print("All Done.")
