""" Very basic implementation for sql model migration """
import logging
import pyramid_sqla
from sqlalchemy.engine import reflection

from memphis import config


@config.subscriber(config.AppStarting)
def inspect(ev):
    engine = pyramid_sqla.get_engine()
    insp = reflection.Inspector.from_engine(engine)

    log = logging.getLogger('ptah-sql-migration')

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
        log.warning("Adding column '%s' to table '%s'", cl.name, cl.table.name)
        cl.create(cl.table, populate_default=True)
