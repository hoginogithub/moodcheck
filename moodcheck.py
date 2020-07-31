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
        elif menu_num == '2':
            print('気分チェックを集計します\n')
        elif menu_num == '9':
            val = False
            print('気分チェックを終了します')
            print('お疲れさまでした\n')
        else:
            print('1,2,9を入力してください')
            print('\n\n')
