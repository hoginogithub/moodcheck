import csv
import datetime

MOOD_MESSAGE = {
    '1': '普段は何でもないことがわずらわしい。',
    '2': '食べたくない。食欲が落ちた。',
    '3': '家族や友達からはげましてもらっても、気分が晴れない。',
    '4': '他の人と同じ程度には、能力があると思う。',
    '5': '物事に集中できない。',
    '6': 'ゆううつだ。',
    '7': '何をするのにも面倒だ。',
    '8': 'これから先のことについて積極的に考えることができる',
    '9': '過去のことについてくよくよ考える。',
    '10': '何か恐ろしい気持ちがする。',
    '11': 'なかなか眠れない。',
    '12': '生活について不満なくすごせる。',
    '13': '普段より口数が少ない。口が重い。',
    '14': '一人ぼっちでさびしい。',
    '15': '皆がよそよそしいと思う。',
    '16': '毎日が楽しい。',
    '17': '急に泣きだすことがある。',
    '18': '悲しいと感じる。',
    '19': '皆が自分をきらっていると感じる。',
    '20': '仕事が手につかない。',
}

DATA_FILE = 'mood_data_file'

REVERSE_QUESTIONS = ['4', '8', '12', '16',]

def is_valid_date(date):
    try:
        yyyy = int(date[0:4])
        mm = int(date[4:6])
        dd = int(date[6:8])
        datetime.date(yyyy,mm,dd)
    except:
        print('正しい日付を入力してください')
        return False
    else:
        return True

def is_valid_choice(choice):
    if choice in ['0', '1']:
        return True
    else:
        print('0か1を入力してください')
        return False

def get_str_date(date, delta_days):
    yyyy = int(date[0:4])
    mm = int(date[4:6])
    dd = int(date[6:8])
    base_date = datetime.date(yyyy,mm,dd)
    result_date = base_date - datetime.timedelta(days=delta_days)
    return result_date.strftime('%Y%m%d')

def get_str_today():
    return datetime.date.today().strftime('%Y%m%d')

def get_str_yesterday():
    str_today = datetime.date.today().strftime('%Y%m%d')
    return get_str_date(str_today, 1)

def interpret_date(date):
    dict_date = {'0': get_str_today(), '1': get_str_yesterday()}
    try:
        date = dict_date[date]
    finally:
        return date

def get_mood_point_sum(from_date, to_date):
    with open(DATA_FILE, encoding='utf-8') as f:
        reader = csv.reader(f)
        mood_point_list = []
        for row in reader:
            if from_date <= row[0] <= to_date:
                mood_point_list.append(list(map(lambda x: int(x), row[1:])))

    return [sum(i) for i in zip(*mood_point_list)]

def get_mood_point(count):
    if count == 0:
        return 0
    if 1 <= count <=2:
        return 1
    if 3 <= count <= 4: 
        return 2
    return 3

def is_data_exist(date):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if date in row:
                return True
    return False

