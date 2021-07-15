## Amazon Location Detect Addresses to Map

[![Publish Version](https://github.com/aws-samples/amazon-location-detected-addresses-to-map/workflows/Publish%20Version/badge.svg)](https://github.com/aws-samples/amazon-location-detected-addresses-to-map/actions)
[![Unit Tests](https://github.com/aws-samples/amazon-location-detected-addresses-to-map/workflows/Unit%20Tests/badge.svg)](https://github.com/aws-samples/amazon-location-detected-addresses-to-map/actions)


TODO: Fill this README out!

Be sure to:

* Change the title in this README
* Edit your repository description on GitHub

### Usage

#### Prerequisites

To deploy the solution, you will require an AWS account. If you don’t already have an AWS account,
create one at <https://aws.amazon.com> by following the on-screen instructions.
Your access to the AWS account must have IAM permissions to launch AWS CloudFormation templates that create IAM roles.

#### Deployment

The application is deployed as an [AWS CloudFormation](https://aws.amazon.com/cloudformation) template.

> **Note**
You are responsible for the cost of the AWS services used while running this sample deployment. There is no additional
cost for using this sample. For full details, see the pricing pages for each AWS service you will be using in this sample. Prices are subject to change.

1. Deploy the latest CloudFormation template by following the link below for your preferred AWS region:

|Region|Launch Template|
|------|---------------|
|**US East (N. Virginia)** (us-east-1) | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=location-to-map&templateURL=https://s3.amazonaws.com/solution-builders-us-east-1/amazon-location-detected-addresses-to-map/latest/main.template)|
|**US West (Oregon)** (us-west-2) | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=location-to-map&templateURL=https://s3.amazonaws.com/solution-builders-us-west-2/amazon-location-detected-addresses-to-map/latest/main.template)|
|**EU (Ireland)** (eu-west-1) | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=location-to-map&templateURL=https://s3.amazonaws.com/solution-builders-eu-west-1/amazon-location-detected-addresses-to-map/latest/main.template)|
|**EU (London)** (eu-west-2) | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=location-to-map&templateURL=https://s3.amazonaws.com/solution-builders-eu-west-2/amazon-location-detected-addresses-to-map/latest/main.template)|
|**EU (Frankfurt)** (eu-central-1) | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=location-to-map&templateURL=https://s3.amazonaws.com/solution-builders-eu-central-1/amazon-location-detected-addresses-to-map/latest/main.template)|
|**AP (Sydney)** (ap-southeast-2) | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=location-to-map&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/amazon-location-detected-addresses-to-map/latest/main.template)|

2. If prompted, login using your AWS account credentials.
1. You should see a screen titled "*Create Stack*" at the "*Specify template*" step. The fields specifying the CloudFormation
   template are pre-populated. Click the *Next* button at the bottom of the page.
1. On the "*Specify stack details*" screen you may customize the following parameters of the CloudFormation stack:

|Parameter label|Default|Description|
|---------------|-------|-----------|
|CreateMap|true|If True, this creates an Amazon Location Map.|
|MapName|ExampleMap01|Must be a unique map resource name. No spaces allowed. For example, ExampleMap.|
|MapPricingPla|RequestBasedUsage|Specifies the pricing plan for your map resource.|
|MapStyle|VectorEsriStreets|Specifies the map style selected from an available data providers.|
|ResourceTags|LocationDetectApp|Tag resources, which can help you identify and categorize them.|
|Environment|DEV|The type of environment to tag your infrastructure with.|

When completed, click *Next*
1. [Configure stack options](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-add-tags.html) if desired, then click *Next*.
1. On the review you screen, you must check the boxes for:
    * "*I acknowledge that AWS CloudFormation might create IAM resources*"
    * "*I acknowledge that AWS CloudFormation might create IAM resources with custom names*"
    * "*I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND*"

   These are required to allow CloudFormation to create a Role to grant access to the resources needed by the stack and name the resources in a dynamic way.
1. Click *Create Stack*
1. Wait for the CloudFormation stack to launch. Completion is indicated when the "Stack status" is "*CREATE_COMPLETE*".
    * You can monitor the stack creation progress in the "Events" tab.

### Clean up

To remove the stack:

1. Open the AWS CloudFormation Console.
1. Click the *location-to-map* project, right-click and select "*Delete Stack*".
1. Your stack will take some time to be deleted. You can track its progress in the "Events" tab.
1. When it is done, the status will change from "DELETE_IN_PROGRESS" to "DELETE_COMPLETE". It will then disappear from the list.
1. Locate the S3 bucket and delete it manually.

## Local Development
See [Local Development](docs/LOCAL_DEVELOPMENT.md) guide to get a copy of the project up and running on your local machine for development and testing purposes.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
