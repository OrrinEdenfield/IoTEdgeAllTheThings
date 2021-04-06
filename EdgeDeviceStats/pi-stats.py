# For Raspberry Pi running Ubuntu, install pyodbc with pip (python3 -m pip install pyodbc) & configure FreeTDS
# For Raspberry Pi running Raspbian, install via: 
#   sudo apt install python-pyodbc python-sqlalchemy freetds-dev freetds-bin unixodbc-dev tdsodbc
# To configure FreeTDS:
#   Edit /etc/odbcinst.ini (get copy from iotpi4ubuntu but remember the driver files may be in a different location)
#    Should look like this for Raspbian
#      [FreeTDS]
#       Description=TDS driver (Sybase/MS SQL)
#       Driver=/usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so
#       Setup=/usr/lib/arm-linux-gnueabihf/odbc/libtdsS.so
#       CPTimeout=
#       CPReuse=
#       UsageCount=2
#
#   Should look like this for Ubuntu
#       [FreeTDS]
#       Description=TDS driver (Sybase/MS SQL)
#       Driver=libtdsodbc.so
#       Setup=libtdsS.so
#       CPTimeout=
#       CPReuse=
#       UsageCount=2

#   Lastly run the python3 install (python3 -m pip install pyodbc)


from linux_metrics import cpu_stat, mem_stat
import pyodbc
import datetime

# Set value of this device
thisdevice = '[DEVICE NAME]'

# Set database connection
cnxn = pyodbc.connect('DRIVER=FreeTDS;SERVER=[HOSTNAME];PORT=1433;DATABASE=[DATABASENAME];UID=[USERNAME];PWD=[PASSWORD];TDS_Version=8.0;')
cursor = cnxn.cursor()

# Set current timestamp
current_timestamp = datetime.datetime.now()

# Get system stats
used_cpu_pct = (100 - cpu_stat.cpu_percents(1)['idle'])
used_mem_pct = ((mem_stat.mem_stats()[0] / mem_stat.mem_stats()[1]) * 100)


# Insert to database
count = cursor.execute("""
SET NOCOUNT ON;
insert into dbo.EdgeDeviceStats ([Timestamp], [DeviceName], [UsedCpuPct], [UsedMemPct])
VALUES (?,?,?,?);""",
current_timestamp, thisdevice, used_cpu_pct, used_mem_pct).rowcount
cnxn.commit()
print(count)
