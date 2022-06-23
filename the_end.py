import requests
import time

user_id = []
token = '5068878742:AAG8t2HuPO-9KxJQwbL71PVNXWEbdHMsbQA'
message = 'Привет, пользователь! \nНадеюсь этот бот хоть немного был тебе полезен и экономил твоё время. \nЕго поддержка прекращается с завтрашнего дня, поскольку я закончил обучение и меня забирают в армию 😁 \nИсходники этого бота доступны всем и взять их можно взять с моего github репозитория - https://github.com/lxvko/eetk \nЖелаю всем с кайфом провести это лето 😊'

def last_message(message):

    with open('user_id.txt') as file:
            user_id = [line.strip() for line in file]

    for req in range(len(user_id)):
        time.sleep(1)
        r = requests.get(f'https://api.telegram.org/bot{token}/sendMessage'
                        f'?chat_id={user_id[req]}&text={message}')
        print(f'{user_id[req]} has been sent')
        
if __name__ == '__main__':
    last_message(message)
