import os
import csv
import pytz
import bcrypt
import django
import datetime
from ast                   import literal_eval
from random                import randrange
from django.utils.timezone import make_aware

# 코드 순서를 지켜야합니다!
os.environ["TZ"] = "UTC"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'westock.settings')
django.setup()

from product.models import (
    MainCategory,
    SubCategory,
    Specific,
    Product,
    SizeType,
    ReleaseDate,
    Image,
    ImageType,
    ProductSize,
    Size,
)
from sale.models   import (
    Status,
    Ask,
    UserAsk,
    Bid,
    Order,
)
from user.models   import (
    User
)

def open_csv_file(filename = "stockx_products.csv", mode = 'r', encoding = 'utf-8'):
    csv_open = open(filename, mode, encoding = encoding)

    if mode == 'r':
        csv_reader = csv.reader(csv_open)
        return (csv_open, csv_reader,)

    csv_writer = csv.writer(csv_open)
    return (csv_open, csv_writer,)

def create_main_category(name = "sneakers"):
    main_category, _ = MainCategory.objects.get_or_create(name = name)
    return main_category

def create_sub_category(main_category, name = "air jordan"):
    sub_category, _ = SubCategory.objects.get_or_create(
        name          = name,
        main_category = main_category
    )
    return sub_category

def create_specific(sub_category, name):
    specific_model, _ = Specific.objects.get_or_create(
        name         = name.lower(),
        sub_category = sub_category
    )
    return specific_model

def create_image_type(name):
    image_type, _ = ImageType.objects.get_or_create(name = name)
    return image_type

def create_status(name):
    status, _ = Status.objects.get_or_create(name = name)
    return status

def create_size_type(name):
    size_type, _ = SizeType.objects.get_or_create(name = name.lower())
    return size_type

def create_image(product, image_type, url):
    image, _ = Image.objects.get_or_create(
        product    = product,
        image_type = image_type,
        url        = url
    )
    return image

def create_release_date(date):
    release_date, _ = ReleaseDate.objects.get_or_create(date = date)
    return release_date

def create_size(name):
    size, _ = Size.objects.get_or_create(name = name)
    return size

def create_sizes(unrefiend_sizes):
    sizes = []
    for unrefined_size in unrefiend_sizes:
        size_name = convert_size_to_number(unrefined_size)
        if not size_name or size_name == '0':
            continue 
        size = create_size(size_name)
        sizes.append(size)
    return sizes

def create_product(specific_model, size_type, release_date, name, ticker, style, colorway, retail_price, description):
    product, _ = Product.objects.get_or_create(
        name         = name,
        description  = description,
        style        = style,
        ticker       = ticker,
        retail_price = retail_price,
        colorway     = colorway,
        release_date = release_date,
        size_type    = size_type,
        category     = specific_model,
    )
    return product

def create_product_size(product, size):
    product_size, _ = ProductSize.objects.get_or_create(product = product, size = size)
    return product_size

def create_image(product, image_type, url):
    image, _ = Image.objects.get_or_create(
        product    = product,
        image_type = image_type,
        url        = url
    )
    return image

def create_user(pk, first_name, last_name, email, password):
    password_bcrypted = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return User.objects.create(
        pk         = pk,
        first_name = first_name,
        last_name  = last_name,
        email      = email,
        password   = password_bcrypted,
    )

def create_ask(price, status, expired_date, product_size, created_at):
    return Ask.objects.create(
        price        = price,
        status       = status,
        expired_date = expired_date,
        product_size = product_size,
        created_at   = created_at
    )

def create_bid(user, price, status, expired_date, product_size, created_at):
    return Bid.objects.create(
        user         = user,
        price        = price,
        status       = status,
        expired_date = expired_date,
        product_size = product_size,
        created_at   = created_at
    )

def create_order(date, bid, ask):
    order, _ = Order.objects.get_or_create(date = date, ask = ask, bid = bid)
    return order

def is_empty(inputs):
    for i in inputs:
        if not i:
            return True
    return False

def convert_size_to_number(unrefined_size):
    unrefined_size = unrefined_size.strip()
    if not unrefined_size:
        return None

    size = unrefined_size.split(' ')[1]
    if size[-1].isalpha():
        size = size[:-1]
    return size

def convert_date(unrefined_date):
    splits = unrefined_date.split('/')
    return splits[2] + '-' + splits[0] + '-' + splits[1]

def convert_price_str_to_int(price_str):
    return int(''.join(price_str.split(',')))

def convert_image_urls_to_string(image_urls):
    result = ""
    for idx, url in enumerate(image_urls):
        if idx != (len(image_urls) - 1):
            added_url = url + "|"
        else:
            added_url = url
        result += added_url
    return result

def convert_str_to_date(date_str):
    date_strs = date_str.split('-')
    year      = int(date_strs[0])
    month     = int(date_strs[1])
    day       = int(date_strs[2])
    hour      = randrange(24)
    minute    = randrange(60)
    second    = randrange(60)
    return datetime.datetime(year, month, day, hour, minute, second, 0, pytz.UTC)

def get_random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)

