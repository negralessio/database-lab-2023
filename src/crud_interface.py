import os
import json
import sqlite3

import src.constants as constants

from src.data_classes import Article, Headline, Author
from typing import List


def get_path_to_data(root_dir: str = './data') -> List[str]:
    """ Utility function that returns a list of file paths

    Recursively iterates over the data folder and adds files (+ its root) to the data list,
    which it also returns.

    :param root_dir: str -- Root directory
    :return: file_paths: List[str] -- List of file paths to the json files
    """
    file_paths: List = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_paths.append(os.path.join(root, file))

    return file_paths


def load_articles(root: str) -> List[Article]:
    """ Loads all JSON files as stores them in Article Objects and returns list of Articles

    Iterates through all the file paths to each JSON file and creates an Article Object
    with the corresponding variables.

    :param root: str -- Root directory
    :return: List[Article] -- List of Article Objects
    """
    # Get path to all JSON files
    data_paths: list = get_path_to_data(root_dir=root)

    articles: List[Article] = []
    for file_path in data_paths:
        with open(file_path) as json_file:
            # Load JSON file
            f = json.load(json_file)
            # Create Article Objects with that from json file / dict
            article = Article(**f)
            # Append Article Object to articles list
            articles.append(article)

    return articles


def make_dicts(articles):
    """ Utility function provided by supervisor to create dictionaries from List of Article DAO

    :param articles: List[Article]
    :return: article_dicts, authored_by_dicts, in_department_dicts, in_topic_dicts, has_breadcrumb_dicts
    """
    article_dicts = []
    authored_by_dicts = []
    in_department_dicts = []
    in_topic_dicts = []
    has_breadcrumb_dicts = []

    for article in articles:
        article_dicts.append({
            'id': article.id,
            'date_created': article.date_created.isoformat(),
            'date_published': article.date_published.isoformat(),
            'date_modified': article.date_modified.isoformat(),
            'channel': article.channel,
            'subchannel': article.subchannel,
            'comments_enabled': 1 if article.comments_enabled else 0,
            'headline_main': article.headline.main,
            'headline_social': article.headline.social,
            'intro': article.intro,
            'full_text': article.text,
            'url': article.url
        })

        for author in article.author.names:
            authored_by_dicts.append({'article_id': article.id, 'author_name': author})

        for department in article.author.departments:
            in_department_dicts.append({'article_id': article.id, 'department_name': department})

        for topic in article.topics:
            in_topic_dicts.append({'article_id': article.id, 'topic_name': topic})

        for breadcrumb in article.breadcrumbs:
            has_breadcrumb_dicts.append({'article_id': article.id, 'breadcrumb': breadcrumb})

    return article_dicts, authored_by_dicts, in_department_dicts, in_topic_dicts, has_breadcrumb_dicts


