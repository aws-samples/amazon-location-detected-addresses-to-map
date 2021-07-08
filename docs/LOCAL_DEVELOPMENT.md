## Local Development

### Pre-Requisites

The following dependencies must be installed:
- Python >=3.8 and pip
- VirtualEnv
- NodeJs
- Go
- Ruby >=2.6 and gem
- [cfn-nag](https://github.com/stelligent/cfn_nag)

Here is a code to install pre-requisites on macOS using [Homebrew](https://brew.sh/). For other operating systems,
please refer to the OS documentation.
```shell
# install python3
brew install python

# install VirtualEnv
pip3 install virtualenv

# install NodeJS
brew install node

# install go
brew install go

# install cfn-nag
brew install ruby brew-gem
brew gem install cfn-nag
```

### Build local development environment

Once you have installed pre-requisites, run commands below:

#### Step 1 - `make init` (Required)
In the first step, you will create your repository and create a virtual environment.

1. Clone the repository.
   ```shell
   git clone <git-repository-clone-address>
   ```
1. Initialize the local environment
   ```shell
   make init
   ```
1. Activate `VirtualEnv` environment.
   ```shell
   source venv/bin/activate
   ```
1. Run pre-commit tests for the first time to check the installation.
   ```shell
   make test
   ```

#### Step 2 - `make config` (Required)
In the second step you will create configuration file for your deployment. The command will generate unique bucket name,
set the stack name, and you will be asked for AWS Region, where you want to deploy the solution too.

1. Run configuration command
   ```shell
   make config
   ```
1. Set AWS Region, for example us-east-1
   ```shell
   AWS Region to create bucket in(e.g. us-east-1)?: us-east-1
   ```
1. This will create and populate `config.mk` file
   ```shell
   AWS_REGION=eu-west-1
   BUCKET_NAME=saes-cookie-cutter-xxxxxxxxxxxxxxx
   STACK_NAME=saes-cookie-cutter
   ```
> Note: You can change those values manually in the `config.mk` file. You can change any variables generated and
> replace with own values. Also, here is the good place to add your template overrides. See the section Overriding
> default parameters.

#### Step 3 - `make bucket` (Optional)
In this step, you can create S3 bucket where you will store all your assets, such as CloudFormation templates, Lambda
functions and any other project related stuff. This step is optional as you may already have a bucket for development.
If that's the case, make sure you configure `config.mk` file accordingly.

1. Create bucket
   ```shell
   make bucket
   ```

#### Step 4 - `make deploy`
In the last step, you will deploy your infrastructure with CloudFormation. The `make deploy` command will **build** your libraries,
**package** the templates and lambda functions and **deploy** it in your AWS account.

1. Deploy CloudFormation
   ```shell
   make deploy
   ```
