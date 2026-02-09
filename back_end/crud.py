from save import Work
import json
def save_results(db, results):
    for item in results:
        work = Work(
            title_text=item["title"]["text"],
            title_url=item["title"]["url"],
            author_text=item["author"]["text"],
            author_url=item["author"]["url"],
            tags=json.dumps(item["tags"], ensure_ascii=False)
        )

        db.add(work)

    db.commit()