def input_data():
    print('データ入力を開始します\n')
    mood_list = []
    loop = True
    while loop:
        date = input('入力日(yyyymmdd or 今日:0, 昨日:1)')
        date = interpret_date(date)
        loop = not(is_valid_date(date))
    if is_data_exist(date):
        print(date + 'は、既に登録済みです')
        return
    mood_list.append(date)
    for num, msg in MOOD_MESSAGE.items():
        loop = True
        while loop:
            if num in REVERSE_QUESTIONS:
                choice = input(num + ':' + msg + '(0:はい:,1:いいえ)')
            else:
                choice = input(num + ':' + msg + '(1:はい,0:いいえ)')
            loop = not(is_valid_choice(choice))
        mood_list.append(int(choice))
    
    with open(DATA_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(mood_list)
    
    print(mood_list[0]+'のデータを登録しました')

    print('\n')

def aggregate_data():
    print('気分チェックを集計します\n')
    loop = True
    while loop:
        date = input(f'集計基準日(yyyymmdd or 今日:0, 昨日:1)')
        date = interpret_date(date)
        loop = not(is_valid_date(date)) 
    from_date = get_str_date(date, 6)
    to_date = get_str_date(date, 0)
    before_from_date = get_str_date(date, 13)
    before_to_date = get_str_date(date, 7)

    print('- 集計結果 -')
    print(from_date + ' - ' + to_date)

    mood_point_sum = get_mood_point_sum(from_date, to_date)
    before_point_sum = get_mood_point_sum(before_from_date, before_to_date)
    total_point = 0
    before_total_point = 0

    for k, x in enumerate(list(zip(mood_point_sum, before_point_sum))):
        mood_point = get_mood_point(x[0])
        before_mood_point = get_mood_point(x[1])
        str_diff_point = f' ({mood_point - before_mood_point:+})'
        print(str(k+1) + ':' + MOOD_MESSAGE[str(k+1)] + '=' + str(mood_point) + '点' + str_diff_point)
        total_point += mood_point
        before_total_point += before_mood_point
    str_diff_total_point = f' ({total_point - before_total_point:+})'
    print('合計:' + str(total_point) + '点'+ str_diff_total_point)
    input('input any buttun')
    print('')

def delete_data():
    print('削除したいデータを指定してください\n')
    loop = True
    while loop:
        date = input('削除対象日(yyyymmdd or 今日:0, 昨日:1)')
        date = interpret_date(date)
        loop = not(is_valid_date(date))
    if not(is_data_exist(date)):
        print('指定された日付のデータは存在しませんでした\n')
        return
    ret = input(date + 'のデータを削除してよろしいですか?(y,n)')
    if not(ret == 'y'):
        return
    data_list = []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not(date in row):
                data_list.append(row)
    with open(DATA_FILE, 'r+') as f:
        f.truncate(0)
    with open(DATA_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for data in data_list:
            writer.writerow(data)
    print(date + 'のデータを削除しました\n')

def display_data():
    print('照会したい日付を入力してください\n')
    loop = True
    while loop:
        date = input('入力日(yyyymmdd or 今日:0, 昨日:1)')
        loop = not(is_valid_date(date))
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if date in row:
                for num, msg in MOOD_MESSAGE.items():
                    if num in REVERSE_QUESTIONS:
                        print(num + ':' + msg + '(0:はい:,1:いいえ)'+ row[int(num)])
                    else:
                        print(num + ':' + msg + '(1:はい,0:いいえ)'+ row[int(num)])
                print('\n')
                return
    print('該当する日付のデータは入力されていません')

    print('\n')

def list_one_week():
    today = datetime.date.today().strftime('%Y%m%d')
    week_list = []
    check_list = ['×' for i in range(0, 7)]
    for i in range(7, 0, -1):
        week_list.append(get_str_date(today, i))
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                check_list[week_list.index(row[0])] = '〇'
            except:
                pass
    for i in range(0, 7):
        print(week_list[i] + "->" + check_list[i])

    print('\n')

if __name__ == "__main__":
    val = True
    while val == True:
        print('== 気分チェック (ver 1.3)==')
        print(f'本日は{get_str_today()}')
        print('メニューを選んでください')
        print('1:データ入力')
        print('2:集計')
        print('3:データ削除')
        print('4:データ照会')
        print('5:過去7日間の入力状況')
        print('9:終了')
        menu_num = input()
        if menu_num == '1':
            input_data()
        elif menu_num == '2':
            aggregate_data()
        elif menu_num == '3':
            delete_data()
        elif menu_num == '4':
            display_data()
        elif menu_num == '5':
            list_one_week()
        elif menu_num == '9':
            val = False
            print('気分チェックを終了します')
            print('お疲れさまでした\n')
        else:
            print('1,2,3,4,5,9を入力してください')
            print('\n\n')
