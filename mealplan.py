import argparse
import arrow
from ics import Calendar, Event
import random


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plan your meals.')
    parser.add_argument('--start-date', type=str,
        default=arrow.utcnow().to('Asia/Singapore').format('DD-MM-YY'),
        required=False, help='dd-mm-yy, default: today')
    parser.add_argument('--lunch-time', type=str, default='12:30',
                        required=False, help='hh:mm, default: 12:30')
    parser.add_argument('--dinner-time', type=str, default='18:30',
                        required=False, help='hh:mm, default: 18:30')
    args = parser.parse_args()
    print(f'Start date: {args.start_date}')
    acceptable_foods = [
        'Udon don', 'Hwangs', 'Sapore', 'Dumplings', 'Salad', 'Wok Fried',
        'Chicken Rice', 'Cai Fan', 'Noodles'
    ]
    random.shuffle(acceptable_foods)

    ptr = 0
    num_days = 7
    planned_foods = []
    for _ in range(num_days * 2):
        planned_foods.append(acceptable_foods[ptr % len(acceptable_foods)])
        ptr += 1

    c = Calendar()
    for i, planned_food in enumerate(planned_foods):
        is_lunch = i % 2 == 0
        prefix = 'Lunch: ' if is_lunch else 'Dinner: '
        e = Event()
        e.name = prefix + planned_food
        time = args.lunch_time if is_lunch else args.dinner_time
        date = arrow.get(args.start_date + ' ' + time, 'DD-MM-YY HH:mm',
                         tzinfo='Asia/Singapore')
        e.begin = date.shift(days=i // 2)
        e.duration = {'minutes': 30}
        c.events.add(e)

    with open('planned_foods.ics', 'w') as my_file:
        my_file.writelines(c)
    print('Saved to planned_foods.ics in current directory')
