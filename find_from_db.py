import docker
import re
import redis
import time

from models import Author, Quote
from connection import db, connect

import platform
is_windows = platform.system() == "Windows"

client = None
redis_client = None

if is_windows:
    
    client = docker.DockerClient(base_url='tcp://localhost:2375')
    client.containers.run(
        'redis:latest', name='my-redis-container', detach=True, ports={'6379/tcp': 6379})
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
else:
    def start_redis_container():
        client = docker.from_env()
        try:
            container = client.containers.get('my-redis-container')
            if container.status != 'running':
                container.start()
        except docker.errors.NotFound:
            client.containers.run(
                'redis:latest', name='my-redis-container', detach=True, ports={'6379/tcp': 6379})
            time.sleep(2)

    start_redis_container()
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def search_quotes_by_author(author_name):
    cached_result = redis_client.get(f"author:{author_name}")
    if cached_result:
        return cached_result.decode('utf-8')

    author = Author.objects(fullname=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        result = "\n".join(
            [f"Цитата: {quote.quote}\nАвтор: {quote.author.fullname}\nТеги: {', '.join(quote.tags)}" for quote in quotes])
        redis_client.setex(f"author:{author_name}", 3600, result)
        return result
    else:
        return "Автор не знайдений"


def search_quotes_by_tag(tag):
    cached_result = redis_client.get(f"tag:{tag}")
    if cached_result:
        return cached_result.decode('utf-8')

    quotes = Quote.objects(tags=tag)
    result = "\n".join(
        [f"Цитата: {quote.quote}\nАвтор: {quote.author.fullname}\nТеги: {', '.join(quote.tags)}" for quote in quotes])
    redis_client.setex(f"tag:{tag}", 3600, result)
    return result


def search_quotes_by_tags(tags):
    tags = tags.split(',')
    quotes = Quote.objects(tags__in=tags)
    return quotes


def main():
    while True:
        command = input("Введіть команду: ").strip()
        match = re.match(r"(name|tag):(.+)", command)

        if match:
            option, value = match.groups()
            if option == "name":
                result = search_quotes_by_author(value)
            elif option == "tag":
                result = search_quotes_by_tag(value)
            print(result)
        elif command == "exit":
            client.close()
            break
        else:
            print("Невідома команда")
            continue


if __name__ == "__main__":
    main()
