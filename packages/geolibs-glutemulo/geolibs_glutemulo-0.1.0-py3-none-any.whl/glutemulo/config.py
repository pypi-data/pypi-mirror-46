from environs import Env
from marshmallow.validate import OneOf
import logging

env = Env()

with env.prefixed("GLUTEMULO_"):
    backend = env("BACKEND", default="carto")
    config = {
        "backend": backend,
        "debug": env.bool("DEBUG", False),
        "log_level": getattr(
            logging,
            env.str(
                "LOG_LEVEL",
                logging.INFO,
                validate=OneOf(
                    "DEBUG INFO WARN ERROR".split(),
                    error="LOG_LEVEL must be one of: {choices}",
                ),
            ),
        ),
    }

    with env.prefixed("INGESTOR_"):
        config.update(
            {
                "ingestor_topic": env("TOPIC", None),
                "ingestor_bootstap_servers": env.list("BOOTSTRAP_SERVERS"),
                "ingestor_group_id": env("GROUP_ID"),
                "ingestor_wait_interval": env("WAIT_INTERVAL", 0),
                "ingestor_auto_offset_reset": env("AUTO_OFFSET_RESET", "earliest"),
                "ingestor_max_poll_records": env.int("MAX_POLL_RECORDS", 500),
                "ingestor_fetch_min_bytes": env.int("FETCH_MIN_BYTES", 1000),
                "ingestor_table_ddl_content": env("TABLE_DLL_CONTENT", ""),
                "ingestor_dataset": env("DATASET", ""),
            }
        )
        with env.prefixed("DATASET_"):
            config.update(
                {
                    "ingestor_dataset_columns": env.list("COLUMNS", []),
                    "ingestor_dataset_ddl": env("DLL", ""),
                    "ingestor_dataset_autocreate": env.bool("AUTOCREATE", False),
                }
            )

    if backend == "carto":
        with env.prefixed("CARTO_"):
            config.update(
                {
                    "carto_user": env("USER"),
                    "carto_api_key": env("API_KEY"),
                    "carto_org": env("ORG"),
                }
            )
            api_url = env("API_URL", None)
            if not api_url:
                api_url = f"https://{env('USER')}.carto.com"
            config["carto_api_url"] = api_url
    elif backend == "postgres":
        with env.prefixed("PG_"):
            postgres_uri = env("URI", None)
            if not postgres_uri:
                config.update(
                    {
                        "pg_user": env("USER"),
                        "pg_password": env("PASSWORD"),
                        "pg_dbname": env("DBNAME"),
                        "pg_host": env("HOST"),
                        "pg_port": env("PORT"),
                    }
                )
                config[
                    "postgres_uri"
                ] = f'host={env("HOST")} port={env("PORT")} dbname={env("DBNAME")} user={env("USER")} password={env("PASSWORD")}'
