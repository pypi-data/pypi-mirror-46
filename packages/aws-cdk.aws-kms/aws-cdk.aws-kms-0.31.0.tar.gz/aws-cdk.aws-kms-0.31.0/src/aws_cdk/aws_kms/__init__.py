import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-kms", "0.31.0", __name__, "aws-kms@0.31.0.jsii.tgz")
class CfnAlias(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.CfnAlias"):
    """A CloudFormation ``AWS::KMS::Alias``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html
    cloudformationResource:
        AWS::KMS::Alias
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, alias_name: str, target_key_id: str) -> None:
        """Create a new ``AWS::KMS::Alias``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            aliasName: ``AWS::KMS::Alias.AliasName``.
            targetKeyId: ``AWS::KMS::Alias.TargetKeyId``.
        """
        props: CfnAliasProps = {"aliasName": alias_name, "targetKeyId": target_key_id}

        jsii.create(CfnAlias, self, [scope, id, props])

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
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> str:
        return jsii.get(self, "aliasName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAliasProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-kms.CfnAliasProps", jsii_struct_bases=[])
class CfnAliasProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::KMS::Alias``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html
    """
    aliasName: str
    """``AWS::KMS::Alias.AliasName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-aliasname
    """

    targetKeyId: str
    """``AWS::KMS::Alias.TargetKeyId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-targetkeyid
    """

class CfnKey(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.CfnKey"):
    """A CloudFormation ``AWS::KMS::Key``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html
    cloudformationResource:
        AWS::KMS::Key
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, key_policy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], description: typing.Optional[str]=None, enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, enable_key_rotation: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, key_usage: typing.Optional[str]=None, pending_window_in_days: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::KMS::Key``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            keyPolicy: ``AWS::KMS::Key.KeyPolicy``.
            description: ``AWS::KMS::Key.Description``.
            enabled: ``AWS::KMS::Key.Enabled``.
            enableKeyRotation: ``AWS::KMS::Key.EnableKeyRotation``.
            keyUsage: ``AWS::KMS::Key.KeyUsage``.
            pendingWindowInDays: ``AWS::KMS::Key.PendingWindowInDays``.
            tags: ``AWS::KMS::Key.Tags``.
        """
        props: CfnKeyProps = {"keyPolicy": key_policy}

        if description is not None:
            props["description"] = description

        if enabled is not None:
            props["enabled"] = enabled

        if enable_key_rotation is not None:
            props["enableKeyRotation"] = enable_key_rotation

        if key_usage is not None:
            props["keyUsage"] = key_usage

        if pending_window_in_days is not None:
            props["pendingWindowInDays"] = pending_window_in_days

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnKey, self, [scope, id, props])

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
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "keyArn")

    @property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> str:
        return jsii.get(self, "keyId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnKeyProps":
        return jsii.get(self, "propertyOverrides")

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


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnKeyProps(jsii.compat.TypedDict, total=False):
    description: str
    """``AWS::KMS::Key.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-description
    """
    enabled: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::KMS::Key.Enabled``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enabled
    """
    enableKeyRotation: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::KMS::Key.EnableKeyRotation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enablekeyrotation
    """
    keyUsage: str
    """``AWS::KMS::Key.KeyUsage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyusage
    """
    pendingWindowInDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::KMS::Key.PendingWindowInDays``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-pendingwindowindays
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::KMS::Key.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-kms.CfnKeyProps", jsii_struct_bases=[_CfnKeyProps])
class CfnKeyProps(_CfnKeyProps):
    """Properties for defining a ``AWS::KMS::Key``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html
    """
    keyPolicy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::KMS::Key.KeyPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keypolicy
    """

class EncryptionKeyAlias(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.EncryptionKeyAlias"):
    """Defines a display name for a customer master key (CMK) in AWS Key Management Service (AWS KMS).

    Using an alias to refer to a key can help you simplify key
    management. For example, when rotating keys, you can just update the alias
    mapping instead of tracking and changing key IDs. For more information, see
    Working with Aliases in the AWS Key Management Service Developer Guide.

    You can also add an alias for a key by calling ``key.addAlias(alias)``.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, alias: str, key: "IEncryptionKey") -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            alias: The name of the alias. The name must start with alias followed by a forward slash, such as alias/. You can't specify aliases that begin with alias/AWS. These aliases are reserved.
            key: The ID of the key for which you are creating the alias. Specify the key's globally unique identifier or Amazon Resource Name (ARN). You can't specify another alias.
        """
        props: EncryptionKeyAliasProps = {"alias": alias, "key": key}

        jsii.create(EncryptionKeyAlias, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> str:
        """The name of the alias."""
        return jsii.get(self, "aliasName")

    @alias_name.setter
    def alias_name(self, value: str):
        return jsii.set(self, "aliasName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-kms.EncryptionKeyAliasProps", jsii_struct_bases=[])
class EncryptionKeyAliasProps(jsii.compat.TypedDict):
    alias: str
    """The name of the alias.

    The name must start with alias followed by a
    forward slash, such as alias/. You can't specify aliases that begin with
    alias/AWS. These aliases are reserved.
    """

    key: "IEncryptionKey"
    """The ID of the key for which you are creating the alias.

    Specify the key's
    globally unique identifier or Amazon Resource Name (ARN). You can't
    specify another alias.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-kms.EncryptionKeyImportProps", jsii_struct_bases=[])
