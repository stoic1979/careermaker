import requests
i = 10
url = "https://www.yelp.com/search?find_desc=Dry+Cleaners&find_loc=New+York%2C+NY&start=" + str(i)
while True:
    i = i + 10
    page = requests.get(url)
    if page.status_code != 200:
        break
    url = "https://www.yelp.com/search?find_desc=Dry+Cleaners&find_loc=New+York%2C+NY&start=" + str(i)
