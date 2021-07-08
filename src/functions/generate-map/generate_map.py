import datetime

import boto3
from jinja2 import Template


def lambda_handler(event, context):
    locations_to_plot = event["locations_to_plot"]
    s3_bucket = event["s3_bucket"]
    s3_folder = event["s3_folder"]
    identity_pool_id = event["identity_pool_id"]
    map_name = event["map_name"]

    html_map_template = """
  <!-- Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. -->
  <!-- SPDX-License-Identifier: MIT-0 -->
  <html>
    <head>
      <link
        href="https://api.mapbox.com/mapbox-gl-js/v1.12.0/mapbox-gl.css"
        rel="stylesheet"
      />
      <style>
        body {
          margin: 0;
        }

        #map {
          height: 100vh;
        }
      </style>
    </head>

    <body>
      <div id="map" />
      <script src="https://api.mapbox.com/mapbox-gl-js/v1.12.0/mapbox-gl.js"></script>
      <script src="https://sdk.amazonaws.com/js/aws-sdk-2.784.0.min.js"></script>
      <script src="https://unpkg.com/@aws-amplify/core@3.7.0/dist/aws-amplify-core.min.js"></script>
      <script>
        // use Signer from @aws-amplify/core
        const { Signer } = window.aws_amplify_core;

        // configuration
        // Cognito Identity Pool ID
        const identityPoolId = "{{ identity_pool_id }}";
        // Amazon Location Service Map Name
        const mapName = "{{ map_name }}";

        // extract the region from the Identity Pool ID
        AWS.config.region = identityPoolId.split(":")[0];

        // instantiate a credential provider
        const credentials = new AWS.CognitoIdentityCredentials({
          IdentityPoolId: identityPoolId,
        });

        /**
         * Sign requests made by Mapbox GL using AWS SigV4.
         */
        function transformRequest(url, resourceType) {
          if (resourceType === "Style" && !url.includes("://")) {
            // resolve to an AWS URL
            url = `https://maps.geo.${AWS.config.region}.amazonaws.com/maps/v0/maps/${url}/style-descriptor`;
          }

          if (url.includes("amazonaws.com")) {
            // only sign AWS requests (with the signature as part of the query string)
            return {
              url: Signer.signUrl(url, {
                access_key: credentials.accessKeyId,
                secret_key: credentials.secretAccessKey,
                session_token: credentials.sessionToken,
              }),
            };
          }

          // don't sign
          return { url };
        }

        /**
         * Initialize a map.
         */
        async function initializeMap() {
          // load credentials and set them up to refresh
          await credentials.getPromise();

          // actually initialize the map
          const map = new mapboxgl.Map({
            container: "map",
            //center: [-0.10456897366709263, 51.51757968001271], // initial map centerpoint
            //zoom: 8, // initial map zoom
            style: mapName,
            transformRequest,
          });

          {% for marker in markers %}
          {{ marker }}
          {% endfor %}

          map.addControl(new mapboxgl.NavigationControl(), "top-left");
        }

        initializeMap();
      </script>
    </body>
  </html>
  """

    template = Template(html_map_template)
    markers = []
    for location_to_plot in locations_to_plot:
        markers.append(
            """
          var marker = new mapboxgl.Marker()
                  .setLngLat({0})
                  .setPopup(new mapboxgl.Popup().setHTML("<h4>{1}</h4>"))
                  .addTo(map);
          //marker.togglePopup(); // toggle popup open or closed
          """.format(
                location_to_plot["coordinates"], location_to_plot["label"]
            ),
        )
    html_map = template.render(
        markers=markers, identity_pool_id=identity_pool_id, map_name=map_name
    )

    # Generate map and upload to S3
    filename_map = "map_{}.html".format(datetime.datetime.utcnow().isoformat())

    client = boto3.client("s3")
    response = client.put_object(
        Bucket=s3_bucket, Body=html_map, Key=s3_folder + filename_map
    )

    print(response)

    # Generate a presigned URL for the S3 object
    response = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": s3_bucket, "Key": s3_folder + filename_map},
        ExpiresIn=3600,
    )
    # The response contains the presigned URL
    print(response)

    return {"link_map": response}
