

import argparse
from db_helper import DBHelper

def parse_args():
    parser = argparse.ArgumentParser(description='CRUD CLI для таблицы users')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('add', help='Добавить пользователя')
    p.add_argument('--name',  required=True, help='Имя')
    p.add_argument('--age',   type=int, required=True, help='Возраст')
    p.add_argument('--email',           help='Email')
    p.add_argument('--skills', help = 'Навыки')

    sub.add_parser('list', help='Показать всех пользователей')

    p = sub.add_parser('find', help='Найти пользователя по ключевому слову')
    p.add_argument('--keyword', required=True, help='Часть имени или email')

    p = sub.add_parser('update', help='Обновить данные пользователя')
    p.add_argument('--id',    type=int, required=True, help='ID пользователя')
    p.add_argument('--name',           help='Новое имя')
    p.add_argument('--age',    type=int, help='Новый возраст')
    p.add_argument('--email',          help='Новый email')
    p.add_argument('--skills',  help = 'Новые навыки')

    p = sub.add_parser('delete', help='Удалить пользователя по ID')
    p.add_argument('--id', type=int, required=True, help='ID пользователя')


    sub.add_parser('stats', help='Показать статистику по пользователям')

    return parser.parse_args()

def main():
    args = parse_args()
    db = DBHelper()

    if args.cmd == 'add':
        uid = db.add_user(args.name, args.age, args.email, args.skills)
        print(f' Пользователь создан с ID={uid}')

    elif args.cmd == 'list':
        rows = db.get_all_users()
        print("ID | Name       | Age | Email | Skills")
        print("---------------------------------------------")
        for r in rows:
            print(f"{r['id']:2d} | {r['name']:<10} | {r['age'] or '-':>3} | {r['email']  or '-'} | {r['skills'] or '-'}")

    elif args.cmd == 'find':
        rows = db.find_users(args.keyword)
        if rows:
            for r in rows:
                print(f"{r['id']}: {r['name']} ({r['age']}), {r['email']}, {r['skills']}")
        else:
            print("Ничего не найдено.")

    elif args.cmd == 'update':
        count = db.update_user(args.id, args.name, args.age, args.email, args.skills)
        if count:
            print(f' Обновлено строк: {count}')
        else:
            print(" Нечего обновлять или пользователь не найден.")

    elif args.cmd == 'delete':
        count = db.delete_user(args.id)
        print(f' Удалено строк: {count}')
    
    


    elif args.cmd == 'stats':
        stats = db.get_stats()
        print(f"Всего пользователей: {stats['total_users']}")
        print(f"Средний возраст: {stats['avg_age'] or 0}")
        print(f"Уникальных email-адресов: {stats['unique_emails']}")
        print(f"Уникальных навыков: {stats['unique skills']}")

if __name__ == '__main__':
    main()