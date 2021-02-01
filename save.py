# -*- coding: UTF-8 -*-
from pyquery import PyQuery as q
from datetime import datetime

path_to_html_file = "content.html"
f_open = open(path_to_html_file)
content = ""
line = f_open.readline()
while line:
    content += line
    line = f_open.readline()
f_open.close()

d = q(content)
item_list = d(".m-timeline .m-dlist li.itm")
print(item_list.length)
song_list = []  # 去重复存储所有分享过的歌曲列表


# 如果上一行是日期，紧邻的下一行也是日期，并且两个时间戳一致则该行日期不再录用
last_timestamp = 0.0

def parse2time(title):
    y = datetime.strptime(title, '%Y年%m月%d日')
    global last_timestamp
    curre_timestam = y.timestamp()
    if curre_timestam == last_timestamp:
        return "--------------- 分割线 ---------------"
    else:
        last_timestamp = curre_timestam
        str = datetime.strftime(y, '	Date:	%Y年%m月%d日 GMT+8 23:59:59')
        return str

ret = ""
for item in item_list:
    date = q(q(item).find(".time")[0]).text()
    text = q(q(item).find(".text")[0]).text()
    song = q(q(item).find(".src.f-cb:not(.src-cmt):not(.src-video):not(.src-empty)"))  # 歌曲
    if song.length > 0:
        # print(song)
        song_title = q(song.find(".scnt .tit")[0]).text()
        song_author = q(song.find(".scnt .from")[0]).text()
        temp = "\n【歌曲】" + song_title + " - " + song_author
        song_list.append({song_author,song_title})
        text += temp

    forward = q(q(item).find(".src.src-cmt.f-cb.f-brk"))
    if forward.length > 0:
        # print(forward)
        _text = q(forward.find(".cemt.f-pr")[0]).text()
        temp = "\n【转发】" + _text + "\n"
        text += temp

    ret += "\n" + parse2time(date) + "\n\n" + text + "\n"

# print(ret)

# 文本写到文件中
export_file_path = "output.txt"
f_write = open(export_file_path, 'a')
f_write.write(ret)
f_write.close()

drop_song_list = []
for item in song_list:
    if not item in drop_song_list:
        drop_song_list.append(item)


print(len(drop_song_list))
