import os
import json
import time
import random
from Pushover import Pushover, Priority
from dotenv import load_dotenv
from mobyapi import MobyAuthenticatedAPI, MobyAPI

load_dotenv()

def get_i_page(x):
    os.system('rm -rf top_picks')
    os.mkdir('top_picks')
    os.chdir('top_picks')
    api = MobyAuthenticatedAPI(
        jwt=os.getenv('JWT'),
        jwt_user_id='446739'
    )
    top_ = api.top_picks(decode_json=False)
    pages = 0
    total_companies = []
    for i in top_:
        pages += 1
        print('Downloading Page:', pages)
        with open('top_picks_pg={}.json'.format(pages), 'w') as f:
            f.write(json.dumps(i))

        for item in i['items']:
            total_companies.append(item['title'])

        if pages == x:
            break

    print('Total unique companies:', len(total_companies))
    os.system('open .')
    os.chdir('..')


def generate_stock_announcement(stock_info):
    # Extract company name and ticker
    company = stock_info.split('(')[0].strip()
    ticker = stock_info.split('(')[1].replace(')', '')

    templates = [
        f"MBSP Scanner has identified {company} ({ticker}) as a potential opportunity for analysis.",
        f"New Market Detection: {company} ({ticker}) has emerged on MBSP's screening criteria.",
        f"MBSP Alert: {company} ({ticker}) meets preliminary scanning parameters.",
        f"System Notification: {company} ({ticker}) has been flagged for potential review.",
        f"MBSP Discovery: {company} ({ticker}) warrants further investigation.",
        f"Automated Detection: {company} ({ticker}) has satisfied initial screening metrics.",
        f"MBSP Scanner Report: {company} ({ticker}) identified for consideration.",
        f"Market Intelligence: {company} ({ticker}) detected by MBSP screening protocols.",
        f"New Detection Alert: {company} ({ticker}) flagged by MBSP system analysis.",
        f"MBSP Screening Result: {company} ({ticker}) presented for evaluation.",
        f"System Alert: {company} ({ticker}) has triggered MBSP detection criteria.",
        f"Market Surveillance: {company} ({ticker}) identified by MBSP protocols.",
        f"Detection Notice: {company} ({ticker}) has met MBSP screening thresholds.",
    ]

    return random.choice(templates)

def check_for_new_listing():
    api = MobyAPI()
    push = Pushover(os.environ['MOBY_API_KEY'])
    top_ = api.top_picks(decode_json=True)
    first = top_.__next__().items[1].title
    sleep_multiplier_range = (5,10)
    while True:
        next_stock = api.top_picks(decode_json=True).__next__().items[0]
        if next_stock != first:
            print('New Listing:', next_stock.title)
            first = next_stock.title
            push.send_message(
                user_key=os.getenv('MBSP_USER_KEY'),
                message=generate_stock_announcement(next_stock.title),
                title='MBSP Fund',
                priority=Priority.NORMAL,
                expire=5,
                retry=60,
                monospace=True
            )

        next_update_in = 60*random.randint(*sleep_multiplier_range)
        print('Next update in: {}m'.format(next_update_in/60))
        time.sleep(next_update_in)


if __name__ == '__main__':
    # get_i_page(6)
    check_for_new_listing()