{% set film_title = 'Dunkirk' %}

SELECT * FROM films
WHERE title = '{{ film_title }}'