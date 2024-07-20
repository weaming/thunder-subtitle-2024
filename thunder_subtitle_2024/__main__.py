import urllib.request
from .tools import gcid_hash_file

import requests
from drawtable import Table


def get_subs(gid: str, max_retry_times: int = 0):
    """
    {
        "gcid": "7B68ABD4268D41696F4FD8B791EE458792272838",
        "cid": "7B68ABD4268D41696F4FD8B791EE458792272838",
        "url": "https://subtitle.v.geilijiasu.com/7B/68/7B68ABD4268D41696F4FD8B791EE458792272838.srt",
        "ext": "srt",
        "name": "eng.srt",
        "duration": 3552000,
        "languages": [
            "eng"
        ],
        "source": 0,
        "score": 10000000,
        "fingerprintf_score": 83.13,
        "fingerprintf_status": "success",
        "star": "5"
    }
    """
    url = f'https://api-shoulei-ssl.xunlei.com/oracle/subtitle?gcid={gid}'
    result = None
    if max_retry_times <= 0:
        while True:
            res = requests.get(url)
            if res.status_code == 200:
                result = res.json()['data']
                break
    else:
        for i in range(max_retry_times):
            res = requests.get(url)
            if res.status_code == 200:
                result = res.json()['data']
                break
    return [i for i in result if i]


def search(fp):
    gid = gcid_hash_file(fp)
    return get_subs(gid, 1000)


def get_url(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return data


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='movie path')
    parser.add_argument('-i', '--index', type=int, help='index to download')
    args = parser.parse_args()

    subs = search(args.path)
    if subs is None:
        print("超过最大重试次数后仍然未能获得正确结果")
    else:
        subs.sort(key=lambda x: x['star'], reverse=True)

        if args.index:
            sub = subs[args.index - 1]
            name, url = sub['name'], sub['url']
            sub_ext = url.rsplit('.', 1)[1]
            data = get_url(url)

            movie_file_path_wo_ext = args.path.rsplit('.', 1)[0]
            sub_file_path = movie_file_path_wo_ext + '.' + sub_ext
            with open(sub_file_path, 'wb') as f:
                f.write(data)
            print('Downloaded {}'.format(sub_file_path))
        else:
            rows = [
                ['Index', 'Rate', 'Votes', 'Language', 'Name', 'URL'],
            ]
            for i, x in enumerate(subs, start=1):
                row = [
                    str(i),
                    x['star'],
                    str(x['fingerprintf_score']),
                    ' '.join(x['languages']),
                    x['name'],
                    x['url'],
                ]
                rows.append(row)

            tb = Table(
                margin_x=1,
                margin_y=0,
                align='left',
                max_col_width=100,
                table_style='base',
            )
            tb.draw(rows)


if __name__ == '__main__':
    main()
