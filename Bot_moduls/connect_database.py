from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from setting import (ASTRA_CLIENT_ID, ASTRA_CLIENT_SECRET,
                     PATH_SECURE_CONNECT_BUNDLE)

cloud_config= {
  'secure_connect_bundle': f'{PATH_SECURE_CONNECT_BUNDLE}'
}
auth_provider = PlainTextAuthProvider(f'{ASTRA_CLIENT_ID}', f'{ASTRA_CLIENT_SECRET}')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
  print(row[0])
else:
  print("An error occurred.")