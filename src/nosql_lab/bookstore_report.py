#!/usr/bin/env python3

"""Print a report of authors and their books from MongoDB Atlas."""

import logging
import os

import pymongo


MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")


def main():
    """Connect to MongoDB Atlas and print books for selected authors."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    client = None

    try:
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD
        )

        logging.info("Connected to MongoDB Atlas.")

        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        author_ids = [
            "author_001",
            "author_002",
            "author_004"
        ]

        author_count = authors.count_documents(
            {"_id": {"$in": author_ids}}
        )

        print(f"Authors: {author_count}")
        print()

        for author in authors.find({"_id": {"$in": author_ids}}):
            print(author["name"])

            author_books = books.find(
                {"author_ids": author["_id"]}
            )

            for book in author_books:
                print(
                    f"  {book['title']} ({book['published_year']})"
                )

            print()

    except Exception as error:
        logging.error("MongoDB operation failed: %s", error)

    finally:
        if client is not None:
            client.close()
            logging.info("MongoDB connection closed.")


if __name__ == "__main__":
    main()
