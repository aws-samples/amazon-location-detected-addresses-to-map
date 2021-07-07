import uuid
from difflib import SequenceMatcher

import boto3


def lambda_handler(event, context):
    client = boto3.client("location")

    addresses_str = event["addresses"]

    """
    response = client.list_place_indexes(
        MaxResults=10,
        #NextToken='string'
    )
    print(response)
    """

    index_name = "index_{}".format(uuid.uuid4())
    print(index_name)

    response = client.create_place_index(
        DataSource="Esri",  # 'Here' | 'Esri'
        DataSourceConfiguration={"IntendedUse": "SingleUse"},  # 'SingleUse' | 'Storage'
        Description="Created by Matteo's script",
        IndexName=index_name,
        # 'RequestBasedUsage' | 'MobileAssetTracking' | 'MobileAssetManagement'
        PricingPlan="RequestBasedUsage",
    )
    # print(response)
    print(
        "CREATE - {} HTTPStatusCode: {}".format(
            response["IndexName"], response["ResponseMetadata"]["HTTPStatusCode"]
        )
    )

    locations_to_plot = []

    for idx, address_str in enumerate(addresses_str):
        response = client.search_place_index_for_text(
            # BiasPosition=[123.0,],
            # FilterBBox=[123.0,],
            # FilterCountries=['string',],
            IndexName=index_name,
            # MaxResults=123,
            Text=address_str,
        )
        print("{}) {}".format(idx, address_str))
        # print(response['Results'])

        # for place in response['Results']:
        #    print("- {} -  {}".format(place['Place']['Label'], place['Place']['Geometry']['Point']))

        similarities = [
            SequenceMatcher(None, address_str, x["Place"]["Label"]).ratio()
            for x in response["Results"]
        ]
        index_most_similar = similarities.index(max(similarities))
        print(similarities, index_most_similar)
        place_most_similar = response["Results"][index_most_similar]["Place"]

        # print(place_most_similar)
        locations_to_plot.append(
            {
                "label": place_most_similar["Label"],
                "coordinates": place_most_similar["Geometry"]["Point"],
            }
        )
        print(locations_to_plot[-1])

    response = client.delete_place_index(IndexName=index_name)
    # print(response)
    print(
        "DELETE - {} HTTPStatusCode: {}".format(
            index_name, response["ResponseMetadata"]["HTTPStatusCode"]
        )
    )

    return {
        "locations_to_plot": locations_to_plot,
        "s3_bucket": event["s3_bucket"],
        "s3_folder": event["s3_folder"],
        "identity_pool_id": event["identity_pool_id"],
        "map_name": event["map_name"],
    }
