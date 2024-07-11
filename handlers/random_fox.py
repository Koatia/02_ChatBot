import requests


def fox():
    url = "https://randomfox.ca/floof/"
    res = requests.get(url)
    if res:
        data = res.json()
        print(data)
        image_url = data.get("image")
        return image_url


if __name__ == "__main__":
    print(fox())
