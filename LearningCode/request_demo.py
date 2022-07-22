import requests

import json
# sign_plain = "WwanDdou" + "" + base64img + "" + "vgdffs"
# hl = hashlib.md5()
# hl.update(sign_plain.encode(encoding='utf-8'))
# sign_cipher = hl.hexdigest()
# params = {
#     'sign': sign_cipher,
#     'typeId': '',
#     'image': base64img,
#     'assetType': ''
# }
# resp = requests.post(json=params, url='https://pam-openapi.secmind.cn/api/captcha/identity')
# resp_data = json.loads(resp.text)
# if resp_data.get('success') is True:
#     img_text = resp_data.get('code')





if __name__ == '__main__':
    url = ''
    params = {
        '': ''
    }

    response = requests.get('https://api.github.com')
    if response:
        print('Success!')
        print(response.text)
        print(response.content)
        response_json = response.json()
        user_url = response_json.get('current_user_url')
        print(user_url)
    else:
        print('An error has occurred.')
