"""
Module that stores the example queries from Exercise 02
"""

QUERY1 =    """
            SELECT topic_name, count(topic_name)
            FROM (article JOIN in_topic
                ON article.id == in_topic.article_id)
            WHERE article.comments_enabled == 0
            GROUP BY topic_name
            ORDER BY count(topic_name) DESC
            """

QUERY2 =    """
            SELECT article.id, LENGTH(article.full_text) as length
            FROM article
            WHERE article.headline_main NOT LIKE '%News%'
                AND article.headline_main NOT LIKE '%Update%'
            ORDER BY length DESC
            """

QUERY3 =    """
            SELECT DATE(article.date_published), count(article.date_published)
            FROM article
            GROUP BY DATE(article.date_published)
            ORDER BY count(article.date_published) DESC
            """


QUERY4 =    """
            SELECT STRFTIME("%m-%Y", article.date_published) as Month,
                count(article.date_published)
            FROM article
            GROUP BY STRFTIME("%m-%Y", article.date_published)
            ORDER BY count(article.date_published) DESC
            """


QUERY5 =    """
            SELECT DATE(article.date_published), article.channel, count(article.channel)
            FROM article
            GROUP BY article.channel, DATE(article.date_published)
            ORDER BY count(article.channel) DESC
            """


QUERY6 =    """
            SELECT temp.department_name, temp.author_name, MAX(temp.num)

            FROM
                (SELECT department_name, author_name, COUNT(author_name) as num
                FROM (article JOIN in_department ON article.id == in_department.article_id)
                    JOIN authored_by ON id == authored_by.article_id
                GROUP BY department_name, author_name) as temp

            GROUP BY temp.department_name
            ORDER BY MAX(temp.num) DESC
            """


QUERY7 =    """
            SELECT article.id, article.headline_main, article_cnt.authored_by_n
            FROM
                (SELECT authored_by.article_id, count(authored_by.article_id) as authored_by_n
                FROM authored_by
                GROUP BY authored_by.article_id) as article_cnt
            JOIN article on article.id == article_cnt.article_id
            ORDER BY authored_by_n DESC
            """


QUERY8 =    """
            WITH split(id, token, str) AS (
                SELECT id, '', full_text||' ' FROM (SELECT * FROM article LIMIT 1)
                UNION ALL SELECT id,
                substr(str, 0, instr(str, ' ')),
                substr(str, instr(str, ' ')+1)
                FROM split WHERE str !=''
            ) SELECT id, token, ROW_NUMBER() OVER(ORDER BY id)-1 AS token_position FROM split WHERE token!=''
            """

# Store them in list for importing
QUERIES_LIST = [QUERY1, QUERY2, QUERY3, QUERY4, QUERY5, QUERY6, QUERY7, QUERY8]
