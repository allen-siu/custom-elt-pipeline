<h1> Bugs Encountered / Details Noticed </h1> 

<h3> - Airflow with dbt directories and paths </h3>

- When mounting files on the DockerOperator object, and due to using WSL, I must use the WSL paths to specify an accurate file path.
- For example, I must start the absolute path with `/mnt/c/{rest of path}` if the file path are in my C drive, and `/home/username/{rest of path}` if the file path is in my Ubuntu profile. 

<h3> - "destination_db"."public"."(table_name)" does not exist </h3>

- The ELT script extracts data from a source_db and writes to the destination_db.
- dbt was running before the script finished executing, so the tables did not exist at that time.
- To fix, inside of docker-compose.yaml the `'depends_on'` section can specify different conditions that must be met `e.g. 'service_started', 'service_healthy', 'service_completed_successfully'`.

<h3> - Jinja </h3>

- Concept similar to environment variables.
- Cannot be used exactly like a variable (e.g. A Jinja for a string still needs quotes around the variable name when being referenced).

<h3> - {{ ref(table_name) }} vs. table_name </h3>

- In this project, both are interchangeable due to not altering schema names.
- `ref()` references the full object name in the database (e.g. `'(db_name)'.'(schema_name)'.'(table_name)'`).

<h3> - cron </h3>

- In the Dockerfile we run the command `RUN echo "0 3 * * * python /app/elt_script.py" | crontab -` to run `elt_script.py` every day at `3 A.M.`.

<h3> - SQL Queries </h3>

- `INSERT` does not care the order you insert the data in. 

    `INSERT INTO table_name (c1, c2, c3) VALUES (c1v, c2v, c3v);`

    same as

    `INSERT INTO table_name (c2, c1, c3) VALUES (c2v, c1v, c3v);`
    
- Another one
