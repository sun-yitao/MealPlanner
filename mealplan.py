import argparse
import arrow
from ics import Calendar, Event
import random


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plan your meals.')
    parser.add_argument('--start-date', type=str,
        default=arrow.utcnow().to('Asia/Singapore').format('DD-MM-YY'),
        required=False, help='dd-mm-yy, default: today')
    parser.add_argument('--num-days', type=int, default=7,
                        required=False, help='num days to plan, default: 7')
    parser.add_argument('--lunch-time', type=str, default='12:30',
                        required=False, help='hh:mm, default: 12:30')
    parser.add_argument('--dinner-time', type=str, default='18:30',
                        required=False, help='hh:mm, default: 18:30')
    parser.add_argument('--exclude-weekends', action='store_true',
                        help='whether to exclude weekends for planning')
    parser.add_argument('--exclude-lunch', action='store_true',
                        help='whether to exclude lunch for planning')
    parser.add_argument('--exclude-dinner', action='store_true',
                        help='whether to exclude dinner for planning')
    args = parser.parse_args()

    acceptable_foods = [  # EDIT HERE
        'Udon don', 'Hwangs', 'Sapore', 'Dumplings', 'Salad', 'Wok Fried',
        'Chicken Rice', 'Cai Fan', 'Noodles'
    ]
    random.shuffle(acceptable_foods)
    print(f'Start date: {args.start_date}')
    start_day_of_week = arrow.get(args.start_date, 'DD-MM-YY').weekday()

    c = Calendar()
    cnt = 0
    for i in range(args.num_days):
        if args.exclude_weekends and (start_day_of_week + i) % 7 > 4:
            continue
        if not args.exclude_lunch:
            e = Event()
            e.name = 'Lunch: ' + acceptable_foods[cnt % len(acceptable_foods)]
            date = arrow.get(args.start_date + ' ' + args.lunch_time,
                             'DD-MM-YY HH:mm', tzinfo='Asia/Singapore')
            e.begin = date.shift(days=i)
            e.duration = {'minutes': 30}
            c.events.add(e)
            cnt += 1

        if not args.exclude_dinner:
            e = Event()
            e.name = 'Dinner: ' + acceptable_foods[cnt % len(acceptable_foods)]
            date = arrow.get(args.start_date + ' ' + args.dinner_time,
                             'DD-MM-YY HH:mm', tzinfo='Asia/Singapore')
            e.begin = date.shift(days=i)
            e.duration = {'minutes': 30}
            c.events.add(e)
            cnt += 1

    with open('planned_foods.ics', 'w') as my_file:
        my_file.writelines(c)
    print('Saved to planned_foods.ics in current directory')