def create_database() -> None:
    """ Creates the article.db database according to the provided schema from exercise 01

    :return: None
    """
    with sqlite3.connect(constants.PATH_DB) as connection:
        cursor = connection.cursor()
        # Create article table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS article(
                    id TEXT NOT NULL,
                    date_created TEXT,
                    date_published TEXT,
                    date_modified TEXT,
                    channel TEXT,
                    subchannel TEXT,
                    comments_enabled INTEGER,
                    headline_main TEXT,
                    headline_social TEXT,
                    intro TEXT,
                    full_text TEXT,
                    url TEXT,
                    PRIMARY KEY(id))
        """)

        # Create authored_by table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS authored_by(
                    article_id TEXT NOT NULL,
                    author_name TEXT NOT NULL,
                    PRIMARY KEY(article_id, author_name)
                    FOREIGN KEY(article_id) REFERENCES article(id))
        """)

        # Create in_department table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS in_department(
                    article_id TEXT NOT NULL,
                    department_name TEXT NOT NULL,
                    PRIMARY KEY(article_id, department_name)
                    FOREIGN KEY(article_id) REFERENCES article(id))
        """)

        # Create in_topic table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS in_topic(
                    article_id TEXT NOT NULL,
                    topic_name TEXT NOT NULL,
                    PRIMARY KEY(article_id, topic_name)
                    FOREIGN KEY(article_id) REFERENCES article(id))
        """)

        # Create has_breadcrumb table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS has_breadcrumb(
                    article_id TEXT NOT NULL,
                    breadcrumb TEXT NOT NULL,
                    PRIMARY KEY(article_id, breadcrumb)
                    FOREIGN KEY(article_id) REFERENCES article(id))
        """)


def create(article: Article):
    """ Puts the given article: Article input in articles.db """
    assert isinstance(article, Article)

    # Cast to list and apply createMany operation
    article_list: list[Article] = [article]
    createMany(article_list)


def createMany(articles: List[Article]) -> None:
    """ Insert data into the article.db as seen in Exercise 01

    :param articles: List[Article] -- List of Article DAOs
    :return: None
    """
    with sqlite3.connect(constants.PATH_DB) as connection:
        article_dicts, authored_by_dicts, in_department_dicts, \
            in_topic_dicts, has_breadcrumb_dicts = make_dicts(articles)

        cursor = connection.cursor()
        # Insert article_dicts into article table
        cursor.executemany("""
            INSERT OR IGNORE INTO article VALUES
            (:id, :date_created, :date_published, :date_modified, :channel, :subchannel,
             :comments_enabled, :headline_main, :headline_social, :intro, :full_text, :url)
        """, article_dicts)

        # Insert authored_by_dicts into authored_by table
        cursor.executemany("""
            INSERT OR IGNORE INTO authored_by VALUES
            (:article_id, :author_name)
        """, authored_by_dicts)

        # Insert in_department_dicts into in_department table
        cursor.executemany("""
            INSERT OR IGNORE INTO in_department VALUES
            (:article_id, :department_name)
        """, in_department_dicts)

        # Insert in_topic_dicts in in_topic table
        cursor.executemany("""
            INSERT OR IGNORE INTO in_topic VALUES
            (:article_id, :topic_name)
        """, in_topic_dicts)

        # Insert has_breadcrumb_dicts in has_breadcrumb table
        cursor.executemany("""
            INSERT OR IGNORE INTO has_breadcrumb VALUES
            (:article_id, :breadcrumb)
        """, has_breadcrumb_dicts)


def read(article_id: str) -> Article:
    """ Collects data from the article with the specified ID by querying multiple tables and returns an init Article

    Applies queries on all tables to collect data about the article with the specified id.
    Then initializes and returns the corresponding Article object

    :param article_id: str -- Article to search for and get an initialized Article object
    :return: Article
    """
    with sqlite3.connect(constants.PATH_DB) as connection:
        # connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Get list of authors
        cursor.execute("SELECT author_name FROM authored_by WHERE article_id == (?)", [article_id])
        results_author_by = cursor.fetchall()
        author_names_list = [x[0] for x in results_author_by]

        # Get list of topics
        cursor.execute("SELECT topic_name FROM in_topic WHERE article_id == (?)", [article_id])
        results_in_topic = cursor.fetchall()
        topics_list = [x[0] for x in results_in_topic]

        # Get Dictionary of Article table
        cursor.execute("SELECT * FROM article WHERE id == (?)", [article_id])
        results_article = cursor.fetchone()
        try:
            rowDict = dict(zip([c[0] for c in cursor.description], results_article))
        except TypeError:
            print(f"Could not find an entry with the id: {article_id}")
            return None

        # Get list of departments
        cursor.execute("SELECT department_name FROM in_department WHERE article_id == (?)", [article_id])
        results_department = cursor.fetchall()
        departments_list = [x[0] for x in results_department]

        # Get list of breadcrumbs
        cursor.execute("SELECT breadcrumb FROM has_breadcrumb WHERE article_id == (?)", [article_id])
        results_breadcrumb = cursor.fetchall()
        breadcrumb_list = [x[0] for x in results_breadcrumb]

        # Get headline and author data
        headline = {
            "main": rowDict["headline_main"],
            "social": rowDict["headline_social"]
        }
        author = {
            "abbreviation": None,
            "departments": departments_list,
            "names": author_names_list
        }

        # Remove some entries that were encapsulated in their own dataclass
        rowDict.pop("headline_main")
        rowDict.pop("headline_social")
        rowDict["text"] = rowDict.pop("full_text")

        # Create article object with crawled data
        article = Article(**rowDict, author=author, headline=headline, breadcrumbs=breadcrumb_list, topics=topics_list)

        return article


def readMany(article_ids: List[str]) -> List[Article]:
    """ Reads and returns multiple Article objects

    :param article_ids: List[str] -- List of article_ids (strings) to read
    :return: List[Article] -- Corresponding initialized Article Objects
    """
    article_list: List[Article] = [read(article_id) for article_id in article_ids]
    return article_list


def delete(article: Article) -> bool:
    """ Deletes the article in the database """
    if article is None:
        return False
    else:
        # Cast to list and apply createMany operation
        article_list: list[Article] = [article]
        deleteMany(article_list)
        return True


def deleteMany(articles: List[Article]) -> None:
    """ Deletes the provided list of Articles from the database articles.db

    :param articles: List[Article]
    :return: None
    """
    with sqlite3.connect(constants.PATH_DB) as connection:
        article_dicts, authored_by_dicts, in_department_dicts, \
            in_topic_dicts, has_breadcrumb_dicts = make_dicts(articles)

        cursor = connection.cursor()
        cursor.executemany("DELETE FROM article WHERE id=:id", article_dicts)

        cursor.executemany("DELETE FROM authored_by WHERE article_id=:article_id and author_name=:author_name",
                           authored_by_dicts)

        cursor.executemany(
            "DELETE FROM in_department WHERE article_id=:article_id and department_name=:department_name",
            in_department_dicts)

        cursor.executemany("DELETE FROM in_topic WHERE article_id=:article_id and topic_name=:topic_name",
                           in_topic_dicts)

        cursor.executemany("DELETE FROM has_breadcrumb WHERE article_id=:article_id and breadcrumb=:breadcrumb",
                           has_breadcrumb_dicts)