class EncryptionKeyImportProps(jsii.compat.TypedDict):
    keyArn: str
    """The ARN of the external KMS key."""

@jsii.data_type(jsii_type="@aws-cdk/aws-kms.EncryptionKeyProps", jsii_struct_bases=[])
class EncryptionKeyProps(jsii.compat.TypedDict, total=False):
    """Construction properties for a KMS Key object."""
    description: str
    """A description of the key.

    Use a description that helps your users decide
    whether the key is appropriate for a particular task.
    """

    enabled: bool
    """Indicates whether the key is available for use.

    Default:
        Key is enabled
    """

    enableKeyRotation: bool
    """Indicates whether AWS KMS rotates the key.

    Default:
        false
    """

    policy: aws_cdk.aws_iam.PolicyDocument
    """Custom policy document to attach to the KMS key.

    Default:
        A policy document with permissions for the account root to
        administer the key will be created.
    """

    retain: bool
    """Whether the encryption key should be retained when it is removed from the Stack.

    This is useful when one wants to
    retain access to data that was encrypted with a key that is being retired.

    Default:
        true
    """

@jsii.interface(jsii_type="@aws-cdk/aws-kms.IEncryptionKey")
class IEncryptionKey(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IEncryptionKeyProxy

    @property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> str:
        """The ARN of the key."""
        ...

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: str) -> "EncryptionKeyAlias":
        """Defines a new alias for the key.

        Arguments:
            alias: -
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement, allow_no_op: typing.Optional[bool]=None) -> None:
        """Adds a statement to the KMS key resource policy.

        Arguments:
            statement: The policy statement to add.
            allowNoOp: If this is set to ``false`` and there is no policy defined (i.e. external key), the operation will fail. Otherwise, it will no-op.
        """
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "EncryptionKeyImportProps":
        """Exports this key from the current stack.

        Returns:
            a key ref which can be used in a call to ``EncryptionKey.import(ref)``.
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Grant the indicated permissions on this key to the given principal.

        Arguments:
            grantee: -
            actions: -
        """
        ...

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant decryption permisisons using this key to the given principal.

        Arguments:
            grantee: -
        """
        ...

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant encryption permisisons using this key to the given principal.

        Arguments:
            grantee: -
        """
        ...

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant encryption and decryption permisisons using this key to the given principal.

        Arguments:
            grantee: -
        """
        ...


class _IEncryptionKeyProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-kms.IEncryptionKey"
    @property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> str:
        """The ARN of the key."""
        return jsii.get(self, "keyArn")

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: str) -> "EncryptionKeyAlias":
        """Defines a new alias for the key.

        Arguments:
            alias: -
        """
        return jsii.invoke(self, "addAlias", [alias])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement, allow_no_op: typing.Optional[bool]=None) -> None:
        """Adds a statement to the KMS key resource policy.

        Arguments:
            statement: The policy statement to add.
            allowNoOp: If this is set to ``false`` and there is no policy defined (i.e. external key), the operation will fail. Otherwise, it will no-op.
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op])

    @jsii.member(jsii_name="export")
    def export(self) -> "EncryptionKeyImportProps":
        """Exports this key from the current stack.

        Returns:
            a key ref which can be used in a call to ``EncryptionKey.import(ref)``.
        """
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Grant the indicated permissions on this key to the given principal.

        Arguments:
            grantee: -
            actions: -
        """
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant decryption permisisons using this key to the given principal.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantDecrypt", [grantee])

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant encryption permisisons using this key to the given principal.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantEncrypt", [grantee])

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant encryption and decryption permisisons using this key to the given principal.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantEncryptDecrypt", [grantee])


