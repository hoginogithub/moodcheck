import csv

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

REVERSE_QUESTIONS = ['4', '8', '12', '16',]

def input_data():
    mood_list = []
    date = input('入力日(yyyymmdd)')
    mood_list.append(date)
    print(date)
    for num, msg in MOOD_MESSAGE.items():
        if num in REVERSE_QUESTIONS:
            check = int(input(num + ':' + msg + '(はい:0,いいえ:1)'))
        else:
            check = int(input(num + ':' + msg + '(はい:1,いいえ:0)'))
        mood_list.append(check)
    
    with open('mood_data_file', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(mood_list)
    
    print(mood_list[0]+'のデータを登録しました')

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
        elif menu_num == '9':
            val = False
            print('気分チェックを終了します')
            print('お疲れさまでした\n')
        else:
            print('1,2,9を入力してください')
            print('\n\n')
