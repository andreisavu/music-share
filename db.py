
import web, settings

#
# Master read/write database
#
master = web.database(dbn = settings.DB_MASTER_TYPE,
	host = settings.DB_MASTER_HOST,
	db = settings.DB_MASTER_NAME,
	user = settings.DB_MASTER_USER,
	pw = settings.DB_MASTER_PASSW)

#
# Slave databases - multiple servers behind HA proxy
#
slave = web.database(dbn = settings.DB_SLAVE_TYPE,
	host = settings.DB_SLAVE_HOST,
	db = settings.DB_SLAVE_NAME,
	user = settings.DB_SLAVE_USER,
	pw = settings.DB_SLAVE_PASSW)

