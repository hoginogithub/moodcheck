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

def input_data():
    mood_list = []
    loop = True
    while loop:
        date = input('入力日(yyyymmdd)')
        loop = not(is_valid_date(date))
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

def get_str_date(date, delta_days):
    yyyy = int(date[0:4])
    mm = int(date[4:6])
    dd = int(date[6:8])
    base_date = datetime.date(yyyy,mm,dd)
    result_date = base_date - datetime.timedelta(days=delta_days)
    return result_date.strftime('%Y%m%d')

def aggregate_data():
    loop = True
    while loop:
        date = input('集計基準日(yyyymmdd)')
        loop = not(is_valid_date(date)) 
    from_date = get_str_date(date, 7)
    to_date = get_str_date(date, 0)
    print('- 集計結果 -')
    print(from_date + ' - ' + to_date)

    with open(DATA_FILE, encoding='utf-8') as f:
        reader = csv.reader(f)
        mood_point_list = []
        for row in reader:
            if from_date <= row[0] <= to_date:
                mood_point_list.append(list(map(lambda x: int(x), row[1:])))

    mood_point_sum = [sum(i) for i in zip(*mood_point_list)]
    total_point = 0
    for k, x in enumerate(mood_point_sum):
        mood_point = 0 if x == 0 else (1 if 1 <= x <=2 else (2 if 3 <= x <= 4 else 3))
        print(str(k+1) + ':' + MOOD_MESSAGE[str(k+1)] + '=' + str(mood_point) + '点')
        total_point += mood_point
    print('合計:' + str(total_point) + '点')

    print('\n')

if __name__ == "__main__":
    val = True
    while val == True:
        print('== 気分チェック ==')
        print('メニューを選んでください')
        print('1:データ入力')
        print('2:集計')
        print('9:終了')
        menu_num = input()
        if menu_num == '1':
            print('データ入力を開始します\n')
            input_data()
        elif menu_num == '2':
            print('気分チェックを集計します\n')
            aggregate_data()
        elif menu_num == '9':
            val = False
            print('気分チェックを終了します')
            print('お疲れさまでした\n')
        else:
            print('1,2,9を入力してください')
            print('\n\n')
