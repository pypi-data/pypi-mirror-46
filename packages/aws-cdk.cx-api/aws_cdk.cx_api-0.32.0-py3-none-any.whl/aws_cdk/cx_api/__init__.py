import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/cx-api", "0.32.0", __name__, "cx-api@0.32.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/cx-api.AppRuntime", jsii_struct_bases=[])
class AppRuntime(jsii.compat.TypedDict):
    """Information about the application's runtime components."""
    libraries: typing.Mapping[str,str]
    """The list of libraries loaded in the application, associated with their versions."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _Artifact(jsii.compat.TypedDict, total=False):
    autoDeploy: bool
    dependencies: typing.List[str]
    metadata: typing.Mapping[str,typing.Any]
    missing: typing.Mapping[str,typing.Any]
    properties: typing.Mapping[str,typing.Any]

@jsii.data_type(jsii_type="@aws-cdk/cx-api.Artifact", jsii_struct_bases=[_Artifact])
class Artifact(_Artifact):
    environment: str

    type: "ArtifactType"

@jsii.enum(jsii_type="@aws-cdk/cx-api.ArtifactType")
class ArtifactType(enum.Enum):
    AwsCloudFormationStack = "AwsCloudFormationStack"
    AwsEcrDockerImage = "AwsEcrDockerImage"
    AwsS3Object = "AwsS3Object"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _AssemblyManifest(jsii.compat.TypedDict, total=False):
    artifacts: typing.Mapping[str,"Artifact"]
    """The set of artifacts in this assembly."""
    runtime: "AppRuntime"
    """Runtime information."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.AssemblyManifest", jsii_struct_bases=[_AssemblyManifest])
class AssemblyManifest(_AssemblyManifest):
    version: str
    """Protocol version."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.AvailabilityZonesContextQuery", jsii_struct_bases=[])
class AvailabilityZonesContextQuery(jsii.compat.TypedDict, total=False):
    """Query to hosted zone context provider."""
    account: str
    """Query account."""

    region: str
    """Query region."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.BuildManifest", jsii_struct_bases=[])
class BuildManifest(jsii.compat.TypedDict):
    steps: typing.Mapping[str,"BuildStep"]

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BuildStep(jsii.compat.TypedDict, total=False):
    depends: typing.List[str]

@jsii.data_type(jsii_type="@aws-cdk/cx-api.BuildStep", jsii_struct_bases=[_BuildStep])
class BuildStep(_BuildStep):
    parameters: typing.Mapping[str,typing.Any]

    type: str

@jsii.enum(jsii_type="@aws-cdk/cx-api.BuildStepType")
class BuildStepType(enum.Enum):
    CopyFile = "CopyFile"
    ZipDirectory = "ZipDirectory"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _ContainerImageAssetMetadataEntry(jsii.compat.TypedDict, total=False):
    buildArgs: typing.Mapping[str,str]
    """Build args to pass to the ``docker build`` command.

    Default:
        no build args are passed
    """
    repositoryName: str
    """ECR repository name, if omitted a default name based on the asset's ID is used instead.

    Specify this property if you need to statically
    address the image, e.g. from a Kubernetes Pod.
    Note, this is only the repository name, without the registry and
    the tag parts.

    Default:
        automatically derived from the asset's ID.
    """

@jsii.data_type(jsii_type="@aws-cdk/cx-api.ContainerImageAssetMetadataEntry", jsii_struct_bases=[_ContainerImageAssetMetadataEntry])
class ContainerImageAssetMetadataEntry(_ContainerImageAssetMetadataEntry):
    id: str
    """Logical identifier for the asset."""

    imageNameParameter: str
    """ECR Repository name and repo digest (separated by "@sha256:") where this image is stored."""

    packaging: str
    """Type of asset."""

    path: str
    """Path on disk to the asset."""

    sourceHash: str
    """The hash of the source directory used to build the asset."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.Environment", jsii_struct_bases=[])
class Environment(jsii.compat.TypedDict):
    """Models an AWS execution environment, for use within the CDK toolkit."""
    account: str
    """The 12-digit AWS account ID for the account this environment deploys into."""

    name: str
    """The arbitrary name of this environment (user-set, or at least user-meaningful)."""

    region: str
    """The AWS region name where this environment deploys into."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.FileAssetMetadataEntry", jsii_struct_bases=[])
