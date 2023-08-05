class parser:

    def SongParse(to_parse):
        s = to_parse #I feel more confident with shorter variables
        formatted_url = s[13].replace('%3A', ':').replace('%2F', '/')
        res = {
            'name': s[3],
            'id': int(s[1]),
            'size_mb': f'{s[9]} MB',
            'size': float(s[9]),
            'author': s[7],
            'links': [
                f'https://www.newgrounds.com/audio/listen/{s[1]}',
                formatted_url
            ]
        }
        return res
