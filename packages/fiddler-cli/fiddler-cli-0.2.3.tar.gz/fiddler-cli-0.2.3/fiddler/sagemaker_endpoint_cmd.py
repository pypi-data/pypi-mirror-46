
import boto3
from botocore.exceptions import ClientError, WaiterError
from fiddler.cli_utils import require_arg
import logging

DEFAULT_IMAGE = (
    '079310353266.dkr.ecr.us-west-1.amazonaws.com/sagemaker_fiddler:latest')

default_container = {
    'proxy': DEFAULT_IMAGE,
    'tensorflow': DEFAULT_IMAGE
}

LOG = logging.getLogger(__name__)


def add_sagemaker_endpoint_arguments(sub_parser):
    """ Adds arguments required for sagemaker_endpoint sub command. """
    parser = sub_parser  # rename

    parser.add_argument('--endpoint-type', choices=['proxy', 'tensorflow'],
                        default='proxy', required=True, help=(
        'The type of model the endpoint infers from. Default is `proxy`. '
        'A proxy endpoint forwards the incoming requests to another endpoint '
        'for inferences. It logs the inference events for monitoring and '
        'analytics. The other supported is `tensorflow`. It '
        'loads TensorFlow model and serves it just like a normal SageMaker '
        'instance would. It logs the inference events as well for monitoring '
        'and analytics. Event logging is optional and can be disabled.'))
    parser.add_argument('--endpoint-name', required=True, help=(
        'Name of the endpoint. An endpoint requires creating a Sagemaker '
        'model and endpoint configuration before creating the the endpoint. '
        'This name is used for all three: Sagemaker model, endpoint '
        'configuration, and the endpoint'))
    parser.add_argument('--execution-role-arn', required=True, help=(
        'Execution ARN to run the model. E.g. `arn:aws:iam::012345678912:role'
        '/service-role/Sage`. See IAM --> Roles under AWS console.'))
    parser.add_argument('--endpoint-region', help=(
        'Region where the endpoint should be located. The default is same '
        'as default region for AWS cli commands.'))
    parser.add_argument('--instance-type', required=True, help=(
        'Instance type for the endpoint. E.g. `ml.t2.large`. See '
        'documentation for `InstanceType` at https://docs.aws.amazon.com/'
        'sagemaker/latest/dg/API_ProductionVariant.html for full list.'))
    parser.add_argument('--initial-instance-count', default=1, help=(
        'Number of instances to launch initially. Default is 1'))
    parser.add_argument('--forwarding-endpoint', help=(
        'When --endpoint-type is `proxy`, the incoming requests are '
        'forwarded to this endpoint for inferences. Required for `proxy`'),
                        metavar='forwarding endpoint for proxy')
    parser.add_argument('--forwarding-endpoint-region', help=(
        'AWS region for forwarding endpoint. Required for `proxy` endpoint.'),
                        metavar='forwarding endpoint region for proxy')
    parser.add_argument('--saved-model-location', help=(
        's3 location of the tensorflow model package (a tar.gz file).'))
    parser.add_argument('--overwrite-model', default=False, help=(
        'While creating model for the endpoint if another model exists '
        'with the same name, it will be delete if this flag is set.'),
                        action='store_true')
    parser.add_argument('--overwrite-endpoint-config', default=False, help=(
        'While creating configuration for the endpoint if a configuration '
        'with the same name exists, it will deleted if this flag is set.'),
                        action='store_true')
    parser.add_argument('--overwrite-endpoint', default=False, help=(
        'While creating the endpoint if another endpoing with the same name '
        'exists, it will be deleted if this flag is set.'),
                        action='store_true')
    parser.add_argument('--fiddler-image', help=(
        'Docker image to use instead of image based on --endpoint-type. '
        'This is normally not required, but might be useful in some '
        'scenarios'))

    # TODO: Let uses specify extra tags and other options for AWS api.
    # TODO: Describe to user how model schema needs to be set up.


