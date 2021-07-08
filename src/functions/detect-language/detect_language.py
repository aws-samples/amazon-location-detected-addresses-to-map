import boto3


def lambda_handler(event, context):
    client = boto3.client("comprehend")

    text = event["text"]

    languages = client.detect_dominant_language(Text=text)
    print("Detected languages: ", languages)

    lang_code = languages["Languages"][0]["LanguageCode"]
    print("First language: ", lang_code)

    return {
        "lang_code": lang_code,
        "text": text,
        "s3_bucket": event["s3_bucket"],
        "s3_folder": event["s3_folder"],
        "identity_pool_id": event["identity_pool_id"],
        "map_name": event["map_name"],
    }
