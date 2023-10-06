from pathlib import Path
import json

from hw.database.connect import connect_db
from hw.database.models import Authors, Tag, Quotes


def load_json_files_from_dir(json_dir: Path) -> dict:
    result = {}
    if json_dir.exists():
        for file_item in json_dir.glob("*.json"):
            if file_item.is_file():
                with file_item.open("r", encoding="UTF-8") as fp:
                    result[file_item.stem] = json.load(fp)
    return result


def seeds(debug: bool = False):
    json_dir = Path(__file__).parent.joinpath("json")
    json_dict = load_json_files_from_dir(json_dir)

    if not json_dict:
        print("Files JSON not found")
        return 1

    authors_id = {}
    seed_object = "authors"
    if seed_object in json_dict:
        Authors.drop_collection()
        for author in json_dict.get(seed_object):
            rec = Authors(**author).save()
            authors_id[author.get("fullname")] = rec.id
            print(f"added {seed_object} id: {rec.id}")

    seed_object = "quotes"
    if seed_object in json_dict:
        Quotes.drop_collection()
        for quote in json_dict.get(seed_object):
            author = quote.get("author")
            author_id = authors_id.get(author)
            if author_id:
                quote["author"] = author_id
                rec = Quotes(**quote).save()
                print(f"added {seed_object} id: {rec.id}")

    if debug:
        authors = Authors.objects()
        for record in authors:
            print("-------------------")
            print(record.to_mongo().to_dict())

        quotes = Quotes.objects()
        for record in quotes:
            print("-------------------")
            print(record.to_mongo().to_dict())

            # tags = [tag.name for tag in note.tags]
            # print(f"id: {note.id} name: {note.name} date: {note.created} records: {records} tags: {tags}")

        find1 = Authors.objects(fullname="Steve Martin").delete()
        print("deleted", find1)

        find1 = Authors.objects()
        for record in find1:
            print("-------------------")
            print(record.to_mongo().to_dict())


# # спочатку - створити об'єкт Tag
# tag = Tag(name='Purchases')
# # потім - створення об'єктів Record
# record1 = Record(description='Buying sausage')
# record2 = Record(description='Buying milk')
# record3 = Record(description='Buying oil')
# #  Останнє - створюємо об'єкт Note і зберігаємо його
# Notes(name='Shopping', records=[record1, record2, record3], tags=[tag, ]).save()

# Notes(name='Going to the movies', records=[Record(description='Went to see the Avengers'), ], tags=[Tag(name='Fun'), ]).save()


if __name__ == "__main__":
    connect_db()
    seeds()
