import requests
from datetime import datetime, timedelta
import json
import time
import re

def setup_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://events.cmu.edu/day/date/20241027',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'no-cache',
        'Cookie': '__qca=P0-771564247-1701817906494; _ce.s=v~84f8b8b82c204077f8fb5f75502b86e3e595651e~lcw~1712257303225~lva~1712257275023~vpv~2~gtrk.la~lpsyhhek~v11.cs~413867~v11.s~b61584d0-f2b5-11ee-a145-a7dfb633a605~v11.sla~1712257303250~v11.send~1712257303225~lcw~1712257303254; _fbp=fb.1.1688406471683.1257655992; _ga=GA1.2.1487770604.1687883194; _ga_1XQYSMEBVE=GS1.1.1724638571.59.0.1724640167.60.0.0; _ga_4EXR1GJJ46=GS1.1.1724643520.56.0.1724643520.0.0.0; _ga_4PZK4PW5B6=GS1.1.1693323812.2.0.1693323812.0.0.0; _ga_6Z5FJHJW2Y=GS1.1.1724730157.2.0.1724730166.0.0.0; _ga_98MDFNBLD8=GS1.1.1714100746.3.0.1714100966.0.0.0; _ga_98SSBVQRP4=GS1.1.1707854693.1.1.1707854712.0.0.0; _ga_CSELMMLRMD=GS1.1.1726692767.3.0.1726692767.0.0.0; _ga_M7YM8JM31D=GS1.2.1712095059.14.1.1712095072.0.0.0; _ga_MPLCXBBXZ5=GS1.1.1727829560.15.0.1727829560.0.0.0; _ga_P112DV9K94=GS1.1.1724638571.47.0.1724640167.0.0.0; _ga_P37Z42P5CR=GS1.1.1690300957.7.1.1690301066.0.0.0; _ga_T8DQDJVNHS=GS1.1.1712257274.1.1.1712257303.0.0.0; _ga_V7S2SH5H31=GS1.1.1688406470.1.1.1688406977.0.0.0; _ga_YLGZ7W2PRE=GS1.2.1707497347.1.1.1707497402.0.0.0; _hp2_id.3001039959={\'userId\':\'7968758830669240\',\'pageviewId\':\'5644623558827062\',\'sessionId\':\'7933332228146266\',\'identity\':\'uu-2-4238c0309ea03f3c838eca35086c93b7223ba9bbfeb2924b35b0aa2c75840042-DIaU25Do2cCPgvrq077VyeLlWOqVJBOryZuHIMrU\',\'trackerVersion\':\'4.0\',\'identityField\':null,\'isIdentified\':1}; _hp2_props.3001039959={\'Base.appName\':\'Canvas\'}; AWSALB=yPFca/CVsvXearvL3yDW2HQ9LB6FrexabST2clkCJSRfSf8PxK2YxJHJHTdT+lIVVcN/e61g7NPRsmFY/FkWeriD5p0c4mEW2cNc/ZsTYz6Xu+Xz5yDptH5zHs8a; AWSALBCORS=yPFca/CVsvXearvL3yDW2HQ9LB6FrexabST2clkCJSRfSf8PxK2YxJHJHTdT+lIVVcN/e61g7NPRsmFY/FkWeriD5p0c4mEW2cNc/ZsTYz6Xu+Xz5yDptH5zHs8a; clive-visitor-tid-156=lpsyfv0q7wjqyrueosn2wsv9d4pul8vnjn35xcbrkbq8ideh3p313pz90qk6eikm; nmstat=6d0da60a-8b62-fe19-9dd7-7a537ead6a93'    }


# Initialize session and headers
session = requests.Session()
headers = setup_headers()

def clean_description(description):
    description = re.sub(r'<.*?>', '', description)  # Remove HTML tags
    description = re.sub(r'\s+', ' ', description).strip()  # Remove excess whitespace
    return description

def fetch_events_for_date(date):
    formatted_date = date.strftime('%Y%m%d')
    url = f"https://events.cmu.edu/live/calendar/view/day/date/{formatted_date}?user_tz=America%2FDetroit&template_vars=id,latitude,longitude,location,time,href,image_raw,title_link,summary,until,is_canceled,is_online,image_src,repeats,is_multi_day,is_first_multi_day,multi_day_span,tag_classes,category_classes,has_map&syntax=%3Cwidget%20type%3D%22events_calendar%22%3E%3Carg%20id%3D%22mini_cal_heat_map%22%3Etrue%3C%2Farg%3E..."
    response = session.get(url, headers=headers)
    
    print(f"Fetching events for {formatted_date} - Status code: {response.status_code}")
    
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Failed to fetch data for {formatted_date}: {response.status_code}")
        return None

# Start and end dates
start_date = datetime(2024, 10, 27)
end_date = datetime(2025, 5, 31)

all_events = []

# Iterate over the date range
current_date = start_date
while current_date <= end_date:
    events = fetch_events_for_date(current_date)
    if events and 'events' in events:
        for event in events['events']:
            # Format date, time, and clean the description
            event_data = {
                'date': datetime.fromtimestamp(event['ts_start']).strftime('%Y-%m-%d'),
                'time': f"{datetime.fromtimestamp(event['ts_start']).strftime('%H:%M')} - {datetime.fromtimestamp(event['ts_end']).strftime('%H:%M')}",
                'title': event.get('title', 'No title available'),
                'description': clean_description(event.get('summary', 'No description available')),
                'location': event.get('location', 'No location available')
            }
            all_events.append(event_data)
    
    # Add a delay to avoid rate-limiting
    time.sleep(3)
    
    current_date += timedelta(days=1)

# Save the cleaned events to a JSON file
with open('cmu_calendar_events.json', 'w', encoding='utf-8') as f:
    json.dump(all_events, f, ensure_ascii=False, indent=2)

print(f"Scraped events from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")