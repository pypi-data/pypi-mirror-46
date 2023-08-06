"""
Connect to ANTARES' Kafka cluster and read messages.

"""
from __future__ import print_function

import argparse
import json
import logging
import os
import sys
import zlib

import bson

import antares_client
from antares_client import Client


log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel("INFO")


def main():
    args = parse_args(sys.argv[1:])
    log.info("Opening connection to ANTARES Kafka...")
    with Client(**args) as client:
        for topic, alert in client.iter():
            if args.get("output_directory", False):
                directory = os.path.join(args["output_directory"], topic)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                alert_id = get_alert_id(alert)
                file_name = "{}.json".format(alert_id)
                file_path = os.path.join(directory, file_name)
                with open(file_path, "w") as f:
                    json.dump(alert, f, indent=4)
                log.info("Saved alert {}".format(file_path))
            else:
                log.info("Received alert on topic '{}'".format(topic))
        log.info("Closing connection...")


def setup_arg_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "--version", action="version", version=antares_client.__version__
    )
    parser.add_argument(
        "topics",
        type=lambda string: string.split(","),
        help="Name of Kafka topic to connect to."
        " You may supply multiple topic names"
        " separated by commas, without spaces.",
    )
    parser.add_argument("--host", type=str, help="Hostname of Kafka cluster.")
    parser.add_argument("--port", type=int, help="Port of Kafka cluster.")
    parser.add_argument("--api-key", type=str, help="ANTARES Kafka API Key.")
    parser.add_argument("--api-secret", type=str, help="ANTARES Kafka API Secret.")
    parser.add_argument(
        "--ssl-ca-location",
        type=str,
        help="Location of your ssl root CAs cert.pem file.",
    )
    parser.add_argument(
        "-g",
        "--group",
        type=str,
        help="Globally unique name of consumer group. Defaults to your hostname.",
    )
    parser.add_argument(
        "-d", "--output-directory", type=str, help="Directory to save Alerts in."
    )
    return parser


def parse_args(args):
    parser = setup_arg_parser()
    args = parser.parse_args(args)
    return vars(args)


def get_alert_id(alert):
    alert_id = alert["new_alert"].get("alert_id", None)
    if alert_id is None:
        alert_id = "{}-{}".format(
            alert["new_alert"]["survey"], alert["new_alert"]["original_id"]
        )
    return alert_id


def parse_antares_alert(payload):
    """
    Convert an ANTARES Alert message to a Python object.

    ANTARES Alerts are outputted in GZIP-compressed BSON format.

    :param payload: byte array of message
    :return: dict
    """
    try:
        return bson.loads(zlib.decompress(payload))
    except Exception:
        log.error("Failed to parse message:")
        log.error(payload)
        raise
