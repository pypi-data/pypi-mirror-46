import zmqflp_managed_client
import zmqflp_server
import time
from multiprocessing import Process
import socket
import asyncio
import logging
import cbor2

LEN_TEST_MESSAGE = 100
log_handlers = [logging.StreamHandler()]
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=log_handlers,
    level=logging.DEBUG)


def server_main():
    asyncio.run(server_loop())
    return 0


async def server_loop():
    server = zmqflp_server.ZMQFLPServer(str_port='9001')
    keep_running = True
    while keep_running:
        # handle the "TEST" requests
        (str_request, orig_headers) = await server.receive()
        req_object = cbor2.loads(str_request)
        if req_object != "EXIT":
            await server.send(orig_headers, req_object)
        elif req_object == "EXIT":
            logging.info('server exiting...')
            await server.send(orig_headers, "EXITING")
            keep_running = False
    if keep_running is False:
        return


def run_test(num_of_tests):
    for i in range(num_of_tests):
        with zmqflp_managed_client.ZMQFLPManagedClient([socket.gethostbyname(socket.gethostname()) + ':9001']) as client:
            test_message = ["TEST" for i in range(LEN_TEST_MESSAGE)]
            # logging.info('hi!')
            reply = client.send_and_receive(cbor2.dumps(test_message))  # , use_bin_type=True))
            # logging.info(reply)
            # logging.debug('reply: '+str(reply))
            if (len(reply) != LEN_TEST_MESSAGE) and (reply[-1] != "TEST"):  # "TEST_OK":
                logging.debug("TEST_FAILURE")
                raise ValueError()
    logging.debug("ending client send")
    return


def main():
    requests = 30
    server_process = Process(target=server_main, daemon=True)
    server_process.start()
    time.sleep(0.5)
    # client_process = Process(target=client_main, args=(requests,))
    # client = zmqflp_client.ZMQFLPClient([socket.gethostbyname(socket.gethostname()) + ':9001'])

    logging.debug(">> starting zmq freelance protocol test!")
    start = time.time()
    run_test(requests)
    # client_process.start()
    # client_process.join()
    avg_time = ((time.time() - start) / requests)
    logging.debug(">> waiting for server to exit...")
    server_process.join(timeout=1)
    logging.debug("Average RT time (sec): " + str(avg_time))
    return


if __name__ == '__main__':
    main()
