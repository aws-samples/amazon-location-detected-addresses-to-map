import boto3


def lambda_handler(event, context):
    client = boto3.client("comprehend")

    response = client.detect_pii_entities(
        Text=event["text"],
        LanguageCode="en",  # 'en'|'es'|'fr'|'de'|'it'|'pt'|'ar'|'hi'|'ja'|'ko'|'zh'|'zh-TW'
    )

    print(response)

    addresses = [
        entity for entity in response["Entities"] if entity["Type"] == "ADDRESS"
    ]
    print(addresses)

    addresses_str = [
        event["text"][address["BeginOffset"] : address["EndOffset"]]
        for address in addresses
    ]
    print(addresses_str)

    return {
        "addresses": addresses_str,
        "s3_bucket": event["s3_bucket"],
        "s3_folder": event["s3_folder"],
        "identity_pool_id": event["identity_pool_id"],
        "map_name": event["map_name"],
    }
