import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cloudfront", "0.32.0", __name__, "aws-cloudfront@0.32.0.jsii.tgz")
@jsii.data_type_optionals(jsii_struct_bases=[])
class _AliasConfiguration(jsii.compat.TypedDict, total=False):
    securityPolicy: "SecurityPolicyProtocol"
    """The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections.

    CloudFront serves your objects only to browsers or devices that support at
    least the SSL version that you specify.

    Default:
        - SSLv3 if sslMethod VIP, TLSv1 if sslMethod SNI
    """
    sslMethod: "SSLMethod"
    """How CloudFront should serve HTTPS requests.

    See the notes on SSLMethod if you wish to use other SSL termination types.

    Default:
        SSLMethod.SNI

    See:
        https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_ViewerCertificate.html
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.AliasConfiguration", jsii_struct_bases=[_AliasConfiguration])
class AliasConfiguration(_AliasConfiguration):
    """Configuration for custom domain names.

    CloudFront can use a custom domain that you provide instead of a
    "cloudfront.net" domain. To use this feature you must provide the list of
    additional domains, and the ACM Certificate that CloudFront should use for
    these additional domains.
    """
    acmCertRef: str
    """ARN of an AWS Certificate Manager (ACM) certificate."""

    names: typing.List[str]
    """Domain names on the certificate.

    Both main domain name and Subject Alternative Names.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.Behavior", jsii_struct_bases=[])
class Behavior(jsii.compat.TypedDict, total=False):
    """A CloudFront behavior wrapper."""
    allowedMethods: "CloudFrontAllowedMethods"
    """The method this CloudFront distribution responds do.

    Default:
        GET_HEAD
    """

    cachedMethods: "CloudFrontAllowedCachedMethods"
    """Which methods are cached by CloudFront by default.

    Default:
        GET_HEAD
    """

    compress: bool
    """If CloudFront should automatically compress some content types.

    Default:
        true
    """

    defaultTtlSeconds: jsii.Number
    """The default amount of time CloudFront will cache an object.

    This value applies only when your custom origin does not add HTTP headers,
    such as Cache-Control max-age, Cache-Control s-maxage, and Expires to objects.

    Default:
        86400 (1 day)
    """

    forwardedValues: "CfnDistribution.ForwardedValuesProperty"
    """The values CloudFront will forward to the origin when making a request.

    Default:
        none (no cookies - no headers)
    """

    isDefaultBehavior: bool
    """If this behavior is the default behavior for the distribution.

    You must specify exactly one default distribution per CloudFront distribution.
    The default behavior is allowed to omit the "path" property.
    """

    maxTtlSeconds: jsii.Number
    """The max amount of time you want objects to stay in the cache before CloudFront queries your origin.

    Default:
        31536000 (one year)
    """

    minTtlSeconds: jsii.Number
    """The minimum amount of time that you want objects to stay in the cache before CloudFront queries your origin."""

    pathPattern: str
    """The path this behavior responds to. Required for all non-default behaviors. (The default behavior implicitly has "*" as the path pattern. )."""

    trustedSigners: typing.List[str]
    """Trusted signers is how CloudFront allows you to serve private content. The signers are the account IDs that are allowed to sign cookies/presigned URLs for this distribution.

    If you pass a non empty value, all requests for this behavior must be signed (no public access will be allowed)
    """

