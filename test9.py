import requests
proxies = { "http": "http://159.203.87.130:3128", "https": "http://159.203.87.130:3128", }
page =requests.get("https://www.google.com/search?sxsrf=ACYBGNQijJp1zP8DrIYLxxx7uIToLlL4mw%3A1574336804346&ei=JHnWXdDgFOPFmAWp9rW4DA&q=python+requests+proxy&oq=python+requests+pro&gs_l=psy-ab.3.0.0j0i203l4j0j0i203j0j0i203j0.699.1661..3205...0.2..0.940.2238.3-1j1j1j1......0....1..gws-wiz.......0i71j35i39j0i67.YEgpl36LGxI")
