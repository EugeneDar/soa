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