def get_average_price(prices):
    return int(sum(prices) // len(prices))

def get_volatility(mini, maxi):
    mid = (mini+maxi) / 2
    return ((maxi-mid)/mid) * 2

def get_price_primium(retail_price, average_price):
    return int((average_price - retail_price) / retail_price) * 100

def main():
    # csv 파일 리소스 오픈
    csv_open, csv_reader = open_csv_file()

    # product 앱에서 미리 만들어두어야 하는 것들
    main_category = create_main_category()
    sub_category  = create_sub_category(main_category)
    
    image_type_list   = create_image_type('list')
    image_type_detail = create_image_type('detail')

    # sale 앱에서 미리 만들어두어야 하는 것들
    status_done     = create_status(name = 'done')
    status_current  = create_status(name = 'current')
    status_pending  = create_status(name = 'pending')
    status_expired  = create_status(name = 'expired')
    status_canceled = create_status(name = 'canceled')

    # 가짜 판매자 & 구매자 생성
    seller = create_user(1, "Mr", "Seller", "seller@westock.com", "Helloworld!")
    buyer  = create_user(2, "Ms", "Buyer", "buyer@westock.com", "Helloworld!")
    # buyers = []
    # for i in range(2, 11):
    #     buyer = create_user(i, "Ms", f"Buyer-{i}", f"buyer-{i}@westock.com", "Helloworld!")
    #     buyers.append(buyer)

    # 12개월 날짜
    start_date = convert_str_to_date('2019-09-01')
    end_date   = convert_str_to_date('2020-09-01')

    for idx, row in enumerate(csv_reader):
        jordan_number          = row[0]
        size_type_name         = row[1]
        list_image_url         = row[2]
        name                   = row[3]
        ticker                 = row[4]
        style                  = row[5]
        colorway               = row[6]
        unrefined_retail_price = row[7]
        unrefined_release_date = row[8]
        description            = row[9]
        detail_image_urls      = literal_eval(row[10])
        unrefiend_sizes        = literal_eval(row[11])
        # orders            = literal_eval(row[12])
        # asks              = literal_eval(row[13])
        # bids              = literal_eval(row[14])

        # 데이터 깨진 로우는 저장하지 않고 버린다
        if is_empty([jordan_number, size_type_name, list_image_url, name, ticker, style, colorway, unrefined_retail_price, unrefined_release_date, detail_image_urls, unrefiend_sizes]):
            continue

        # 데이터 변환
        retail_price = convert_price_str_to_int(unrefined_retail_price)
        refined_date = convert_date(unrefined_release_date)

        # Product 인스턴스 생성
        specific_model = create_specific(sub_category, jordan_number)
        size_type      = create_size_type(size_type_name)
        release_date   = create_release_date(refined_date)
        sizes          = create_sizes(unrefiend_sizes)
        product        = create_product(specific_model, size_type, release_date, name, ticker, style, colorway, retail_price, description)

        # ProductSize - Product와 Size 연결
        product_sizes = []
        for size in sizes:
            product_size = create_product_size(product, size)
            product_sizes.append(product_size)

        # Browse 페이지용 이미지 URL
        create_image(product, image_type_list, list_image_url)

        # 상세 페이지용 이미지 URL
        detail_image_urls_string = convert_image_urls_to_string(detail_image_urls)
        create_image(product, image_type_detail, detail_image_urls_string)

        # Ask 생성
        asks              = []
        ask_prices        = []
        ask_expired_dates = []
        ask_product_sizes = []
        if not product_sizes:
            continue

        for i in range(20):
            product_size_index = randrange(len(product_sizes))
            product_size       = product_sizes[product_size_index]
            expired_date       = get_random_date(start_date, end_date)
            price              = randrange(200, 1000)
            created_at         = get_random_date(start_date, expired_date)
            ask                = create_ask(price, status_done, expired_date, product_size, created_at)
            UserAsk(ask = ask, user = seller).save()

            asks.append(ask)
            ask_prices.append(price)
            ask_expired_dates.append(expired_date)
            ask_product_sizes.append(product_size)

        # Bid 생성
        bids = []
        for k, ask in enumerate(asks):
            created_at = ask_expired_dates[k] - datetime.timedelta(days=1)
            bid = create_bid(buyer, ask_prices[k], status_done, ask_expired_dates[k], ask_product_sizes[k], created_at)
            bids.append(bid)

        # Order 생성
        for j, ask in enumerate(asks):
            date = ask_expired_dates[k] - datetime.timedelta(days=2)
            create_order(date, bids[j], asks[j])

        if idx == 500 or idx == 1000 or idx == 1500:
            print(f'[진행 상황] - {idx}개 입력 완료')

        # 평균가, Volatility, 가격 프리미엄 계산 후 product 업데이트
        average_price         = get_average_price(ask_prices)
        asks_queryset         = Ask.objects.filter(product_size=product_size, status=status_done).order_by('-expired_date')[:12]
        prices_for_volatility = []
        for ask_query in asks_queryset:
            prices_for_volatility.append(ask_query.price)
        volatility    = get_volatility(min(prices_for_volatility), max(prices_for_volatility))
        price_premium = get_price_primium(retail_price, average_price)

        product.average_price = average_price
        product.volatility    = volatility
        product.price_premium = price_premium
        product.save()
        
    # csv 파일 리소스 해제
    csv_open.close()

if __name__ == "__main__":
    print("데이터베이스에 입력을 시작해요. 시간이 오래걸리니 기다려주세요!")
    main()
    print("데이터베이스에 입력이 완료되었어요! 모든 테이블을 꼭 확인해주세요!")