def sagemaker_endpoint_cmd(args):
    """Create SageMaker endpoint."""

    client = boto3.client('sagemaker', region_name=args.endpoint_region)
    # Region could be None, in which case it will be read from environment
    # variables or aws configuration (similar to aws cli).

    c_env = {  # Environment for containers.
        'PREDICTOR_TYPE': args.endpoint_type,
    }

    if args.endpoint_type == 'proxy':
        c_env['FORWARDING_ENDPOINT'] = require_arg(
            args, 'forwarding_endpoint',
            'It is needed when endpoint-type is `proxy`')
        c_env['FORWARDING_ENDPOINT_REGION'] = require_arg(
            args, 'forwarding_endpoint_region',
            'It is needed when endpoint-type is `proxy`')
    elif args.endpoint_type == 'tensorflow':
        c_env['SAVED_MODEL_LOC'] = require_arg(
            args, 'saved_model_location',
            'It is needed for tensorflow endpoints')
        # TODO: Change this to user 'ModelDataUrl'

    def check_existing(thing, thing_name, **kwargs):
        """Invoke'describe_' api to check if the entity exists.
           Delete it if 'overwrite-{entity}' option is set.

           :returns: False if it didn't exist.
                     True if it exists and is deleted successfully.
                     `ValueError` is raised in case of any other errors."""
        try:
            getattr(client, f'describe_{thing}')(**kwargs)
        except ClientError:
            # Mostly implies it does not exist. Continue normally.
            return False
        # It exists. Check it can be overwritten.
        if getattr(args, f'overwrite_{thing}'):
            LOG.info(f'Found existing {thing} with the same name '
                     f'`{thing_name}`. Deleting it.')
            getattr(client, f'delete_{thing}')(**kwargs)
            return True
        else:
            arg_name = f'overwrite_{thing}'.replace('_', '-')
            msg = f'{thing} with name `{thing_name}`, already exists. '\
                  f'Please set `--{arg_name}` to overwrite it.'
            LOG.warning(msg)
            raise ValueError(msg)

    name = args.endpoint_name

    # Create model
    check_existing('model', name, ModelName=name)
    if args.fiddler_image is None:
        image = default_container[args.endpoint_type]
    else:
        image = args.fiddler_image
    create_model_resp = client.create_model(
        ModelName=name,
        ExecutionRoleArn=args.execution_role_arn,
        PrimaryContainer={
            'Image': image,
            'Environment': c_env
        })

    LOG.info('Created model for endpoint. ModelArn: {}'.format(
        create_model_resp['ModelArn']))

    # Create endpoint configuration.
    check_existing('endpoint_config', name, EndpointConfigName=name)
    create_endpoint_config_resp = client.create_endpoint_config(
        EndpointConfigName=name,
        ProductionVariants=[
            {
                'VariantName': name,
                'ModelName': name,
                'InitialInstanceCount': args.initial_instance_count,
                'InstanceType': args.instance_type
            }
        ])

    LOG.info('Created endpoint config. EndpointConfigArn: {}'.format(
        create_endpoint_config_resp['EndpointConfigArn']))

    # Finally create endpoint
    if check_existing('endpoint', name, EndpointName=name):
        # It takes some time for it to be deleted completely. Wait for that.
        client.get_waiter('endpoint_deleted').wait(
            EndpointName=name,
            # Default is 30s x 60, change it to 2s x 300.
            WaiterConfig={'Delay': 2, 'MaxAttempts': 300}
        )

    create_endpoint_resp = client.create_endpoint(EndpointName=name,
                                                  EndpointConfigName=name)
    LOG.info('Created endpoint `{}`. EndpointArn: {}'.format(
        name, create_endpoint_resp['EndpointArn']))

    LOG.info('Waiting for the endpoint to be in service. '
             'This can take several minutes.')
    try:
        client.get_waiter('endpoint_in_service').wait(
            EndpointName=name,
            # Default is 30s x 120. Change it to 5s x 360.
            WaiterConfig={'Delay': 5, 'MaxAttempts': 360}
        )
    except WaiterError as e:
        failure_reason = e.last_response.get('FailureReason',
                                             'Reason is unknown')
        msg = f'Endpoint failed to start up. {failure_reason}'
        LOG.error(msg)
        raise Exception(msg)
    LOG.info(f'Endpoint `{name}` is started and is in service.')
