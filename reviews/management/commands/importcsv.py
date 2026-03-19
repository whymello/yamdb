import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

DATA_DIR = Path("static/data")


class Command(BaseCommand):
    help = "Импорт данных из CSV файлов в базу данных"

    def handle(self, *args, **kwargs) -> None:
        self.import_users()
        self.import_category()
        self.import_genre()
        self.import_titles()
        self.import_genre_title()
        self.import_reviews()
        self.import_comments()

        self.stdout.write(msg=self.style.SUCCESS(text="Импорт завершён"))

    def import_users(self) -> None:
        with open(file=DATA_DIR / "users.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                User.objects.create(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                    role=row["role"],
                    bio=row["bio"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                )

    def import_category(self) -> None:
        with open(file=DATA_DIR / "category.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                Category.objects.create(
                    id=row["id"],
                    name=row["name"],
                    slug=row["slug"],
                )

    def import_genre(self) -> None:
        with open(file=DATA_DIR / "genre.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.create(
                    id=row["id"],
                    name=row["name"],
                    slug=row["slug"],
                )

    def import_titles(self) -> None:
        with open(file=DATA_DIR / "titles.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                category = Category.objects.get(id=row["category"])

                Title.objects.create(
                    id=row["id"],
                    name=row["name"],
                    year=row["year"],
                    category=category,
                )

    def import_genre_title(self) -> None:
        with open(file=DATA_DIR / "genre_title.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row["title_id"])
                genre = Genre.objects.get(id=row["genre_id"])
                title.genre.add(genre)

    def import_reviews(self) -> None:
        with open(file=DATA_DIR / "review.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row["title_id"])
                author = User.objects.get(id=row["author"])

                Review.objects.create(
                    id=row["id"],
                    title=title,
                    text=row["text"],
                    author=author,
                    score=row["score"],
                    pub_date=row["pub_date"],
                )

    def import_comments(self) -> None:
        with open(file=DATA_DIR / "comments.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                review = Review.objects.get(id=row["review_id"])
                author = User.objects.get(id=row["author"])

                Comment.objects.create(
                    id=row["id"],
                    review=review,
                    text=row["text"],
                    author=author,
                    pub_date=row["pub_date"],
                )
