import multiprocessing
import numpy as np
from pymilvus import connections, utility, Collection, CollectionSchema, FieldSchema, DataType

milvus_instances = [
    {"alias": "instance1", "host": "localhost", "port": "19530"}
    # add other instances ex: {"alias": "instance2", "host": "192.168.2.6", "port": "19530"}
]
collection_name = "example_collection"
dim = 128  # Vector dimension


def setup_milvus(instance, result_list):
    print(f"Connecting to {instance['host']}:{instance['port']}...")

    # Explicitly reconnect in the child process
    connections.connect(alias=instance["alias"], host=instance["host"], port=instance["port"])

    # Create collection if not exists
    if collection_name not in utility.list_collections(using=instance["alias"]):
        print(f"Creating collection: {collection_name}")

        # Define schema
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim)
        ]
        schema = CollectionSchema(fields, description="Example collection")

        # Create collection
        collection = Collection(name=collection_name, schema=schema, using=instance["alias"])

        # Create an index for fast search
        index_params = {"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
        collection.create_index(field_name="vector", index_params=index_params)
    else:
        collection = Collection(name=collection_name, using=instance["alias"])

    # Insert 50 random vectors
    vectors = np.random.rand(50, dim).astype(np.float32)
    insert_result = collection.insert([vectors])

    # Load collection before querying
    collection.load()

    # Query with a random vector
    query_vector = np.random.rand(1, dim).astype(np.float32)
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    search_results = collection.search(query_vector, "vector", search_params, limit=5)

    # Convert search results to picklable format
    formatted_results = [
        {"id": hit.id, "distance": hit.distance} for hits in search_results for hit in hits
    ]

    # Store results in shared list
    result_list.append({instance["host"]: formatted_results})

    # Disconnect
    connections.disconnect(alias=instance["alias"])


if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        result_list = manager.list()  # Shared list for storing results
        processes = []

        for instance in milvus_instances:
            process = multiprocessing.Process(target=setup_milvus, args=(instance, result_list))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        # Print final results from all processes
        print("Final search results:", list(result_list))