class FileAssetMetadataEntry(jsii.compat.TypedDict):
    artifactHashParameter: str
    """The name of the parameter where the hash of the bundled asset should be passed in."""

    id: str
    """Logical identifier for the asset."""

    packaging: str
    """Requested packaging style."""

    path: str
    """Path on disk to the asset."""

    s3BucketParameter: str
    """Name of parameter where S3 bucket should be passed in."""

    s3KeyParameter: str
    """Name of parameter where S3 key should be passed in."""

    sourceHash: str
    """The hash of the source directory used to build the asset."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _HostedZoneContextQuery(jsii.compat.TypedDict, total=False):
    account: str
    """Query account."""
    privateZone: bool
    """True if the zone you want to find is a private hosted zone."""
    region: str
    """Query region."""
    vpcId: str
    """The VPC ID to that the private zone must be associated with.

    If you provide VPC ID and privateZone is false, this will return no results
    and raise an error.
    """

@jsii.data_type(jsii_type="@aws-cdk/cx-api.HostedZoneContextQuery", jsii_struct_bases=[_HostedZoneContextQuery])
class HostedZoneContextQuery(_HostedZoneContextQuery):
    """Query to hosted zone context provider."""
    domainName: str
    """The domain name e.g. example.com to lookup."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _MetadataEntry(jsii.compat.TypedDict, total=False):
    data: typing.Any
    """The data."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.MetadataEntry", jsii_struct_bases=[_MetadataEntry])
class MetadataEntry(_MetadataEntry):
    """An metadata entry in the construct."""
    trace: typing.List[str]
    """A stack trace for when the entry was created."""

    type: str
    """The type of the metadata entry."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.MissingContext", jsii_struct_bases=[])
class MissingContext(jsii.compat.TypedDict):
    """Represents a missing piece of context."""
    props: typing.Mapping[str,typing.Any]

    provider: str

@jsii.data_type(jsii_type="@aws-cdk/cx-api.SSMParameterContextQuery", jsii_struct_bases=[])
class SSMParameterContextQuery(jsii.compat.TypedDict, total=False):
    """Query to hosted zone context provider."""
    account: str
    """Query account."""

    parameterName: str
    """Parameter name to query."""

    region: str
    """Query region."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.SynthesizeResponse", jsii_struct_bases=[AssemblyManifest])
class SynthesizeResponse(AssemblyManifest, jsii.compat.TypedDict):
    """
    Deprecated:
        use ``AssemblyManifest``
    """
    stacks: typing.List["SynthesizedStack"]

@jsii.data_type_optionals(jsii_struct_bases=[])
class _SynthesizedStack(jsii.compat.TypedDict, total=False):
    autoDeploy: bool
    dependsOn: typing.List[str]
    """Other stacks this stack depends on."""
    missing: typing.Mapping[str,"MissingContext"]

@jsii.data_type(jsii_type="@aws-cdk/cx-api.SynthesizedStack", jsii_struct_bases=[_SynthesizedStack])
class SynthesizedStack(_SynthesizedStack):
    """A complete synthesized stack."""
    environment: "Environment"

    metadata: typing.Mapping[str,typing.List["MetadataEntry"]]

    name: str

    template: typing.Any

@jsii.data_type_optionals(jsii_struct_bases=[])
class _VpcContextQuery(jsii.compat.TypedDict, total=False):
    account: str
    """Query account."""
    region: str
    """Query region."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcContextQuery", jsii_struct_bases=[_VpcContextQuery])
class VpcContextQuery(_VpcContextQuery):
    """Query input for looking up a VPC."""
    filter: typing.Mapping[str,str]
    """Filters to apply to the VPC.

    Filter parameters are the same as passed to DescribeVpcs.

    See:
        https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcs.html
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _VpcContextResponse(jsii.compat.TypedDict, total=False):
    isolatedSubnetIds: typing.List[str]
    """IDs of all isolated subnets.

    Element count: #(availabilityZones) · #(isolatedGroups)
    """
    isolatedSubnetNames: typing.List[str]
    """Name of isolated subnet groups.

    Element count: #(isolatedGroups)
    """
    privateSubnetIds: typing.List[str]
    """IDs of all private subnets.

    Element count: #(availabilityZones) · #(privateGroups)
    """
    privateSubnetNames: typing.List[str]
    """Name of private subnet groups.

    Element count: #(privateGroups)
    """
    publicSubnetIds: typing.List[str]
    """IDs of all public subnets.

    Element count: #(availabilityZones) · #(publicGroups)
    """
    publicSubnetNames: typing.List[str]
    """Name of public subnet groups.

    Element count: #(publicGroups)
    """
    vpnGatewayId: str
    """The VPN gateway ID."""

@jsii.data_type(jsii_type="@aws-cdk/cx-api.VpcContextResponse", jsii_struct_bases=[_VpcContextResponse])
class VpcContextResponse(_VpcContextResponse):
    """Properties of a discovered VPC."""
    availabilityZones: typing.List[str]
    """AZs."""

    vpcId: str
    """VPC id."""

__all__ = ["AppRuntime", "Artifact", "ArtifactType", "AssemblyManifest", "AvailabilityZonesContextQuery", "BuildManifest", "BuildStep", "BuildStepType", "ContainerImageAssetMetadataEntry", "Environment", "FileAssetMetadataEntry", "HostedZoneContextQuery", "MetadataEntry", "MissingContext", "SSMParameterContextQuery", "SynthesizeResponse", "SynthesizedStack", "VpcContextQuery", "VpcContextResponse", "__jsii_assembly__"]

publication.publish()
