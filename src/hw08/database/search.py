import redis
from redis_lru import RedisLRU

from hw08.database.models import Authors, Quotes


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)
print("REDIS:", client)



@cache
def find_by_name(name:str) -> list:
    result = []
    author = Authors.objects(fullname__iregex=name).first()
    if author:
        author_fullname = author.fullname
        author_id = author.id
        records = Quotes.objects(author=author_id)
        for record in records:
            r_dict = record.to_mongo().to_dict()
            author_fullname = record.author.fullname
            if author_fullname:
                r_dict["author"] = author_fullname
            del(r_dict["_id"])
            result.append(r_dict)
    return result

@cache
def find_by_tag(tag:str) -> list:
    result = []
    if tag:
        records = Quotes.objects(tags__iregex=tag)
        for record in records:
            r_dict = record.to_mongo().to_dict()
            author_fullname = record.author.fullname
            if author_fullname:
                r_dict["author"] = author_fullname
            del(r_dict["_id"])
            result.append(r_dict)
    return result

if __name__ == "__main__":
    from hw08.database.connect import connect_db

    if connect_db():
        find_by_name("eins")
        find_by_tag("live")
