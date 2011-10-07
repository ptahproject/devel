from sqlalchemy.engine import reflection

import pyramid_sqla
from memphis import config


@config.subscriber(config.SettingsInitialized)
def inspect(ev):
    engine = pyramid_sqla.get_engine()

    insp = reflection.Inspector.from_engine(engine)

    missing = []
    md = pyramid_sqla.get_base().metadata
    for name, table in md.tables.items():
        names = [rec['name'] for rec in insp.get_columns(name)]

        for cl in table.columns:
            if cl.name not in names:
                missing.append(cl)

    if missing:
        import migrate.changeset

    for cl in missing:
        cl.create(cl.table, populate_default=True)