@jsii.implements(IEncryptionKey)
class EncryptionKey(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.EncryptionKey"):
    """Defines a KMS key."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, enable_key_rotation: typing.Optional[bool]=None, policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument]=None, retain: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            description: A description of the key. Use a description that helps your users decide whether the key is appropriate for a particular task.
            enabled: Indicates whether the key is available for use. Default: Key is enabled
            enableKeyRotation: Indicates whether AWS KMS rotates the key. Default: false
            policy: Custom policy document to attach to the KMS key. Default: A policy document with permissions for the account root to administer the key will be created.
            retain: Whether the encryption key should be retained when it is removed from the Stack. This is useful when one wants to retain access to data that was encrypted with a key that is being retired. Default: true
        """
        props: EncryptionKeyProps = {}

        if description is not None:
            props["description"] = description

        if enabled is not None:
            props["enabled"] = enabled

        if enable_key_rotation is not None:
            props["enableKeyRotation"] = enable_key_rotation

        if policy is not None:
            props["policy"] = policy

        if retain is not None:
            props["retain"] = retain

        jsii.create(EncryptionKey, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, key_arn: str) -> "IEncryptionKey":
        """Defines an imported encryption key.

        ``ref`` can be obtained either via a call to ``key.export()`` or using
        literals.

        For example:

        const keyAttr = key.export();
        const keyRef1 = EncryptionKey.import(this, 'MyImportedKey1', keyAttr);
        const keyRef2 = EncryptionKey.import(this, 'MyImportedKey2', {
        keyArn: new KeyArn('arn:aws:kms:...')
        });

        Arguments:
            scope: The parent construct.
            id: The name of the construct.
            props: The key reference.
            keyArn: The ARN of the external KMS key.
        """
        props: EncryptionKeyImportProps = {"keyArn": key_arn}

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: str) -> "EncryptionKeyAlias":
        """Defines a new alias for the key.

        Arguments:
            alias: -
        """
        return jsii.invoke(self, "addAlias", [alias])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement, allow_no_op: typing.Optional[bool]=None) -> None:
        """Adds a statement to the KMS key resource policy.

        Arguments:
            statement: The policy statement to add.
            allowNoOp: If this is set to ``false`` and there is no policy defined (i.e. external key), the operation will fail. Otherwise, it will no-op.
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op])

    @jsii.member(jsii_name="export")
    def export(self) -> "EncryptionKeyImportProps":
        """Exports this key from the current stack.

        Returns:
            a key ref which can be used in a call to ``EncryptionKey.import(ref)``.
        """
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Grant the indicated permissions on this key to the given principal.

        This modifies both the principal's policy as well as the resource policy,
        since the default CloudFormation setup for KMS keys is that the policy
        must not be empty and so default grants won't work.

        Arguments:
            grantee: -
            actions: -
        """
        return jsii.invoke(self, "grant", [grantee, actions])

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant decryption permisisons using this key to the given principal.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantDecrypt", [grantee])

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant encryption permisisons using this key to the given principal.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantEncrypt", [grantee])

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant encryption and decryption permisisons using this key to the given principal.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantEncryptDecrypt", [grantee])

    @property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> str:
        """The ARN of the key."""
        return jsii.get(self, "keyArn")

    @property
    @jsii.member(jsii_name="policy")
    def _policy(self) -> typing.Optional[aws_cdk.aws_iam.PolicyDocument]:
        """Optional policy document that represents the resource policy of this key.

        If specified, addToResourcePolicy can be used to edit this policy.
        Otherwise this method will no-op.
        """
        return jsii.get(self, "policy")


class ViaServicePrincipal(aws_cdk.aws_iam.PrincipalBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kms.ViaServicePrincipal"):
    """A principal to allow access to a key if it's being used through another AWS service."""
    def __init__(self, service_name: str, base_principal: typing.Optional[aws_cdk.aws_iam.IPrincipal]=None) -> None:
        """
        Arguments:
            serviceName: -
            basePrincipal: -
        """
        jsii.create(ViaServicePrincipal, self, [service_name, base_principal])

    @property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> aws_cdk.aws_iam.PrincipalPolicyFragment:
        """Return the policy fragment that identifies this principal in a Policy."""
        return jsii.get(self, "policyFragment")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        return jsii.get(self, "serviceName")


__all__ = ["CfnAlias", "CfnAliasProps", "CfnKey", "CfnKeyProps", "EncryptionKey", "EncryptionKeyAlias", "EncryptionKeyAliasProps", "EncryptionKeyImportProps", "EncryptionKeyProps", "IEncryptionKey", "ViaServicePrincipal", "__jsii_assembly__"]

publication.publish()
