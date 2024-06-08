Выполнил: Дарашкевич Евгений Михайлович, БПМИ216.

Выбранный вариант: Социальная сеть.

# User service

## Quick start

### How to launch services and databases

```
bash src/services/run.sh
```

### Test

#### Users service

You can find some examples of usage in `src/services/users/examples/` directory.

#### Posts service

You can find some examples of usage in `src/services/posts/examples/` directory.

### How to init clickhouse

Connect via `clickhouse-client` and execute code below:
```
CREATE TABLE post_views_kafka (
    post_id String,
    viewed_at DateTime,
    post_author_id String,
    event_author_id String
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:29092',
         kafka_topic_list = 'post_views',
         kafka_group_name = 'post_views_group',
         kafka_format = 'JSONEachRow';

CREATE TABLE post_likes_kafka (
    post_id String,
    liked_at DateTime,
    post_author_id String,
    event_author_id String
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:29092',
         kafka_topic_list = 'post_likes',
         kafka_group_name = 'post_likes_group',
         kafka_format = 'JSONEachRow';

CREATE TABLE post_views (
    post_id String,
    viewed_at DateTime,
    post_author_id String,
    event_author_id String
) ENGINE = MergeTree()
ORDER BY post_id;

CREATE TABLE post_likes (
    post_id String,
    liked_at DateTime,
    post_author_id String,
    event_author_id String
) ENGINE = MergeTree()
ORDER BY post_id;

CREATE MATERIALIZED VIEW post_views_mv TO post_views
AS SELECT 
    post_id, 
    viewed_at,
    post_author_id,
    event_author_id
FROM post_views_kafka;

CREATE MATERIALIZED VIEW post_likes_mv TO post_likes
AS SELECT 
    post_id, 
    liked_at,
     post_author_id,
    event_author_id
FROM post_likes_kafka;
```

Use this to check tables content:
```
SELECT * FROM post_views;
SELECT * FROM post_likes;
```
