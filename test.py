import json
import os
import time
from Pushover import Pushover
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


def check_for_new_listing():
    api = MobyAPI()
    push = Pushover(os.environ['MOBY_API_KEY'])
    top_ = api.top_picks(decode_json=True)
    first = top_.__next__().items[1].title
    while True:
        next_stock = api.top_picks(decode_json=True).__next__().items[0]
        if next_stock != first:
            print('New Listing:', next_stock.title)
            first = next_stock.title
            push.send_message(
                user_key=os.getenv('MBSP_USER_KEY'),
                message='New stock acquired {}'.format(next_stock.title),
                title='MBSP Fund'
            )
            break

        time.sleep(60*60)


if __name__ == '__main__':
    # get_i_page(6)
    check_for_new_listing()