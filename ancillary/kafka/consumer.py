import time
import os
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List


class AncillaryService:
    redis = {}
    # data - 100 packets --> 1000 words => 100 * 1000 = 1 L --> 1 MB
    # 32000 --> 512 mb [X]
    # 32 GB || 64 GB
    # Master-Slave --> 2 GB container -- [16] primary [16] secondary --> 64 GB
    # Time
    # 1. Database - Mongo | Dynamo
    # 2. Time, Cost, Persistence, Sorting*
    executor = ThreadPoolExecutor()

    def set_data_in_redis(
        self,
        resource_id: int,
        packet_index: int,
        data: List,
    ):
        resource_id_dict = self.redis.get(resource_id)
        if resource_id_dict is not None:
            resource_id_dict[packet_index] = data
            self.redis[resource_id] = resource_id_dict
        else:
            self.redis[resource_id] = {packet_index: data}

    def get_all_data_from_redis(self, resource_id: int):
        return self.redis.get(resource_id)

    def invalidate_cache(self, resource_id: int):
        self.redis.pop(resource_id)

    @staticmethod
    def generate_array(payload: str):
        return [len(item) for item in payload.split(" ")]

    def process_packet_data(self, packet_data):
        print(f"PACKET: {packet_data}")
        payload = packet_data.get("payload")
        output = self.generate_array(payload=payload)
        resource_id = packet_data.get("resource_id")
        packet_index = packet_data.get("packet_index")
        self.set_data_in_redis(
            resource_id=resource_id,
            packet_index=packet_index,
            data=output,
        )
        # print(f"REDIS: {self.redis}")
        if packet_data.get("last_chunk_flag"):
            time.sleep(60)
            output = sorted(self.redis.get(resource_id).items())
            final_array = []
            for packet_index, packet_output in output:
                final_array.extend(packet_output)
            print(f"FINAL OUTPUT for {resource_id}: {final_array}")
            # Call Downstream Service
            downstream_service(
                resource_id=packet_data.get("resource_id"), data=final_array
            )
            self.invalidate_cache(resource_id=resource_id)
            # print(f"REDIS: {self.redis}")
            return final_array
        return "Waiting for rest of the data..."

    def process(self, packet_data: dict, test_call=False):

        if not test_call:
            # Validate Data
            from ancillary.serializers import PacketSerializer

            serializer = PacketSerializer(data=packet_data)
            serializer.is_valid(raise_exception=True)

        return self.executor.submit(self.process_packet_data, packet_data)


def downstream_service(resource_id: int, data: List[int]):
    os.makedirs('downstream_data', exist_ok=True)
    with open(file=f"downstream_data/{resource_id}.txt", mode="w+") as f:
        for item in data:
            f.write(f"{item}\n")
