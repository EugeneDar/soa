GET_TOTAL_VIEWS_AND_LIKES_TEMPLATE = """
    SELECT
        (
            SELECT 
                COUNT(DISTINCT event_author) AS unique_authors_count
            FROM post_views
            WHERE post_id = '{post_id}'
        ) AS likes_count,
        (
            SELECT 
                COUNT(DISTINCT event_author) AS unique_authors_count
            FROM post_likes
            WHERE post_id = '{post_id}'
        ) AS views_count
"""


GET_TOP_POSTS_TEMPLATE = """
    SELECT
        post_id,
        COUNT(DISTINCT event_author) AS unique_authors_count
    FROM
        {table_name}
    GROUP BY
        post_id
    ORDER BY
        unique_authors_count DESC
    LIMIT 5
"""

