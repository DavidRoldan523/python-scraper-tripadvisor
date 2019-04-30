from json import dump
from selenium import webdriver
from time import sleep

def get_all_reviews(hotel, language):
    review_total_pages = []
    ##Chrome
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get(hotel)
    sleep(2)
    driver.execute_script("document.querySelector('.hotels-review-list-parts-LanguageFilter__taLnk--3iBfk').click();")
    sleep(2)
    driver.execute_script(f"document.querySelector('input[value={language}]').click()")
    sleep(1)
    language_id = driver.find_element_by_xpath(f'//input[@value="{language}"]').get_attribute('id')

    hotel_name = driver.find_element_by_xpath('//h1[@id="HEADING"]').text
    total_reviews = driver.find_element_by_xpath(f'//label[@for="{language_id}"]/span[@class="hotels-review-list-parts-LanguageFilter__paren_count--EHwQo"]').text
    print(total_reviews)
    hotel_rating = driver.find_element_by_class_name('hotels-hotel-review-about-with-photos-Reviews__overallRating--vElGA').text
    stop_loop_for = int(int(total_reviews.replace('.', '').replace('(', '').replace(')', '')) / 5)

    if stop_loop_for % 2 == 0:
        stop_loop_for += 1
    else:
        stop_loop_for += 2
    click_stop = (stop_loop_for - 2) * 5

    print(f"Stop Loop {stop_loop_for}")

    print(f"Click Stop {click_stop}")

    url_extrac_http = hotel.replace('https://www.tripadvisor.co', '')
    url_partido = url_extrac_http.split('-Reviews-')

    #Cuerpo JSON
    for i in range(1, 3):
        print(f"Reviews Page: {i}")
        if i == 1:
            driver.execute_script("document.querySelector('.hotels-review-list-parts-ExpandableReview__cta--3U9OU').click();")
            sleep(2)
        else:
            sleep(2)
            click = (i - 1) * 5
            href = url_partido[0] + '-Reviews-or' + str(click) + '-' + url_partido[1]
            driver.execute_script(f"""document.querySelector('a[href="{href}"]').click();""")
            sleep(2)
            driver.execute_script("document.querySelector('.hotels-review-list-parts-ExpandableReview__cta--3U9OU').click();")
            sleep(2)

        reviews = driver.find_elements_by_xpath('//div[@class=""]/div/div[@class="hotels-hotel-review-community-content-Card__ui_card--3kTH_ hotels-hotel-review-community-content-Card__card--1MJgB hotels-hotel-review-community-content-Card__section--28b0a"]')
        reviews_body_list = [x for x in reviews[0].find_elements_by_xpath('//q[@class="hotels-review-list-parts-ExpandableReview__reviewText--3oMkH"]')]

        for review in reviews_body_list:
            review_dict = {
                'review_text': review.text,
                'review_posted_date': "XXXXX",
                'review_header': "XXXXXX",
                'review_rating': "XXXXX",
                'review_author': "XXXXX"
            }
            review_total_pages.append(review_dict)

    driver.quit()
    data = {
        'hotel_name': hotel_name,
        'total_reviews': total_reviews,
        'ratings': hotel_rating,
        'reviews': review_total_pages,
    }
    return data

def core():
    hoteles = ['https://www.tripadvisor.co/Hotel_Review-g150807-d152886-Reviews-The_Ritz_Carlton_Cancun-Cancun_Yucatan_Peninsula.html']
    language = 'pt'
    for hotel in hoteles:
        print(f"IN PROCESS FOR: {hotel}")
        temp = get_all_reviews(hotel, language)
        file = open('PruebaHotel.json', 'w', encoding='utf8')
        dump(temp, file, indent=4, ensure_ascii=False)
        file.close()

if __name__ == '__main__':
    core()