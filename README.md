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
CREATE TABLE post_views (
    post_id String,
    viewed_at DateTime
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:29092',
         kafka_topic_list = 'post_views',
         kafka_group_name = 'post_views_group',
         kafka_format = 'JSONEachRow';

CREATE TABLE post_likes (
    post_id String,
    liked_at DateTime
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:29092',
         kafka_topic_list = 'post_likes',
         kafka_group_name = 'post_likes_group',
         kafka_format = 'JSONEachRow';

CREATE MATERIALIZED VIEW post_views_mv
ENGINE = MergeTree()
ORDER BY post_id
AS SELECT post_id, viewed_at
FROM post_views;

CREATE MATERIALIZED VIEW post_likes_mv
ENGINE = MergeTree()
ORDER BY post_id
AS SELECT post_id, liked_at
FROM post_likes;
```

Use this to check tables content:
```
SELECT * FROM post_views_mv;
SELECT * FROM post_likes_mv;
```
