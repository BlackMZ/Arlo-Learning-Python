from urllib.parse import urlparse


def get_url(url):
    return urlparse(url)

if __name__ == '__main__':
    url = "http://pam.secminddev.com/loginToWorkspace/?type=mysql&server=81.68.195.21&port=3366&database=mall&user=root&password=ZEc5dmNtMTVjM0Zz&connectionId=62d7afcd46b71c57e107d017"
    res = get_url(url)
    print(res)
    print("scheme : ", res.scheme)
    print("domain : ", res.netloc)
    print("pth : ", res.path)
    print("params : ", res.hostname)
    base_path = res.netloc