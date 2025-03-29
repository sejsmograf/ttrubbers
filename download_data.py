import requests
import csv
from dataclasses import  asdict
from bs4 import BeautifulSoup
from rubber_data import RubberData



url = "https://revspin.net/top-rubber/overall-desc.html?p={}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}



def get_page_count():
    return 6 # hardcode for now


def has_class(element, classname: str):
    return element.has_attr("class") and classname in element["class"]


def get_rank(row) -> int:
    rank = row.find("td", class_="rank")
    return int(rank.text[:-2])


def get_name(row) -> str:
    return row.find("td", class_="product").text.strip()


def get_float_by_class(row, classname) -> float:
    return float(row.find("td", class_=classname).text)


def get_int_by_class(row, classname) -> int:
    return int(row.find("td", class_=classname).text)


def get_price(row) -> float:
    price_str = row.find("td", class_="price").text
    dollar_idx = price_str.find("$")
    price = float(price_str[dollar_idx + 1 :])
    return price


rubbers = []

for i in range(1, 1 + get_page_count()):
    print(f"Scraping {i} out of {get_page_count()} pages")
    response = requests.get(url.format(i), headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="top_product_list")
    rows = table.find_all("tr")

    for row in rows:
        if has_class(row, "head"):
            continue

        rank = get_rank(row)
        name = get_name(row)

        speed = get_float_by_class(row, "speed")
        spin = get_float_by_class(row, "spin")
        control = get_float_by_class(row, "control")
        tackiness = get_float_by_class(row, "tackiness")
        weight = get_float_by_class(row, "weight")
        hardness = get_float_by_class(row, "sponge_hardness")
        gears = get_float_by_class(row, "gears")
        throw_angle = get_float_by_class(row, "throw_angle")
        consistency = get_float_by_class(row, "consistency")
        durable = get_float_by_class(row, "durability")
        overall = get_float_by_class(row, "overall")
        ratings = get_int_by_class(row, "ratings")
        price = get_price(row)

        entry = RubberData(
            rank=rank,
            name=name,
            speed=speed,
            spin=spin,
            control=control,
            tackiness=tackiness,
            weight=weight,
            hardness=hardness,
            gears=gears,
            throw_angle=throw_angle,
            consistency=consistency,
            durable=durable,
            overall=overall,
            ratings=ratings,
            price=price,
        )

        rubbers.append(entry)


rubbers = [
    asdict(rubber) for rubber in rubbers
]

with open("rubbers.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=rubbers[0].keys())
    writer.writeheader()
    writer.writerows(rubbers)
