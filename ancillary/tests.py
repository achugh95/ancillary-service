from ancillary.kafka.consumer import AncillaryService


def run_test(test_data: list):
    for dp in test_data:
        output = AncillaryService().process(packet_data=dp, test_call=True)
        # print(f"Output Received: {output.result()}")  # Waits till the function completes
        # time.sleep(5)


def test_single_chunk_complete_data():
    test_data = [
        {
            "resource_id": 101,
            "payload": "Bat Ball",
            "packet_index": 1,
            "last_chunk_flag": True,
        },
    ]
    run_test(test_data=test_data)


def test_multiple_chunk_data_packets():
    test_data = [
        # Multiple chunk data packets
        {
            "resource_id": 100,
            "payload": "I like to play table tennis!",
            "packet_index": 2,
            "last_chunk_flag": True,
        },
        {
            "resource_id": 100,
            "payload": "Bat Ball",
            "packet_index": 1,
            "last_chunk_flag": False,
        },
    ]
    run_test(test_data=test_data)


def test_multiple_chunk_out_of_order_data():
    test_data = [
        # Multiple chunk data with out-of-order packets
        {
            "resource_id": 200,
            "payload": "I like to play table tennis!",
            "packet_index": 2,
            "last_chunk_flag": True,
        },
        {
            "resource_id": 200,
            "payload": "Bat Ball",
            "packet_index": 1,
            "last_chunk_flag": False,
        },
    ]
    run_test(test_data=test_data)


def test_incomplete_data():
    test_data = [
        # Incomplete Data
        {
            "resource_id": 102,
            "payload": "Bat Ball",
            "packet_index": 1,
            "last_chunk_flg": False,
        },
    ]
    run_test(test_data=test_data)


test_single_chunk_complete_data()
test_multiple_chunk_data_packets()
test_multiple_chunk_out_of_order_data()
test_incomplete_data()