class CfnCloudFrontOriginAccessIdentity(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentity"):
    """A CloudFormation ``AWS::CloudFront::CloudFrontOriginAccessIdentity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html
    cloudformationResource:
        AWS::CloudFront::CloudFrontOriginAccessIdentity
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cloud_front_origin_access_identity_config: typing.Union["CloudFrontOriginAccessIdentityConfigProperty", aws_cdk.cdk.Token]) -> None:
        """Create a new ``AWS::CloudFront::CloudFrontOriginAccessIdentity``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            cloudFrontOriginAccessIdentityConfig: ``AWS::CloudFront::CloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfig``.
        """
        props: CfnCloudFrontOriginAccessIdentityProps = {"cloudFrontOriginAccessIdentityConfig": cloud_front_origin_access_identity_config}

        jsii.create(CfnCloudFrontOriginAccessIdentity, self, [scope, id, props])

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
    @jsii.member(jsii_name="cloudFrontOriginAccessIdentityId")
    def cloud_front_origin_access_identity_id(self) -> str:
        return jsii.get(self, "cloudFrontOriginAccessIdentityId")

    @property
    @jsii.member(jsii_name="cloudFrontOriginAccessIdentityS3CanonicalUserId")
    def cloud_front_origin_access_identity_s3_canonical_user_id(self) -> str:
        """
        cloudformationAttribute:
            S3CanonicalUserId
        """
        return jsii.get(self, "cloudFrontOriginAccessIdentityS3CanonicalUserId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCloudFrontOriginAccessIdentityProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty", jsii_struct_bases=[])
    class CloudFrontOriginAccessIdentityConfigProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig.html
        """
        comment: str
        """``CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty.Comment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig.html#cfn-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig-comment
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentityProps", jsii_struct_bases=[])
class CfnCloudFrontOriginAccessIdentityProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::CloudFront::CloudFrontOriginAccessIdentity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html
    """
    cloudFrontOriginAccessIdentityConfig: typing.Union["CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty", aws_cdk.cdk.Token]
    """``AWS::CloudFront::CloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html#cfn-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig
    """

class CfnDistribution(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution"):
    """A CloudFormation ``AWS::CloudFront::Distribution``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html
    cloudformationResource:
        AWS::CloudFront::Distribution
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, distribution_config: typing.Union[aws_cdk.cdk.Token, "DistributionConfigProperty"], tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::CloudFront::Distribution``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            distributionConfig: ``AWS::CloudFront::Distribution.DistributionConfig``.
            tags: ``AWS::CloudFront::Distribution.Tags``.
        """
        props: CfnDistributionProps = {"distributionConfig": distribution_config}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDistribution, self, [scope, id, props])

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
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> str:
        """
        cloudformationAttribute:
            DomainName
        """
        return jsii.get(self, "distributionDomainName")

    @property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> str:
        return jsii.get(self, "distributionId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDistributionProps":
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
    class _CacheBehaviorProperty(jsii.compat.TypedDict, total=False):
        allowedMethods: typing.List[str]
        """``CfnDistribution.CacheBehaviorProperty.AllowedMethods``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-allowedmethods
        """
        cachedMethods: typing.List[str]
        """``CfnDistribution.CacheBehaviorProperty.CachedMethods``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-cachedmethods
        """
        compress: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDistribution.CacheBehaviorProperty.Compress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-compress
        """
        defaultTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CacheBehaviorProperty.DefaultTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-defaultttl
        """
        fieldLevelEncryptionId: str
        """``CfnDistribution.CacheBehaviorProperty.FieldLevelEncryptionId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-fieldlevelencryptionid
        """
        lambdaFunctionAssociations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.LambdaFunctionAssociationProperty"]]]
        """``CfnDistribution.CacheBehaviorProperty.LambdaFunctionAssociations``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-lambdafunctionassociations
        """
        maxTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CacheBehaviorProperty.MaxTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-maxttl
        """
        minTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CacheBehaviorProperty.MinTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-minttl
        """
        smoothStreaming: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDistribution.CacheBehaviorProperty.SmoothStreaming``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-smoothstreaming
        """
        trustedSigners: typing.List[str]
        """``CfnDistribution.CacheBehaviorProperty.TrustedSigners``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-trustedsigners
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CacheBehaviorProperty", jsii_struct_bases=[_CacheBehaviorProperty])
    class CacheBehaviorProperty(_CacheBehaviorProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html
        """
        forwardedValues: typing.Union["CfnDistribution.ForwardedValuesProperty", aws_cdk.cdk.Token]
        """``CfnDistribution.CacheBehaviorProperty.ForwardedValues``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-forwardedvalues
        """

        pathPattern: str
        """``CfnDistribution.CacheBehaviorProperty.PathPattern``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-pathpattern
        """

        targetOriginId: str
        """``CfnDistribution.CacheBehaviorProperty.TargetOriginId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-targetoriginid
        """

        viewerProtocolPolicy: str
        """``CfnDistribution.CacheBehaviorProperty.ViewerProtocolPolicy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-viewerprotocolpolicy
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CookiesProperty(jsii.compat.TypedDict, total=False):
        whitelistedNames: typing.List[str]
        """``CfnDistribution.CookiesProperty.WhitelistedNames``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cookies.html#cfn-cloudfront-distribution-cookies-whitelistednames
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CookiesProperty", jsii_struct_bases=[_CookiesProperty])
    class CookiesProperty(_CookiesProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cookies.html
        """
        forward: str
        """``CfnDistribution.CookiesProperty.Forward``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cookies.html#cfn-cloudfront-distribution-cookies-forward
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CustomErrorResponseProperty(jsii.compat.TypedDict, total=False):
        errorCachingMinTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CustomErrorResponseProperty.ErrorCachingMinTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-errorcachingminttl
        """
        responseCode: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CustomErrorResponseProperty.ResponseCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-responsecode
        """
        responsePagePath: str
        """``CfnDistribution.CustomErrorResponseProperty.ResponsePagePath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-responsepagepath
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CustomErrorResponseProperty", jsii_struct_bases=[_CustomErrorResponseProperty])
    class CustomErrorResponseProperty(_CustomErrorResponseProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html
        """
        errorCode: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CustomErrorResponseProperty.ErrorCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-errorcode
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CustomOriginConfigProperty(jsii.compat.TypedDict, total=False):
        httpPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CustomOriginConfigProperty.HTTPPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-httpport
        """
        httpsPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CustomOriginConfigProperty.HTTPSPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-httpsport
        """
        originKeepaliveTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CustomOriginConfigProperty.OriginKeepaliveTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originkeepalivetimeout
        """
        originReadTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.CustomOriginConfigProperty.OriginReadTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originreadtimeout
        """
        originSslProtocols: typing.List[str]
        """``CfnDistribution.CustomOriginConfigProperty.OriginSSLProtocols``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originsslprotocols
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CustomOriginConfigProperty", jsii_struct_bases=[_CustomOriginConfigProperty])
    class CustomOriginConfigProperty(_CustomOriginConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html
        """
        originProtocolPolicy: str
        """``CfnDistribution.CustomOriginConfigProperty.OriginProtocolPolicy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originprotocolpolicy
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _DefaultCacheBehaviorProperty(jsii.compat.TypedDict, total=False):
        allowedMethods: typing.List[str]
        """``CfnDistribution.DefaultCacheBehaviorProperty.AllowedMethods``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-allowedmethods
        """
        cachedMethods: typing.List[str]
        """``CfnDistribution.DefaultCacheBehaviorProperty.CachedMethods``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-cachedmethods
        """
        compress: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDistribution.DefaultCacheBehaviorProperty.Compress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-compress
        """
        defaultTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.DefaultCacheBehaviorProperty.DefaultTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-defaultttl
        """
        fieldLevelEncryptionId: str
        """``CfnDistribution.DefaultCacheBehaviorProperty.FieldLevelEncryptionId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-fieldlevelencryptionid
        """
        lambdaFunctionAssociations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.LambdaFunctionAssociationProperty"]]]
        """``CfnDistribution.DefaultCacheBehaviorProperty.LambdaFunctionAssociations``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-lambdafunctionassociations
        """
        maxTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.DefaultCacheBehaviorProperty.MaxTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-maxttl
        """
        minTtl: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDistribution.DefaultCacheBehaviorProperty.MinTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-minttl
        """
        smoothStreaming: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDistribution.DefaultCacheBehaviorProperty.SmoothStreaming``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-smoothstreaming
        """
        trustedSigners: typing.List[str]
        """``CfnDistribution.DefaultCacheBehaviorProperty.TrustedSigners``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-trustedsigners
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.DefaultCacheBehaviorProperty", jsii_struct_bases=[_DefaultCacheBehaviorProperty])
    class DefaultCacheBehaviorProperty(_DefaultCacheBehaviorProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html
        """
        forwardedValues: typing.Union["CfnDistribution.ForwardedValuesProperty", aws_cdk.cdk.Token]
        """``CfnDistribution.DefaultCacheBehaviorProperty.ForwardedValues``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-forwardedvalues
        """

        targetOriginId: str
        """``CfnDistribution.DefaultCacheBehaviorProperty.TargetOriginId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-targetoriginid
        """

        viewerProtocolPolicy: str
        """``CfnDistribution.DefaultCacheBehaviorProperty.ViewerProtocolPolicy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-viewerprotocolpolicy
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _DistributionConfigProperty(jsii.compat.TypedDict, total=False):
        aliases: typing.List[str]
        """``CfnDistribution.DistributionConfigProperty.Aliases``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-aliases
        """
        cacheBehaviors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.CacheBehaviorProperty"]]]
        """``CfnDistribution.DistributionConfigProperty.CacheBehaviors``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-cachebehaviors
        """
        comment: str
        """``CfnDistribution.DistributionConfigProperty.Comment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-comment
        """
        customErrorResponses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnDistribution.CustomErrorResponseProperty", aws_cdk.cdk.Token]]]
        """``CfnDistribution.DistributionConfigProperty.CustomErrorResponses``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-customerrorresponses
        """
        defaultCacheBehavior: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.DefaultCacheBehaviorProperty"]
        """``CfnDistribution.DistributionConfigProperty.DefaultCacheBehavior``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-defaultcachebehavior
        """
        defaultRootObject: str
        """``CfnDistribution.DistributionConfigProperty.DefaultRootObject``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-defaultrootobject
        """
        httpVersion: str
        """``CfnDistribution.DistributionConfigProperty.HttpVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-httpversion
        """
        ipv6Enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDistribution.DistributionConfigProperty.IPV6Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-ipv6enabled
        """
        logging: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.LoggingProperty"]
        """``CfnDistribution.DistributionConfigProperty.Logging``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-logging
        """
        origins: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.OriginProperty"]]]
        """``CfnDistribution.DistributionConfigProperty.Origins``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-origins
        """
        priceClass: str
        """``CfnDistribution.DistributionConfigProperty.PriceClass``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-priceclass
        """
        restrictions: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.RestrictionsProperty"]
        """``CfnDistribution.DistributionConfigProperty.Restrictions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-restrictions
        """
        viewerCertificate: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.ViewerCertificateProperty"]
        """``CfnDistribution.DistributionConfigProperty.ViewerCertificate``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-viewercertificate
        """
        webAclId: str
        """``CfnDistribution.DistributionConfigProperty.WebACLId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-webaclid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.DistributionConfigProperty", jsii_struct_bases=[_DistributionConfigProperty])
    class DistributionConfigProperty(_DistributionConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDistribution.DistributionConfigProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-enabled
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ForwardedValuesProperty(jsii.compat.TypedDict, total=False):
        cookies: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.CookiesProperty"]
        """``CfnDistribution.ForwardedValuesProperty.Cookies``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-cookies
        """
        headers: typing.List[str]
        """``CfnDistribution.ForwardedValuesProperty.Headers``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-headers
        """
        queryStringCacheKeys: typing.List[str]
        """``CfnDistribution.ForwardedValuesProperty.QueryStringCacheKeys``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-querystringcachekeys
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.ForwardedValuesProperty", jsii_struct_bases=[_ForwardedValuesProperty])
    class ForwardedValuesProperty(_ForwardedValuesProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html
        """
        queryString: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDistribution.ForwardedValuesProperty.QueryString``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-querystring
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _GeoRestrictionProperty(jsii.compat.TypedDict, total=False):
        locations: typing.List[str]
        """``CfnDistribution.GeoRestrictionProperty.Locations``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-georestriction.html#cfn-cloudfront-distribution-georestriction-locations
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.GeoRestrictionProperty", jsii_struct_bases=[_GeoRestrictionProperty])
    class GeoRestrictionProperty(_GeoRestrictionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-georestriction.html
        """
        restrictionType: str
        """``CfnDistribution.GeoRestrictionProperty.RestrictionType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-georestriction.html#cfn-cloudfront-distribution-georestriction-restrictiontype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.LambdaFunctionAssociationProperty", jsii_struct_bases=[])
    class LambdaFunctionAssociationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html
        """
        eventType: str
        """``CfnDistribution.LambdaFunctionAssociationProperty.EventType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html#cfn-cloudfront-distribution-lambdafunctionassociation-eventtype
        """

        lambdaFunctionArn: str
        """``CfnDistribution.LambdaFunctionAssociationProperty.LambdaFunctionARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html#cfn-cloudfront-distribution-lambdafunctionassociation-lambdafunctionarn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _LoggingProperty(jsii.compat.TypedDict, total=False):
        includeCookies: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDistribution.LoggingProperty.IncludeCookies``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html#cfn-cloudfront-distribution-logging-includecookies
        """
        prefix: str
        """``CfnDistribution.LoggingProperty.Prefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html#cfn-cloudfront-distribution-logging-prefix
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.LoggingProperty", jsii_struct_bases=[_LoggingProperty])
    class LoggingProperty(_LoggingProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html
        """
        bucket: str
        """``CfnDistribution.LoggingProperty.Bucket``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html#cfn-cloudfront-distribution-logging-bucket
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginCustomHeaderProperty", jsii_struct_bases=[])
    class OriginCustomHeaderProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origincustomheader.html
        """
        headerName: str
        """``CfnDistribution.OriginCustomHeaderProperty.HeaderName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origincustomheader.html#cfn-cloudfront-distribution-origincustomheader-headername
        """

        headerValue: str
        """``CfnDistribution.OriginCustomHeaderProperty.HeaderValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origincustomheader.html#cfn-cloudfront-distribution-origincustomheader-headervalue
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _OriginProperty(jsii.compat.TypedDict, total=False):
        customOriginConfig: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.CustomOriginConfigProperty"]
        """``CfnDistribution.OriginProperty.CustomOriginConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-customoriginconfig
        """
        originCustomHeaders: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDistribution.OriginCustomHeaderProperty"]]]
        """``CfnDistribution.OriginProperty.OriginCustomHeaders``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-origincustomheaders
        """
        originPath: str
        """``CfnDistribution.OriginProperty.OriginPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-originpath
        """
        s3OriginConfig: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.S3OriginConfigProperty"]
        """``CfnDistribution.OriginProperty.S3OriginConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-s3originconfig
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginProperty", jsii_struct_bases=[_OriginProperty])
    class OriginProperty(_OriginProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html
        """
        domainName: str
        """``CfnDistribution.OriginProperty.DomainName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-domainname
        """

        id: str
        """``CfnDistribution.OriginProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-id
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.RestrictionsProperty", jsii_struct_bases=[])
    class RestrictionsProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-restrictions.html
        """
        geoRestriction: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.GeoRestrictionProperty"]
        """``CfnDistribution.RestrictionsProperty.GeoRestriction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-restrictions.html#cfn-cloudfront-distribution-restrictions-georestriction
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.S3OriginConfigProperty", jsii_struct_bases=[])
    class S3OriginConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-s3originconfig.html
        """
        originAccessIdentity: str
        """``CfnDistribution.S3OriginConfigProperty.OriginAccessIdentity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-s3originconfig.html#cfn-cloudfront-distribution-s3originconfig-originaccessidentity
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.ViewerCertificateProperty", jsii_struct_bases=[])
    class ViewerCertificateProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html
        """
        acmCertificateArn: str
        """``CfnDistribution.ViewerCertificateProperty.AcmCertificateArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-acmcertificatearn
        """

        cloudFrontDefaultCertificate: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDistribution.ViewerCertificateProperty.CloudFrontDefaultCertificate``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-cloudfrontdefaultcertificate
        """

        iamCertificateId: str
        """``CfnDistribution.ViewerCertificateProperty.IamCertificateId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-iamcertificateid
        """

        minimumProtocolVersion: str
        """``CfnDistribution.ViewerCertificateProperty.MinimumProtocolVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-minimumprotocolversion
        """

        sslSupportMethod: str
        """``CfnDistribution.ViewerCertificateProperty.SslSupportMethod``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-sslsupportmethod
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDistributionProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::CloudFront::Distribution.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistributionProps", jsii_struct_bases=[_CfnDistributionProps])
class CfnDistributionProps(_CfnDistributionProps):
    """Properties for defining a ``AWS::CloudFront::Distribution``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html
    """
    distributionConfig: typing.Union[aws_cdk.cdk.Token, "CfnDistribution.DistributionConfigProperty"]
    """``AWS::CloudFront::Distribution.DistributionConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-distributionconfig
    """

class CfnStreamingDistribution(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution"):
    """A CloudFormation ``AWS::CloudFront::StreamingDistribution``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html
    cloudformationResource:
        AWS::CloudFront::StreamingDistribution
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, streaming_distribution_config: typing.Union[aws_cdk.cdk.Token, "StreamingDistributionConfigProperty"], tags: typing.List[aws_cdk.cdk.CfnTag]) -> None:
        """Create a new ``AWS::CloudFront::StreamingDistribution``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            streamingDistributionConfig: ``AWS::CloudFront::StreamingDistribution.StreamingDistributionConfig``.
            tags: ``AWS::CloudFront::StreamingDistribution.Tags``.
        """
        props: CfnStreamingDistributionProps = {"streamingDistributionConfig": streaming_distribution_config, "tags": tags}

        jsii.create(CfnStreamingDistribution, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnStreamingDistributionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="streamingDistributionDomainName")
    def streaming_distribution_domain_name(self) -> str:
        """
        cloudformationAttribute:
            DomainName
        """
        return jsii.get(self, "streamingDistributionDomainName")

    @property
    @jsii.member(jsii_name="streamingDistributionId")
    def streaming_distribution_id(self) -> str:
        return jsii.get(self, "streamingDistributionId")

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

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.LoggingProperty", jsii_struct_bases=[])
    class LoggingProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html
        """
        bucket: str
        """``CfnStreamingDistribution.LoggingProperty.Bucket``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html#cfn-cloudfront-streamingdistribution-logging-bucket
        """

        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnStreamingDistribution.LoggingProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html#cfn-cloudfront-streamingdistribution-logging-enabled
        """

        prefix: str
        """``CfnStreamingDistribution.LoggingProperty.Prefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html#cfn-cloudfront-streamingdistribution-logging-prefix
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.S3OriginProperty", jsii_struct_bases=[])
    class S3OriginProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-s3origin.html
        """
        domainName: str
        """``CfnStreamingDistribution.S3OriginProperty.DomainName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-s3origin.html#cfn-cloudfront-streamingdistribution-s3origin-domainname
        """

        originAccessIdentity: str
        """``CfnStreamingDistribution.S3OriginProperty.OriginAccessIdentity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-s3origin.html#cfn-cloudfront-streamingdistribution-s3origin-originaccessidentity
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _StreamingDistributionConfigProperty(jsii.compat.TypedDict, total=False):
        aliases: typing.List[str]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Aliases``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-aliases
        """
        logging: typing.Union[aws_cdk.cdk.Token, "CfnStreamingDistribution.LoggingProperty"]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Logging``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-logging
        """
        priceClass: str
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.PriceClass``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-priceclass
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.StreamingDistributionConfigProperty", jsii_struct_bases=[_StreamingDistributionConfigProperty])
    class StreamingDistributionConfigProperty(_StreamingDistributionConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html
        """
        comment: str
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Comment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-comment
        """

        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-enabled
        """

        s3Origin: typing.Union[aws_cdk.cdk.Token, "CfnStreamingDistribution.S3OriginProperty"]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.S3Origin``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-s3origin
        """

        trustedSigners: typing.Union[aws_cdk.cdk.Token, "CfnStreamingDistribution.TrustedSignersProperty"]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.TrustedSigners``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-trustedsigners
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TrustedSignersProperty(jsii.compat.TypedDict, total=False):
        awsAccountNumbers: typing.List[str]
        """``CfnStreamingDistribution.TrustedSignersProperty.AwsAccountNumbers``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-trustedsigners.html#cfn-cloudfront-streamingdistribution-trustedsigners-awsaccountnumbers
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.TrustedSignersProperty", jsii_struct_bases=[_TrustedSignersProperty])
    class TrustedSignersProperty(_TrustedSignersProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-trustedsigners.html
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnStreamingDistribution.TrustedSignersProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-trustedsigners.html#cfn-cloudfront-streamingdistribution-trustedsigners-enabled
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistributionProps", jsii_struct_bases=[])
class CfnStreamingDistributionProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::CloudFront::StreamingDistribution``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html
    """
    streamingDistributionConfig: typing.Union[aws_cdk.cdk.Token, "CfnStreamingDistribution.StreamingDistributionConfigProperty"]
    """``AWS::CloudFront::StreamingDistribution.StreamingDistributionConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::CloudFront::StreamingDistribution.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-tags
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontAllowedCachedMethods")
class CloudFrontAllowedCachedMethods(enum.Enum):
    """Enums for the methods CloudFront can cache."""
    GET_HEAD = "GET_HEAD"
    GET_HEAD_OPTIONS = "GET_HEAD_OPTIONS"

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontAllowedMethods")
class CloudFrontAllowedMethods(enum.Enum):
    """An enum for the supported methods to a CloudFront distribution."""
    GET_HEAD = "GET_HEAD"
    GET_HEAD_OPTIONS = "GET_HEAD_OPTIONS"
    ALL = "ALL"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CloudFrontWebDistributionProps(jsii.compat.TypedDict, total=False):
    aliasConfiguration: "AliasConfiguration"
    """AliasConfiguration is used to configured CloudFront to respond to requests on custom domain names.

    Default:
        - None.
    """
    comment: str
    """A comment for this distribution in the CloudFront console.

    Default:
        - No comment is added to distribution.
    """
    defaultRootObject: str
    """The default object to serve.

    Default:
        - "index.html" is served.
    """
    enableIpV6: bool
    """If your distribution should have IPv6 enabled.

    Default:
        true
    """
    errorConfigurations: typing.List["CfnDistribution.CustomErrorResponseProperty"]
    """How CloudFront should handle requests that are not successful (eg PageNotFound).

    By default, CloudFront does not replace HTTP status codes in the 4xx and 5xx range
    with custom error messages. CloudFront does not cache HTTP status codes.

    Default:
        - No custom error configuration.
    """
    httpVersion: "HttpVersion"
    """The max supported HTTP Versions.

    Default:
        HttpVersion.HTTP2
    """
    loggingConfig: "LoggingConfiguration"
    """Optional - if we should enable logging. You can pass an empty object ({}) to have us auto create a bucket for logging. Omission of this property indicates no logging is to be enabled.

    Default:
        - no logging is enabled by default.
    """
    priceClass: "PriceClass"
    """The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing).

    Default:
        PriceClass.PriceClass100 the cheapest option for CloudFront is picked by default.
    """
    viewerProtocolPolicy: "ViewerProtocolPolicy"
    """The default viewer policy for incoming clients.

    Default:
        RedirectToHTTPs
    """
    webACLId: str
    """Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution.

    Default:
        - No AWS Web Application Firewall web access control list (web ACL).

    See:
        https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontWebDistributionProps", jsii_struct_bases=[_CloudFrontWebDistributionProps])
class CloudFrontWebDistributionProps(_CloudFrontWebDistributionProps):
    originConfigs: typing.List["SourceConfiguration"]
    """The origin configurations for this distribution.

    Behaviors are a part of the origin.
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CustomOriginConfig(jsii.compat.TypedDict, total=False):
    allowedOriginSSLVersions: typing.List["OriginSslPolicy"]
    """The SSL versions to use when interacting with the origin.

    Default:
        OriginSslPolicy.TLSv1_2
    """
    httpPort: jsii.Number
    """The origin HTTP port.

    Default:
        80
    """
    httpsPort: jsii.Number
    """The origin HTTPS port.

    Default:
        443
    """
    originKeepaliveTimeoutSeconds: jsii.Number
    """The keep alive timeout when making calls in seconds.

    Default:
        5
    """
    originProtocolPolicy: "OriginProtocolPolicy"
    """The protocol (http or https) policy to use when interacting with the origin.

    Default:
        OriginProtocolPolicy.HttpsOnly
    """
    originReadTimeoutSeconds: jsii.Number
    """The read timeout when calling the origin in seconds.

    Default:
        30
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CustomOriginConfig", jsii_struct_bases=[_CustomOriginConfig])
class CustomOriginConfig(_CustomOriginConfig):
    """A custom origin configuration."""
    domainName: str
    """The domain name of the custom origin.

    Should not include the path - that should be in the parent SourceConfiguration
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _ErrorConfiguration(jsii.compat.TypedDict, total=False):
    cacheTtl: jsii.Number
    """How long before this error is retried."""

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.ErrorConfiguration", jsii_struct_bases=[_ErrorConfiguration])
class ErrorConfiguration(_ErrorConfiguration):
    originErrorCode: jsii.Number
    """The error code matched from the origin."""

    respondWithErrorCode: jsii.Number
    """The error code that is sent to the caller."""

    respondWithPage: str
    """The path to service instead."""

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.HttpVersion")
class HttpVersion(enum.Enum):
    HTTP1_1 = "HTTP1_1"
    HTTP2 = "HTTP2"

@jsii.interface(jsii_type="@aws-cdk/aws-cloudfront.IDistribution")
class IDistribution(jsii.compat.Protocol):
    """Interface for CloudFront distributions."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IDistributionProxy

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the distribution."""
        ...


class _IDistributionProxy():
    """Interface for CloudFront distributions."""
    __jsii_type__ = "@aws-cdk/aws-cloudfront.IDistribution"
    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the distribution."""
        return jsii.get(self, "domainName")


@jsii.implements(IDistribution)
class CloudFrontWebDistribution(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CloudFrontWebDistribution"):
    """Amazon CloudFront is a global content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to your viewers with low latency and high transfer speeds. CloudFront fronts user provided content and caches it at edge locations across the world.

    Here's how you can use this construct::

        * import { CloudFront } from '@aws-cdk/aws-cloudfront'
        *
        * const sourceBucket = new Bucket(this, 'Bucket');
        *
        * const distribution = new CloudFrontDistribution(this, 'MyDistribution', {
        *  originConfigs: [
        *    {
        *      s3OriginSource: {
        *      s3BucketSource: sourceBucket
        *      },
        *      behaviors : [ {isDefaultBehavior}]
        *    }
        *  ]
        * });
        * ```

       This will create a CloudFront distribution that uses your S3Bucket as it's origin.

       You can customize the distribution using additional properties from the CloudFrontWebDistributionProps interface.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, origin_configs: typing.List["SourceConfiguration"], alias_configuration: typing.Optional["AliasConfiguration"]=None, comment: typing.Optional[str]=None, default_root_object: typing.Optional[str]=None, enable_ip_v6: typing.Optional[bool]=None, error_configurations: typing.Optional[typing.List["CfnDistribution.CustomErrorResponseProperty"]]=None, http_version: typing.Optional["HttpVersion"]=None, logging_config: typing.Optional["LoggingConfiguration"]=None, price_class: typing.Optional["PriceClass"]=None, viewer_protocol_policy: typing.Optional["ViewerProtocolPolicy"]=None, web_acl_id: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            originConfigs: The origin configurations for this distribution. Behaviors are a part of the origin.
            aliasConfiguration: AliasConfiguration is used to configured CloudFront to respond to requests on custom domain names. Default: - None.
            comment: A comment for this distribution in the CloudFront console. Default: - No comment is added to distribution.
            defaultRootObject: The default object to serve. Default: - "index.html" is served.
            enableIpV6: If your distribution should have IPv6 enabled. Default: true
            errorConfigurations: How CloudFront should handle requests that are not successful (eg PageNotFound). By default, CloudFront does not replace HTTP status codes in the 4xx and 5xx range with custom error messages. CloudFront does not cache HTTP status codes. Default: - No custom error configuration.
            httpVersion: The max supported HTTP Versions. Default: HttpVersion.HTTP2
            loggingConfig: Optional - if we should enable logging. You can pass an empty object ({}) to have us auto create a bucket for logging. Omission of this property indicates no logging is to be enabled. Default: - no logging is enabled by default.
            priceClass: The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing). Default: PriceClass.PriceClass100 the cheapest option for CloudFront is picked by default.
            viewerProtocolPolicy: The default viewer policy for incoming clients. Default: RedirectToHTTPs
            webACLId: Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. Default: - No AWS Web Application Firewall web access control list (web ACL).
        """
        props: CloudFrontWebDistributionProps = {"originConfigs": origin_configs}

        if alias_configuration is not None:
            props["aliasConfiguration"] = alias_configuration

        if comment is not None:
            props["comment"] = comment

        if default_root_object is not None:
            props["defaultRootObject"] = default_root_object

        if enable_ip_v6 is not None:
            props["enableIpV6"] = enable_ip_v6

        if error_configurations is not None:
            props["errorConfigurations"] = error_configurations

        if http_version is not None:
            props["httpVersion"] = http_version

        if logging_config is not None:
            props["loggingConfig"] = logging_config

        if price_class is not None:
            props["priceClass"] = price_class

        if viewer_protocol_policy is not None:
            props["viewerProtocolPolicy"] = viewer_protocol_policy

        if web_acl_id is not None:
            props["webACLId"] = web_acl_id

        jsii.create(CloudFrontWebDistribution, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> str:
        """The distribution ID for this distribution."""
        return jsii.get(self, "distributionId")

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name created by CloudFront for this distribution. If you are using aliases for your distribution, this is the domainName your DNS records should point to. (In Route53, you could create an ALIAS record to this value, for example. )."""
        return jsii.get(self, "domainName")

    @property
    @jsii.member(jsii_name="loggingBucket")
    def logging_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """The logging bucket for this CloudFront distribution. If logging is not enabled for this distribution - this property will be undefined."""
        return jsii.get(self, "loggingBucket")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.LoggingConfiguration", jsii_struct_bases=[])
class LoggingConfiguration(jsii.compat.TypedDict, total=False):
    """Logging configuration for incoming requests."""
    bucket: aws_cdk.aws_s3.IBucket
    """Bucket to log requests to.

    Default:
        - A logging bucket is automatically created.
    """

    includeCookies: bool
    """Whether to include the cookies in the logs.

    Default:
        false
    """

    prefix: str
    """Where in the bucket to store logs.

    Default:
        - No prefix.
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.OriginProtocolPolicy")
class OriginProtocolPolicy(enum.Enum):
    HttpOnly = "HttpOnly"
    MatchViewer = "MatchViewer"
    HttpsOnly = "HttpsOnly"

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.OriginSslPolicy")
class OriginSslPolicy(enum.Enum):
    SSLv3 = "SSLv3"
    TLSv1 = "TLSv1"
    TLSv1_1 = "TLSv1_1"
    TLSv1_2 = "TLSv1_2"

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.PriceClass")
class PriceClass(enum.Enum):
    """The price class determines how many edge locations CloudFront will use for your distribution."""
    PriceClass100 = "PriceClass100"
    PriceClass200 = "PriceClass200"
    PriceClassAll = "PriceClassAll"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _S3OriginConfig(jsii.compat.TypedDict, total=False):
    originAccessIdentityId: str
    """The optional ID of the origin identity cloudfront will use when calling your s3 bucket."""

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.S3OriginConfig", jsii_struct_bases=[_S3OriginConfig])
class S3OriginConfig(_S3OriginConfig):
    s3BucketSource: aws_cdk.aws_s3.IBucket
    """The source bucket to serve content from."""

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.SSLMethod")
class SSLMethod(enum.Enum):
    """The SSL method CloudFront will use for your distribution.

    Server Name Indication (SNI) - is an extension to the TLS computer networking protocol by which a client indicates
    which hostname it is attempting to connect to at the start of the handshaking process. This allows a server to present
    multiple certificates on the same IP address and TCP port number and hence allows multiple secure (HTTPS) websites
    (or any other service over TLS) to be served by the same IP address without requiring all those sites to use the same certificate.

    CloudFront can use SNI to host multiple distributions on the same IP - which a large majority of clients will support.

    If your clients cannot support SNI however - CloudFront can use dedicated IPs for your distribution - but there is a prorated monthly charge for
    using this feature. By default, we use SNI - but you can optionally enable dedicated IPs (VIP).

    See the CloudFront SSL for more details about pricing : https://aws.amazon.com/cloudfront/custom-ssl-domains/
    """
    SNI = "SNI"
    VIP = "VIP"

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.SecurityPolicyProtocol")
class SecurityPolicyProtocol(enum.Enum):
    """The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify."""
    SSLv3 = "SSLv3"
    TLSv1 = "TLSv1"
    TLSv1_2016 = "TLSv1_2016"
    TLSv1_1_2016 = "TLSv1_1_2016"
    TLSv1_2_2018 = "TLSv1_2_2018"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _SourceConfiguration(jsii.compat.TypedDict, total=False):
    customOriginSource: "CustomOriginConfig"
    """A custom origin source - for all non-s3 sources."""
    originHeaders: typing.Mapping[str,str]
    """Any additional headers to pass to the origin.

    Default:
        - No additional headers are passed.
    """
    originPath: str
    """The relative path to the origin root to use for sources.

    Default:
        /
    """
    s3OriginSource: "S3OriginConfig"
    """An s3 origin source - if you're using s3 for your assets."""

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.SourceConfiguration", jsii_struct_bases=[_SourceConfiguration])
class SourceConfiguration(_SourceConfiguration):
    """A source configuration is a wrapper for CloudFront origins and behaviors. An origin is what CloudFront will "be in front of" - that is, CloudFront will pull it's assets from an origin.

    If you're using s3 as a source - pass the ``s3Origin`` property, otherwise, pass the ``customOriginSource`` property.

    One or the other must be passed, and it is invalid to pass both in the same SourceConfiguration.
    """
    behaviors: typing.List["Behavior"]
    """The behaviors associated with this source. At least one (default) behavior must be included."""

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.ViewerProtocolPolicy")
class ViewerProtocolPolicy(enum.Enum):
    """How HTTPs should be handled with your distribution."""
    HTTPSOnly = "HTTPSOnly"
    RedirectToHTTPS = "RedirectToHTTPS"
    AllowAll = "AllowAll"

__all__ = ["AliasConfiguration", "Behavior", "CfnCloudFrontOriginAccessIdentity", "CfnCloudFrontOriginAccessIdentityProps", "CfnDistribution", "CfnDistributionProps", "CfnStreamingDistribution", "CfnStreamingDistributionProps", "CloudFrontAllowedCachedMethods", "CloudFrontAllowedMethods", "CloudFrontWebDistribution", "CloudFrontWebDistributionProps", "CustomOriginConfig", "ErrorConfiguration", "HttpVersion", "IDistribution", "LoggingConfiguration", "OriginProtocolPolicy", "OriginSslPolicy", "PriceClass", "S3OriginConfig", "SSLMethod", "SecurityPolicyProtocol", "SourceConfiguration", "ViewerProtocolPolicy", "__jsii_assembly__"]

publication.publish()
