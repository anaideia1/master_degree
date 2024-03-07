from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from alembic_utils.replaceable_entity import register_entities

from backend.session import Base


update_update_time_func = PGFunction(
    schema="public",
    signature="update_updated_at()",
    definition="""
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = (CURRENT_TIMESTAMP AT TIME ZONE 'UTC');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """,
)

register_entities([update_update_time_func])

update_time_triggers = [
    PGTrigger(
        schema="public",
        signature=f"update_{tb_name}_updated_at",
        on_entity=tb_name,
        definition=f"""
            BEFORE INSERT OR UPDATE ON {tb_name}
            FOR EACH ROW EXECUTE FUNCTION update_updated_at()
        """,
    )
    for tb_name, tb in Base.metadata.tables.items()
    if any(c.name == "updated_at" for c in tb.columns)
]

register_entities(update_time_triggers)
