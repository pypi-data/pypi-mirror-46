import json
from netapp_uom.client import NetApp_UOM_Client

UOM_HOST='10.0.1.21'
UOM_USER='admin'
UOM_PASS='g1zm08764'

# Create a new client connection
uom_client = NetApp_UOM_Client(UOM_HOST, UOM_USER, UOM_PASS, verify_ssl=False)

# Get a list of clusters and iterate
for cluster in uom_client.get_clusters():
  print('Cluster: {0}'.format(cluster.json['cluster']['label']))

  # Dump the raw JSON response
  print(cluster.json)

  # Dump attributes for the cluster
  for attr_key, attr_val in cluster:
    print('> {0}: {1}'.format(attr_key, attr_val))

# Get a list of volumes, filtered by cluster ID and SVM ID
# The filter only affects this query
filtered_volumes = uom_client.filter({
  'clusterId': '1',
  'svmId': '361'
}).get_volumes()

print(json.dumps(filtered_volumes.json, indent=2))

# Apply custom parameters when getting nodes
filtered_nodes = uom_client.get_nodes(params={
  'limit': 40,
  'clusterId': '1'
})

print(json.dumps(filtered_nodes.json, indent=2))
