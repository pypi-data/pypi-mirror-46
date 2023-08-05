from etl.monitor import logger

CURR_FILE = "[PROCEDURE]"


def create_type_notification(db, name):
    """
    Creates a notification with a payload and sends it to channel 'purr'.

    Parameters
    ----------
    Returns
    -------
    Example
    -------
    create_notification(db)
    """
    cmd = """CREATE OR REPLACE FUNCTION %s()
    RETURNS TRIGGER AS $$
    BEGIN
        PERFORM pg_notify('purr', 'type_change');
        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    """ % name

    try:
        logger.info("Creating procedure: %s" % name, CURR_FILE)
        db.execute_cmd(cmd)

    except Exception as ex:
        logger.error("Insert failed: %s" % ex, CURR_FILE)


def drop_type_notification(db, name):
    """
    Drops a notification with a payload and sends it to channel 'purr'.

    Parameters
    ----------
    Returns
    -------
    Example
    -------
    drop_notification(db)
    """
    cmd = "DROP FUNCTION IF EXISTS %s();" % name

    try:
        db.execute_cmd(cmd)
        logger.info("Dropping procedure: %s" % name, CURR_FILE)
    except Exception as ex:
        logger.error("Dropping procedure failed: %s" % ex, CURR_FILE)
