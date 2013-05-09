# -*- coding: utf-8 -*-
import sys
import os
import re
import markup

styles = '../style.css'
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

try:
    os.makedirs('html')
except OSError, exc:
    pass
with open('html/index.html', 'w') as f:
    chapters = ['<a href="chapter%s.html">%s</a>' % re.match(r'^\\(\d+)\s*(.*)', i).groups() for i in lines if re.match(r'^\\\d+', i)]
    title = lines[0].strip()
    page = markup.page()
    page.init(css=styles, title=title, charset='utf-8', lang='zh-CN')
    page.h1(title)
    page.div(id_='box')
    page.div('目录', class_='header')
    page.ul()
    page.li(chapters)
    page.ul.close()
    page.div('This page is make by Simplex 1.0', id_='footer')
    page.div.close()
    f.write(str(page))
    for i in range(1, len(chapters) + 1):
        page = markup.page()
        index = []
        for j in range(0, len(lines)):
             if re.match(r'^\\\d+', lines[j]):
                 index.append(j)
        t = index[i-1]
        start = t + 1
        if i < len(index):
            end = index[i]
        else:
            end = len(lines)
        title = re.match(r'^\\\d+\s*(.*)', lines[t]).group(1)
        paragraphs = lines[start:end]
        links = []
        if i == 1:
            x = i + 1
            links.append('<a href="index.html">目录</a>')
            links.append('<a href="chapter%d.html">下一章</a> ' % x)
        elif i == len(index):
            x = i - 1
            links.append('<a href="chapter%d.html">上一章</a> ' % x)
            links.append('<a href="index.html">目录</a>')
        else:
            x = i - 1
            links.append('<a href="chapter%d.html">上一章</a> ' % x)
            links.append('<a href="index.html">目录</a> ')
            x = i + 1
            links.append('<a href="chapter%d.html">下一章</a>' % x)
        with open('html/chapter%d.html' % i, 'w') as f:
            page.init(css=styles, title=title, charset='utf-8', lang='zh-CN')
            page.h1(lines[0].strip())
            page.div(id_='navigationColumn')
            page.div('导航', class_='header')
            page.ul()
            page.li(links)
            page.ul.close()
            page.div.close()
            page.div(id_='box')
            page.div(class_='article')
            page.div(title, class_="title")
            page.p(paragraphs)
            page.div(class_='right')
            page.span(links, class_='button')
            page.div.close()
            page.div.close()
            page.div('This page is make by Simplex 1.0', id_='footer')
            page.div.close()
            f.write(str(page))

