-- select_related - used for 1:1 many:one - inner join ForeignKey, OneToOneField
SELECT
    "snippet"."id",
    ...
FROM "snippet"
INNER JOIN "auth_user" ON (
    "snippet"."user_id" = "auth_user"."id"
    )

-- prefetch_related - ManyToManyField, ForeignKey(related_name) many:many , обратная связь
SELECT * FROM "snippet";

SELECT * FROM "comment"
WHERE "comment"."snippet_id" IN (1, 2, 3, ...); -- Здесь будут ID всех сниппетов из первого запроса