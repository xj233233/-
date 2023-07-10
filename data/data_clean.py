import re


def clean(book_list):
    BOOKS = book_list
    c1 = '群众出版社'
    c2 = ' 1981-8 '

    for book in BOOKS:

        if book['出版社'] == c2:
            book['出版社'] = c1  # 修改
            book['出版时间'] = c2
            book['价格'] = '53.00'
        # 将评论人数更换为数字
        book['评价人数'] = int(''.join(filter(str.isdigit, str(book['评价人数']))))

        # 只保留数字和小数点
        book['价格'] = ''.join(filter(lambda ch: ch in '0123456789.', str(book['价格'])))

        # 出版年份
        book['出版时间'] = ''.join(filter(str.isdigit, str(book['出版时间'])))[:4]

        # 确认国家
        country = book['国家']
        book['国家'] = country.replace('国', '')
        if book['国家'] == '清' or book['国家'] == '明':
            book['国家'] = '中'  # 修改

        elif book['书名'] == '哈利·波特':
            book['国家'] = '英'

        elif book['书名'] == '厌女':
            book['国家'] = '日'

        elif book['书名'] == '美丽新世界':
            book['国家'] = '英'


        elif book['书名'] == '人生的智慧':
            book['国家'] = '德'


        elif book['书名'] == '你当像鸟飞往你的山':
            book['国家'] = '美'


        elif book['书名'] == '海的女儿':
            book['国家'] = '丹麦'


        elif book['书名'] == '不能承受的生命之轻':
            book['国家'] = '法'


        elif book['书名'] == '冰与火之歌':
            book['国家'] = '美'


        elif book['书名'] == '平面国':
            book['国家'] = '英'


        elif book['书名'] == '地下室手记':
            book['国家'] = '白俄'


        elif book['书名'] == '流俗地':
            book['国家'] = '马来西亚'

    print('当前书籍信息：')
    for i in BOOKS[:]:
        print(i)

    return BOOKS
