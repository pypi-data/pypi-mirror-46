import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_logs
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-kinesis", "0.32.0", __name__, "aws-kinesis@0.32.0.jsii.tgz")
class CfnStream(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesis.CfnStream"):
    """A CloudFormation ``AWS::Kinesis::Stream``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html
    cloudformationResource:
        AWS::Kinesis::Stream
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, shard_count: typing.Union[jsii.Number, aws_cdk.cdk.Token], name: typing.Optional[str]=None, retention_period_hours: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, stream_encryption: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["StreamEncryptionProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::Kinesis::Stream``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            shardCount: ``AWS::Kinesis::Stream.ShardCount``.
            name: ``AWS::Kinesis::Stream.Name``.
            retentionPeriodHours: ``AWS::Kinesis::Stream.RetentionPeriodHours``.
            streamEncryption: ``AWS::Kinesis::Stream.StreamEncryption``.
            tags: ``AWS::Kinesis::Stream.Tags``.
        """
        props: CfnStreamProps = {"shardCount": shard_count}

        if name is not None:
            props["name"] = name

        if retention_period_hours is not None:
            props["retentionPeriodHours"] = retention_period_hours

        if stream_encryption is not None:
            props["streamEncryption"] = stream_encryption

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnStream, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStreamProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "streamArn")

    @property
    @jsii.member(jsii_name="streamId")
    def stream_id(self) -> str:
        return jsii.get(self, "streamId")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.CfnStream.StreamEncryptionProperty", jsii_struct_bases=[])
    class StreamEncryptionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html
        """
        encryptionType: str
        """``CfnStream.StreamEncryptionProperty.EncryptionType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html#cfn-kinesis-stream-streamencryption-encryptiontype
        """

        keyId: str
        """``CfnStream.StreamEncryptionProperty.KeyId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html#cfn-kinesis-stream-streamencryption-keyid
        """


class CfnStreamConsumer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesis.CfnStreamConsumer"):
    """A CloudFormation ``AWS::Kinesis::StreamConsumer``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html
    cloudformationResource:
        AWS::Kinesis::StreamConsumer
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, consumer_name: str, stream_arn: str) -> None:
        """Create a new ``AWS::Kinesis::StreamConsumer``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            consumerName: ``AWS::Kinesis::StreamConsumer.ConsumerName``.
            streamArn: ``AWS::Kinesis::StreamConsumer.StreamARN``.
        """
        props: CfnStreamConsumerProps = {"consumerName": consumer_name, "streamArn": stream_arn}

        jsii.create(CfnStreamConsumer, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnStreamConsumerProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="streamConsumerArn")
    def stream_consumer_arn(self) -> str:
        return jsii.get(self, "streamConsumerArn")

    @property
    @jsii.member(jsii_name="streamConsumerConsumerArn")
    def stream_consumer_consumer_arn(self) -> str:
        """
        cloudformationAttribute:
            ConsumerARN
        """
        return jsii.get(self, "streamConsumerConsumerArn")

    @property
    @jsii.member(jsii_name="streamConsumerConsumerCreationTimestamp")
    def stream_consumer_consumer_creation_timestamp(self) -> str:
        """
        cloudformationAttribute:
            ConsumerCreationTimestamp
        """
        return jsii.get(self, "streamConsumerConsumerCreationTimestamp")

    @property
    @jsii.member(jsii_name="streamConsumerConsumerName")
    def stream_consumer_consumer_name(self) -> str:
        """
        cloudformationAttribute:
            ConsumerName
        """
        return jsii.get(self, "streamConsumerConsumerName")

    @property
    @jsii.member(jsii_name="streamConsumerConsumerStatus")
    def stream_consumer_consumer_status(self) -> str:
        """
        cloudformationAttribute:
            ConsumerStatus
        """
        return jsii.get(self, "streamConsumerConsumerStatus")

    @property
    @jsii.member(jsii_name="streamConsumerStreamArn")
    def stream_consumer_stream_arn(self) -> str:
        """
        cloudformationAttribute:
            StreamARN
        """
        return jsii.get(self, "streamConsumerStreamArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.CfnStreamConsumerProps", jsii_struct_bases=[])
class CfnStreamConsumerProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::Kinesis::StreamConsumer``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html
    """
    consumerName: str
    """``AWS::Kinesis::StreamConsumer.ConsumerName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-consumername
    """

    streamArn: str
    """``AWS::Kinesis::StreamConsumer.StreamARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-streamarn
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnStreamProps(jsii.compat.TypedDict, total=False):
    name: str
    """``AWS::Kinesis::Stream.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-name
    """
    retentionPeriodHours: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::Kinesis::Stream.RetentionPeriodHours``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-retentionperiodhours
    """
    streamEncryption: typing.Union[aws_cdk.cdk.Token, "CfnStream.StreamEncryptionProperty"]
    """``AWS::Kinesis::Stream.StreamEncryption``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-streamencryption
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::Kinesis::Stream.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.CfnStreamProps", jsii_struct_bases=[_CfnStreamProps])
class CfnStreamProps(_CfnStreamProps):
    """Properties for defining a ``AWS::Kinesis::Stream``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html
    """
    shardCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::Kinesis::Stream.ShardCount``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-shardcount
    """

@jsii.interface(jsii_type="@aws-cdk/aws-kinesis.IStream")
class IStream(aws_cdk.cdk.IResource, aws_cdk.aws_logs.ILogSubscriptionDestination, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IStreamProxy

    @property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> str:
        """The ARN of the stream.

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> str:
        """The name of the stream.

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this stream."""
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        Arguments:
            grantee: -
        """
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants read/write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        Arguments:
            grantee: -
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to encrypt the
        contents of the stream will also be granted.

        Arguments:
            grantee: -
        """
        ...


class _IStreamProxy(jsii.proxy_for(aws_cdk.cdk.IResource), jsii.proxy_for(aws_cdk.aws_logs.ILogSubscriptionDestination)):
    __jsii_type__ = "@aws-cdk/aws-kinesis.IStream"
    @property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> str:
        """The ARN of the stream.

        attribute:
            true
        """
        return jsii.get(self, "streamArn")

    @property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> str:
        """The name of the stream.

        attribute:
            true
        """
        return jsii.get(self, "streamName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this stream."""
        return jsii.get(self, "encryptionKey")

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants read/write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantReadWrite", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to encrypt the
        contents of the stream will also be granted.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])


@jsii.implements(IStream)
class Stream(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesis.Stream"):
    """A Kinesis stream.

    Can be encrypted with a KMS key.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, encryption: typing.Optional["StreamEncryption"]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, retention_period_hours: typing.Optional[jsii.Number]=None, shard_count: typing.Optional[jsii.Number]=None, stream_name: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            encryption: The kind of server-side encryption to apply to this stream. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: Unencrypted
            encryptionKey: External KMS key to use for stream encryption. The 'encryption' property must be set to "Kms". Default: If encryption is set to "Kms" and this property is undefined, a new KMS key will be created and associated with this stream.
            retentionPeriodHours: The number of hours for the data records that are stored in shards to remain accessible. Default: 24
            shardCount: The number of shards for the stream. Default: 1
            streamName: Enforces a particular physical stream name. Default: 
        """
        props: StreamProps = {}

        if encryption is not None:
            props["encryption"] = encryption

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        if retention_period_hours is not None:
            props["retentionPeriodHours"] = retention_period_hours

        if shard_count is not None:
            props["shardCount"] = shard_count

        if stream_name is not None:
            props["streamName"] = stream_name

        jsii.create(Stream, self, [scope, id, props])

    @jsii.member(jsii_name="fromStreamArn")
    @classmethod
    def from_stream_arn(cls, scope: aws_cdk.cdk.Construct, id: str, stream_arn: str) -> "IStream":
        """
        Arguments:
            scope: -
            id: -
            streamArn: -
        """
        return jsii.sinvoke(cls, "fromStreamArn", [scope, id, stream_arn])

    @jsii.member(jsii_name="fromStreamAttributes")
    @classmethod
    def from_stream_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, stream_arn: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> "IStream":
        """Creates a Stream construct that represents an external stream.

        Arguments:
            scope: The parent creating construct (usually ``this``).
            id: The construct's name.
            attrs: Stream import properties.
            streamArn: The ARN of the stream.
            encryptionKey: The KMS key securing the contents of the stream if encryption is enabled.
        """
        attrs: StreamAttributes = {"streamArn": stream_arn}

        if encryption_key is not None:
            attrs["encryptionKey"] = encryption_key

        return jsii.sinvoke(cls, "fromStreamAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants read/write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantReadWrite", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @jsii.member(jsii_name="logSubscriptionDestination")
    def log_subscription_destination(self, source_log_group: aws_cdk.aws_logs.ILogGroup) -> aws_cdk.aws_logs.LogSubscriptionDestination:
        """Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        Arguments:
            sourceLogGroup: -
        """
        return jsii.invoke(self, "logSubscriptionDestination", [source_log_group])

    @property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> str:
        """The ARN of the stream."""
        return jsii.get(self, "streamArn")

    @property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> str:
        """The name of the stream."""
        return jsii.get(self, "streamName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Optional KMS encryption key associated with this stream."""
        return jsii.get(self, "encryptionKey")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _StreamAttributes(jsii.compat.TypedDict, total=False):
    encryptionKey: aws_cdk.aws_kms.IKey
    """The KMS key securing the contents of the stream if encryption is enabled."""

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.StreamAttributes", jsii_struct_bases=[_StreamAttributes])
class StreamAttributes(_StreamAttributes):
    """A reference to a stream.

    The easiest way to instantiate is to call
    ``stream.export()``. Then, the consumer can use ``Stream.import(this, ref)`` and
    get a ``Stream``.
    """
    streamArn: str
    """The ARN of the stream."""

@jsii.enum(jsii_type="@aws-cdk/aws-kinesis.StreamEncryption")
class StreamEncryption(enum.Enum):
    """What kind of server-side encryption to apply to this stream."""
    Unencrypted = "Unencrypted"
    """Records in the stream are not encrypted."""
    Kms = "Kms"
    """Server-side encryption with a KMS key managed by the user. If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined."""

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesis.StreamProps", jsii_struct_bases=[])
class StreamProps(jsii.compat.TypedDict, total=False):
    encryption: "StreamEncryption"
    """The kind of server-side encryption to apply to this stream.

    If you choose KMS, you can specify a KMS key via ``encryptionKey``. If
    encryption key is not specified, a key will automatically be created.

    Default:
        Unencrypted
    """

    encryptionKey: aws_cdk.aws_kms.IKey
    """External KMS key to use for stream encryption.

    The 'encryption' property must be set to "Kms".

    Default:
        If encryption is set to "Kms" and this property is undefined, a
        new KMS key will be created and associated with this stream.
    """

    retentionPeriodHours: jsii.Number
    """The number of hours for the data records that are stored in shards to remain accessible.

    Default:
        24
    """

    shardCount: jsii.Number
    """The number of shards for the stream.

    Default:
        1
    """

    streamName: str
    """Enforces a particular physical stream name.

    Default:
        
    """

__all__ = ["CfnStream", "CfnStreamConsumer", "CfnStreamConsumerProps", "CfnStreamProps", "IStream", "Stream", "StreamAttributes", "StreamEncryption", "StreamProps", "__jsii_assembly__"]

publication.publish()
