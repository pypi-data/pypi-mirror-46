import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-servicecatalog", "0.32.0", __name__, "aws-servicecatalog@0.32.0.jsii.tgz")
class CfnAcceptedPortfolioShare(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnAcceptedPortfolioShare"):
    """A CloudFormation ``AWS::ServiceCatalog::AcceptedPortfolioShare``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html
    cloudformationResource:
        AWS::ServiceCatalog::AcceptedPortfolioShare
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, accept_language: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::AcceptedPortfolioShare``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            portfolioId: ``AWS::ServiceCatalog::AcceptedPortfolioShare.PortfolioId``.
            acceptLanguage: ``AWS::ServiceCatalog::AcceptedPortfolioShare.AcceptLanguage``.
        """
        props: CfnAcceptedPortfolioShareProps = {"portfolioId": portfolio_id}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        jsii.create(CfnAcceptedPortfolioShare, self, [scope, id, props])

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
    @jsii.member(jsii_name="acceptedPortfolioShareId")
    def accepted_portfolio_share_id(self) -> str:
        return jsii.get(self, "acceptedPortfolioShareId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAcceptedPortfolioShareProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnAcceptedPortfolioShareProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::AcceptedPortfolioShare.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html#cfn-servicecatalog-acceptedportfolioshare-acceptlanguage
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnAcceptedPortfolioShareProps", jsii_struct_bases=[_CfnAcceptedPortfolioShareProps])
class CfnAcceptedPortfolioShareProps(_CfnAcceptedPortfolioShareProps):
    """Properties for defining a ``AWS::ServiceCatalog::AcceptedPortfolioShare``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html
    """
    portfolioId: str
    """``AWS::ServiceCatalog::AcceptedPortfolioShare.PortfolioId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html#cfn-servicecatalog-acceptedportfolioshare-portfolioid
    """

class CfnCloudFormationProduct(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProduct"):
    """A CloudFormation ``AWS::ServiceCatalog::CloudFormationProduct``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html
    cloudformationResource:
        AWS::ServiceCatalog::CloudFormationProduct
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, owner: str, provisioning_artifact_parameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ProvisioningArtifactPropertiesProperty", aws_cdk.cdk.Token]]], accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None, distributor: typing.Optional[str]=None, support_description: typing.Optional[str]=None, support_email: typing.Optional[str]=None, support_url: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::CloudFormationProduct``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::ServiceCatalog::CloudFormationProduct.Name``.
            owner: ``AWS::ServiceCatalog::CloudFormationProduct.Owner``.
            provisioningArtifactParameters: ``AWS::ServiceCatalog::CloudFormationProduct.ProvisioningArtifactParameters``.
            acceptLanguage: ``AWS::ServiceCatalog::CloudFormationProduct.AcceptLanguage``.
            description: ``AWS::ServiceCatalog::CloudFormationProduct.Description``.
            distributor: ``AWS::ServiceCatalog::CloudFormationProduct.Distributor``.
            supportDescription: ``AWS::ServiceCatalog::CloudFormationProduct.SupportDescription``.
            supportEmail: ``AWS::ServiceCatalog::CloudFormationProduct.SupportEmail``.
            supportUrl: ``AWS::ServiceCatalog::CloudFormationProduct.SupportUrl``.
            tags: ``AWS::ServiceCatalog::CloudFormationProduct.Tags``.
        """
        props: CfnCloudFormationProductProps = {"name": name, "owner": owner, "provisioningArtifactParameters": provisioning_artifact_parameters}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        if distributor is not None:
            props["distributor"] = distributor

        if support_description is not None:
            props["supportDescription"] = support_description

        if support_email is not None:
            props["supportEmail"] = support_email

        if support_url is not None:
            props["supportUrl"] = support_url

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnCloudFormationProduct, self, [scope, id, props])

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
    @jsii.member(jsii_name="cloudFormationProductId")
    def cloud_formation_product_id(self) -> str:
        return jsii.get(self, "cloudFormationProductId")

    @property
    @jsii.member(jsii_name="cloudFormationProductProductName")
    def cloud_formation_product_product_name(self) -> str:
        """
        cloudformationAttribute:
            ProductName
        """
        return jsii.get(self, "cloudFormationProductProductName")

    @property
    @jsii.member(jsii_name="cloudFormationProductProvisioningArtifactIds")
    def cloud_formation_product_provisioning_artifact_ids(self) -> str:
        """
        cloudformationAttribute:
            ProvisioningArtifactIds
        """
        return jsii.get(self, "cloudFormationProductProvisioningArtifactIds")

    @property
    @jsii.member(jsii_name="cloudFormationProductProvisioningArtifactNames")
    def cloud_formation_product_provisioning_artifact_names(self) -> str:
        """
        cloudformationAttribute:
            ProvisioningArtifactNames
        """
        return jsii.get(self, "cloudFormationProductProvisioningArtifactNames")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCloudFormationProductProps":
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
    class _ProvisioningArtifactPropertiesProperty(jsii.compat.TypedDict, total=False):
        description: str
        """``CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty.Description``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-description
        """
        disableTemplateValidation: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty.DisableTemplateValidation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-disabletemplatevalidation
        """
        name: str
        """``CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty", jsii_struct_bases=[_ProvisioningArtifactPropertiesProperty])
    class ProvisioningArtifactPropertiesProperty(_ProvisioningArtifactPropertiesProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html
        """
        info: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        """``CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty.Info``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-info
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnCloudFormationProductProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::CloudFormationProduct.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-acceptlanguage
    """
    description: str
    """``AWS::ServiceCatalog::CloudFormationProduct.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-description
    """
    distributor: str
    """``AWS::ServiceCatalog::CloudFormationProduct.Distributor``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-distributor
    """
    supportDescription: str
    """``AWS::ServiceCatalog::CloudFormationProduct.SupportDescription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supportdescription
    """
    supportEmail: str
    """``AWS::ServiceCatalog::CloudFormationProduct.SupportEmail``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supportemail
    """
    supportUrl: str
    """``AWS::ServiceCatalog::CloudFormationProduct.SupportUrl``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supporturl
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::ServiceCatalog::CloudFormationProduct.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProductProps", jsii_struct_bases=[_CfnCloudFormationProductProps])
class CfnCloudFormationProductProps(_CfnCloudFormationProductProps):
    """Properties for defining a ``AWS::ServiceCatalog::CloudFormationProduct``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html
    """
    name: str
    """``AWS::ServiceCatalog::CloudFormationProduct.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-name
    """

    owner: str
    """``AWS::ServiceCatalog::CloudFormationProduct.Owner``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-owner
    """

    provisioningArtifactParameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty", aws_cdk.cdk.Token]]]
    """``AWS::ServiceCatalog::CloudFormationProduct.ProvisioningArtifactParameters``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactparameters
    """

class CfnCloudFormationProvisionedProduct(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProvisionedProduct"):
    """A CloudFormation ``AWS::ServiceCatalog::CloudFormationProvisionedProduct``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html
    cloudformationResource:
        AWS::ServiceCatalog::CloudFormationProvisionedProduct
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, accept_language: typing.Optional[str]=None, notification_arns: typing.Optional[typing.List[str]]=None, path_id: typing.Optional[str]=None, product_id: typing.Optional[str]=None, product_name: typing.Optional[str]=None, provisioned_product_name: typing.Optional[str]=None, provisioning_artifact_id: typing.Optional[str]=None, provisioning_artifact_name: typing.Optional[str]=None, provisioning_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ProvisioningParameterProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::CloudFormationProvisionedProduct``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            acceptLanguage: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.AcceptLanguage``.
            notificationArns: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.NotificationArns``.
            pathId: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.PathId``.
            productId: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProductId``.
            productName: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProductName``.
            provisionedProductName: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProvisionedProductName``.
            provisioningArtifactId: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProvisioningArtifactId``.
            provisioningArtifactName: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProvisioningArtifactName``.
            provisioningParameters: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProvisioningParameters``.
            tags: ``AWS::ServiceCatalog::CloudFormationProvisionedProduct.Tags``.
        """
        props: CfnCloudFormationProvisionedProductProps = {}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if notification_arns is not None:
            props["notificationArns"] = notification_arns

        if path_id is not None:
            props["pathId"] = path_id

        if product_id is not None:
            props["productId"] = product_id

        if product_name is not None:
            props["productName"] = product_name

        if provisioned_product_name is not None:
            props["provisionedProductName"] = provisioned_product_name

        if provisioning_artifact_id is not None:
            props["provisioningArtifactId"] = provisioning_artifact_id

        if provisioning_artifact_name is not None:
            props["provisioningArtifactName"] = provisioning_artifact_name

        if provisioning_parameters is not None:
            props["provisioningParameters"] = provisioning_parameters

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnCloudFormationProvisionedProduct, self, [scope, id, props])

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
    @jsii.member(jsii_name="cloudFormationProvisionedProductCloudformationStackArn")
    def cloud_formation_provisioned_product_cloudformation_stack_arn(self) -> str:
        """
        cloudformationAttribute:
            CloudformationStackArn
        """
        return jsii.get(self, "cloudFormationProvisionedProductCloudformationStackArn")

    @property
    @jsii.member(jsii_name="cloudFormationProvisionedProductId")
    def cloud_formation_provisioned_product_id(self) -> str:
        return jsii.get(self, "cloudFormationProvisionedProductId")

    @property
    @jsii.member(jsii_name="cloudFormationProvisionedProductRecordId")
    def cloud_formation_provisioned_product_record_id(self) -> str:
        """
        cloudformationAttribute:
            RecordId
        """
        return jsii.get(self, "cloudFormationProvisionedProductRecordId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCloudFormationProvisionedProductProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty", jsii_struct_bases=[])
    class ProvisioningParameterProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningparameter.html
        """
        key: str
        """``CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningparameter.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameter-key
        """

        value: str
        """``CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningparameter.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameter-value
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnCloudFormationProvisionedProductProps", jsii_struct_bases=[])
class CfnCloudFormationProvisionedProductProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::ServiceCatalog::CloudFormationProvisionedProduct``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html
    """
    acceptLanguage: str
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-acceptlanguage
    """

    notificationArns: typing.List[str]
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.NotificationArns``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-notificationarns
    """

    pathId: str
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.PathId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-pathid
    """

    productId: str
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProductId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-productid
    """

    productName: str
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProductName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-productname
    """

    provisionedProductName: str
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProvisionedProductName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisionedproductname
    """

    provisioningArtifactId: str
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProvisioningArtifactId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningartifactid
    """

    provisioningArtifactName: str
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProvisioningArtifactName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningartifactname
    """

    provisioningParameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty"]]]
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.ProvisioningParameters``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameters
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::ServiceCatalog::CloudFormationProvisionedProduct.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-tags
    """

class CfnLaunchNotificationConstraint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchNotificationConstraint"):
    """A CloudFormation ``AWS::ServiceCatalog::LaunchNotificationConstraint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html
    cloudformationResource:
        AWS::ServiceCatalog::LaunchNotificationConstraint
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, notification_arns: typing.List[str], portfolio_id: str, product_id: str, accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::LaunchNotificationConstraint``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            notificationArns: ``AWS::ServiceCatalog::LaunchNotificationConstraint.NotificationArns``.
            portfolioId: ``AWS::ServiceCatalog::LaunchNotificationConstraint.PortfolioId``.
            productId: ``AWS::ServiceCatalog::LaunchNotificationConstraint.ProductId``.
            acceptLanguage: ``AWS::ServiceCatalog::LaunchNotificationConstraint.AcceptLanguage``.
            description: ``AWS::ServiceCatalog::LaunchNotificationConstraint.Description``.
        """
        props: CfnLaunchNotificationConstraintProps = {"notificationArns": notification_arns, "portfolioId": portfolio_id, "productId": product_id}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        jsii.create(CfnLaunchNotificationConstraint, self, [scope, id, props])

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
    @jsii.member(jsii_name="launchNotificationConstraintId")
    def launch_notification_constraint_id(self) -> str:
        return jsii.get(self, "launchNotificationConstraintId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchNotificationConstraintProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnLaunchNotificationConstraintProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::LaunchNotificationConstraint.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-acceptlanguage
    """
    description: str
    """``AWS::ServiceCatalog::LaunchNotificationConstraint.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-description
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchNotificationConstraintProps", jsii_struct_bases=[_CfnLaunchNotificationConstraintProps])
class CfnLaunchNotificationConstraintProps(_CfnLaunchNotificationConstraintProps):
    """Properties for defining a ``AWS::ServiceCatalog::LaunchNotificationConstraint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html
    """
    notificationArns: typing.List[str]
    """``AWS::ServiceCatalog::LaunchNotificationConstraint.NotificationArns``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-notificationarns
    """

    portfolioId: str
    """``AWS::ServiceCatalog::LaunchNotificationConstraint.PortfolioId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-portfolioid
    """

    productId: str
    """``AWS::ServiceCatalog::LaunchNotificationConstraint.ProductId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-productid
    """

class CfnLaunchRoleConstraint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchRoleConstraint"):
    """A CloudFormation ``AWS::ServiceCatalog::LaunchRoleConstraint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html
    cloudformationResource:
        AWS::ServiceCatalog::LaunchRoleConstraint
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, product_id: str, role_arn: str, accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::LaunchRoleConstraint``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            portfolioId: ``AWS::ServiceCatalog::LaunchRoleConstraint.PortfolioId``.
            productId: ``AWS::ServiceCatalog::LaunchRoleConstraint.ProductId``.
            roleArn: ``AWS::ServiceCatalog::LaunchRoleConstraint.RoleArn``.
            acceptLanguage: ``AWS::ServiceCatalog::LaunchRoleConstraint.AcceptLanguage``.
            description: ``AWS::ServiceCatalog::LaunchRoleConstraint.Description``.
        """
        props: CfnLaunchRoleConstraintProps = {"portfolioId": portfolio_id, "productId": product_id, "roleArn": role_arn}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        jsii.create(CfnLaunchRoleConstraint, self, [scope, id, props])

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
    @jsii.member(jsii_name="launchRoleConstraintId")
    def launch_role_constraint_id(self) -> str:
        return jsii.get(self, "launchRoleConstraintId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchRoleConstraintProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnLaunchRoleConstraintProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::LaunchRoleConstraint.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-acceptlanguage
    """
    description: str
    """``AWS::ServiceCatalog::LaunchRoleConstraint.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-description
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchRoleConstraintProps", jsii_struct_bases=[_CfnLaunchRoleConstraintProps])
class CfnLaunchRoleConstraintProps(_CfnLaunchRoleConstraintProps):
    """Properties for defining a ``AWS::ServiceCatalog::LaunchRoleConstraint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html
    """
    portfolioId: str
    """``AWS::ServiceCatalog::LaunchRoleConstraint.PortfolioId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-portfolioid
    """

    productId: str
    """``AWS::ServiceCatalog::LaunchRoleConstraint.ProductId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-productid
    """

    roleArn: str
    """``AWS::ServiceCatalog::LaunchRoleConstraint.RoleArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-rolearn
    """

class CfnLaunchTemplateConstraint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchTemplateConstraint"):
    """A CloudFormation ``AWS::ServiceCatalog::LaunchTemplateConstraint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html
    cloudformationResource:
        AWS::ServiceCatalog::LaunchTemplateConstraint
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, product_id: str, rules: str, accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::LaunchTemplateConstraint``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            portfolioId: ``AWS::ServiceCatalog::LaunchTemplateConstraint.PortfolioId``.
            productId: ``AWS::ServiceCatalog::LaunchTemplateConstraint.ProductId``.
            rules: ``AWS::ServiceCatalog::LaunchTemplateConstraint.Rules``.
            acceptLanguage: ``AWS::ServiceCatalog::LaunchTemplateConstraint.AcceptLanguage``.
            description: ``AWS::ServiceCatalog::LaunchTemplateConstraint.Description``.
        """
        props: CfnLaunchTemplateConstraintProps = {"portfolioId": portfolio_id, "productId": product_id, "rules": rules}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        jsii.create(CfnLaunchTemplateConstraint, self, [scope, id, props])

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
    @jsii.member(jsii_name="launchTemplateConstraintId")
    def launch_template_constraint_id(self) -> str:
        return jsii.get(self, "launchTemplateConstraintId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchTemplateConstraintProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnLaunchTemplateConstraintProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::LaunchTemplateConstraint.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-acceptlanguage
    """
    description: str
    """``AWS::ServiceCatalog::LaunchTemplateConstraint.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-description
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnLaunchTemplateConstraintProps", jsii_struct_bases=[_CfnLaunchTemplateConstraintProps])
class CfnLaunchTemplateConstraintProps(_CfnLaunchTemplateConstraintProps):
    """Properties for defining a ``AWS::ServiceCatalog::LaunchTemplateConstraint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html
    """
    portfolioId: str
    """``AWS::ServiceCatalog::LaunchTemplateConstraint.PortfolioId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-portfolioid
    """

    productId: str
    """``AWS::ServiceCatalog::LaunchTemplateConstraint.ProductId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-productid
    """

    rules: str
    """``AWS::ServiceCatalog::LaunchTemplateConstraint.Rules``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-rules
    """

class CfnPortfolio(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolio"):
    """A CloudFormation ``AWS::ServiceCatalog::Portfolio``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html
    cloudformationResource:
        AWS::ServiceCatalog::Portfolio
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, display_name: str, provider_name: str, accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::Portfolio``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            displayName: ``AWS::ServiceCatalog::Portfolio.DisplayName``.
            providerName: ``AWS::ServiceCatalog::Portfolio.ProviderName``.
            acceptLanguage: ``AWS::ServiceCatalog::Portfolio.AcceptLanguage``.
            description: ``AWS::ServiceCatalog::Portfolio.Description``.
            tags: ``AWS::ServiceCatalog::Portfolio.Tags``.
        """
        props: CfnPortfolioProps = {"displayName": display_name, "providerName": provider_name}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnPortfolio, self, [scope, id, props])

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
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> str:
        return jsii.get(self, "portfolioId")

    @property
    @jsii.member(jsii_name="portfolioName")
    def portfolio_name(self) -> str:
        """
        cloudformationAttribute:
            PortfolioName
        """
        return jsii.get(self, "portfolioName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPortfolioProps":
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


class CfnPortfolioPrincipalAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioPrincipalAssociation"):
    """A CloudFormation ``AWS::ServiceCatalog::PortfolioPrincipalAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html
    cloudformationResource:
        AWS::ServiceCatalog::PortfolioPrincipalAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, principal_arn: str, principal_type: str, accept_language: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::PortfolioPrincipalAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            portfolioId: ``AWS::ServiceCatalog::PortfolioPrincipalAssociation.PortfolioId``.
            principalArn: ``AWS::ServiceCatalog::PortfolioPrincipalAssociation.PrincipalARN``.
            principalType: ``AWS::ServiceCatalog::PortfolioPrincipalAssociation.PrincipalType``.
            acceptLanguage: ``AWS::ServiceCatalog::PortfolioPrincipalAssociation.AcceptLanguage``.
        """
        props: CfnPortfolioPrincipalAssociationProps = {"portfolioId": portfolio_id, "principalArn": principal_arn, "principalType": principal_type}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        jsii.create(CfnPortfolioPrincipalAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="portfolioPrincipalAssociationId")
    def portfolio_principal_association_id(self) -> str:
        return jsii.get(self, "portfolioPrincipalAssociationId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPortfolioPrincipalAssociationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnPortfolioPrincipalAssociationProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::PortfolioPrincipalAssociation.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-acceptlanguage
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioPrincipalAssociationProps", jsii_struct_bases=[_CfnPortfolioPrincipalAssociationProps])
class CfnPortfolioPrincipalAssociationProps(_CfnPortfolioPrincipalAssociationProps):
    """Properties for defining a ``AWS::ServiceCatalog::PortfolioPrincipalAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html
    """
    portfolioId: str
    """``AWS::ServiceCatalog::PortfolioPrincipalAssociation.PortfolioId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-portfolioid
    """

    principalArn: str
    """``AWS::ServiceCatalog::PortfolioPrincipalAssociation.PrincipalARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-principalarn
    """

    principalType: str
    """``AWS::ServiceCatalog::PortfolioPrincipalAssociation.PrincipalType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-principaltype
    """

class CfnPortfolioProductAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioProductAssociation"):
    """A CloudFormation ``AWS::ServiceCatalog::PortfolioProductAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html
    cloudformationResource:
        AWS::ServiceCatalog::PortfolioProductAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, product_id: str, accept_language: typing.Optional[str]=None, source_portfolio_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::PortfolioProductAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            portfolioId: ``AWS::ServiceCatalog::PortfolioProductAssociation.PortfolioId``.
            productId: ``AWS::ServiceCatalog::PortfolioProductAssociation.ProductId``.
            acceptLanguage: ``AWS::ServiceCatalog::PortfolioProductAssociation.AcceptLanguage``.
            sourcePortfolioId: ``AWS::ServiceCatalog::PortfolioProductAssociation.SourcePortfolioId``.
        """
        props: CfnPortfolioProductAssociationProps = {"portfolioId": portfolio_id, "productId": product_id}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if source_portfolio_id is not None:
            props["sourcePortfolioId"] = source_portfolio_id

        jsii.create(CfnPortfolioProductAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="portfolioProductAssociationId")
    def portfolio_product_association_id(self) -> str:
        return jsii.get(self, "portfolioProductAssociationId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPortfolioProductAssociationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnPortfolioProductAssociationProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::PortfolioProductAssociation.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-acceptlanguage
    """
    sourcePortfolioId: str
    """``AWS::ServiceCatalog::PortfolioProductAssociation.SourcePortfolioId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-sourceportfolioid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioProductAssociationProps", jsii_struct_bases=[_CfnPortfolioProductAssociationProps])
class CfnPortfolioProductAssociationProps(_CfnPortfolioProductAssociationProps):
    """Properties for defining a ``AWS::ServiceCatalog::PortfolioProductAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html
    """
    portfolioId: str
    """``AWS::ServiceCatalog::PortfolioProductAssociation.PortfolioId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-portfolioid
    """

    productId: str
    """``AWS::ServiceCatalog::PortfolioProductAssociation.ProductId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-productid
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnPortfolioProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::Portfolio.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-acceptlanguage
    """
    description: str
    """``AWS::ServiceCatalog::Portfolio.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-description
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::ServiceCatalog::Portfolio.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioProps", jsii_struct_bases=[_CfnPortfolioProps])
class CfnPortfolioProps(_CfnPortfolioProps):
    """Properties for defining a ``AWS::ServiceCatalog::Portfolio``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html
    """
    displayName: str
    """``AWS::ServiceCatalog::Portfolio.DisplayName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-displayname
    """

    providerName: str
    """``AWS::ServiceCatalog::Portfolio.ProviderName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-providername
    """

class CfnPortfolioShare(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioShare"):
    """A CloudFormation ``AWS::ServiceCatalog::PortfolioShare``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html
    cloudformationResource:
        AWS::ServiceCatalog::PortfolioShare
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, account_id: str, portfolio_id: str, accept_language: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::PortfolioShare``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            accountId: ``AWS::ServiceCatalog::PortfolioShare.AccountId``.
            portfolioId: ``AWS::ServiceCatalog::PortfolioShare.PortfolioId``.
            acceptLanguage: ``AWS::ServiceCatalog::PortfolioShare.AcceptLanguage``.
        """
        props: CfnPortfolioShareProps = {"accountId": account_id, "portfolioId": portfolio_id}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        jsii.create(CfnPortfolioShare, self, [scope, id, props])

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
    @jsii.member(jsii_name="portfolioShareId")
    def portfolio_share_id(self) -> str:
        return jsii.get(self, "portfolioShareId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPortfolioShareProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnPortfolioShareProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::PortfolioShare.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-acceptlanguage
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnPortfolioShareProps", jsii_struct_bases=[_CfnPortfolioShareProps])
class CfnPortfolioShareProps(_CfnPortfolioShareProps):
    """Properties for defining a ``AWS::ServiceCatalog::PortfolioShare``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html
    """
    accountId: str
    """``AWS::ServiceCatalog::PortfolioShare.AccountId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-accountid
    """

    portfolioId: str
    """``AWS::ServiceCatalog::PortfolioShare.PortfolioId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-portfolioid
    """

class CfnResourceUpdateConstraint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnResourceUpdateConstraint"):
    """A CloudFormation ``AWS::ServiceCatalog::ResourceUpdateConstraint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html
    cloudformationResource:
        AWS::ServiceCatalog::ResourceUpdateConstraint
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, portfolio_id: str, product_id: str, tag_update_on_provisioned_product: str, accept_language: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::ResourceUpdateConstraint``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            portfolioId: ``AWS::ServiceCatalog::ResourceUpdateConstraint.PortfolioId``.
            productId: ``AWS::ServiceCatalog::ResourceUpdateConstraint.ProductId``.
            tagUpdateOnProvisionedProduct: ``AWS::ServiceCatalog::ResourceUpdateConstraint.TagUpdateOnProvisionedProduct``.
            acceptLanguage: ``AWS::ServiceCatalog::ResourceUpdateConstraint.AcceptLanguage``.
            description: ``AWS::ServiceCatalog::ResourceUpdateConstraint.Description``.
        """
        props: CfnResourceUpdateConstraintProps = {"portfolioId": portfolio_id, "productId": product_id, "tagUpdateOnProvisionedProduct": tag_update_on_provisioned_product}

        if accept_language is not None:
            props["acceptLanguage"] = accept_language

        if description is not None:
            props["description"] = description

        jsii.create(CfnResourceUpdateConstraint, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnResourceUpdateConstraintProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="resourceUpdateConstraintId")
    def resource_update_constraint_id(self) -> str:
        return jsii.get(self, "resourceUpdateConstraintId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnResourceUpdateConstraintProps(jsii.compat.TypedDict, total=False):
    acceptLanguage: str
    """``AWS::ServiceCatalog::ResourceUpdateConstraint.AcceptLanguage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-acceptlanguage
    """
    description: str
    """``AWS::ServiceCatalog::ResourceUpdateConstraint.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-description
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnResourceUpdateConstraintProps", jsii_struct_bases=[_CfnResourceUpdateConstraintProps])
class CfnResourceUpdateConstraintProps(_CfnResourceUpdateConstraintProps):
    """Properties for defining a ``AWS::ServiceCatalog::ResourceUpdateConstraint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html
    """
    portfolioId: str
    """``AWS::ServiceCatalog::ResourceUpdateConstraint.PortfolioId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-portfolioid
    """

    productId: str
    """``AWS::ServiceCatalog::ResourceUpdateConstraint.ProductId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-productid
    """

    tagUpdateOnProvisionedProduct: str
    """``AWS::ServiceCatalog::ResourceUpdateConstraint.TagUpdateOnProvisionedProduct``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-tagupdateonprovisionedproduct
    """

class CfnTagOption(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnTagOption"):
    """A CloudFormation ``AWS::ServiceCatalog::TagOption``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html
    cloudformationResource:
        AWS::ServiceCatalog::TagOption
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, key: str, value: str, active: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::ServiceCatalog::TagOption``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            key: ``AWS::ServiceCatalog::TagOption.Key``.
            value: ``AWS::ServiceCatalog::TagOption.Value``.
            active: ``AWS::ServiceCatalog::TagOption.Active``.
        """
        props: CfnTagOptionProps = {"key": key, "value": value}

        if active is not None:
            props["active"] = active

        jsii.create(CfnTagOption, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTagOptionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tagOptionId")
    def tag_option_id(self) -> str:
        return jsii.get(self, "tagOptionId")


class CfnTagOptionAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicecatalog.CfnTagOptionAssociation"):
    """A CloudFormation ``AWS::ServiceCatalog::TagOptionAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html
    cloudformationResource:
        AWS::ServiceCatalog::TagOptionAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource_id: str, tag_option_id: str) -> None:
        """Create a new ``AWS::ServiceCatalog::TagOptionAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            resourceId: ``AWS::ServiceCatalog::TagOptionAssociation.ResourceId``.
            tagOptionId: ``AWS::ServiceCatalog::TagOptionAssociation.TagOptionId``.
        """
        props: CfnTagOptionAssociationProps = {"resourceId": resource_id, "tagOptionId": tag_option_id}

        jsii.create(CfnTagOptionAssociation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTagOptionAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tagOptionAssociationId")
    def tag_option_association_id(self) -> str:
        return jsii.get(self, "tagOptionAssociationId")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnTagOptionAssociationProps", jsii_struct_bases=[])
class CfnTagOptionAssociationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::ServiceCatalog::TagOptionAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html
    """
    resourceId: str
    """``AWS::ServiceCatalog::TagOptionAssociation.ResourceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html#cfn-servicecatalog-tagoptionassociation-resourceid
    """

    tagOptionId: str
    """``AWS::ServiceCatalog::TagOptionAssociation.TagOptionId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html#cfn-servicecatalog-tagoptionassociation-tagoptionid
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnTagOptionProps(jsii.compat.TypedDict, total=False):
    active: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::ServiceCatalog::TagOption.Active``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-active
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-servicecatalog.CfnTagOptionProps", jsii_struct_bases=[_CfnTagOptionProps])
class CfnTagOptionProps(_CfnTagOptionProps):
    """Properties for defining a ``AWS::ServiceCatalog::TagOption``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html
    """
    key: str
    """``AWS::ServiceCatalog::TagOption.Key``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-key
    """

    value: str
    """``AWS::ServiceCatalog::TagOption.Value``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-value
    """

__all__ = ["CfnAcceptedPortfolioShare", "CfnAcceptedPortfolioShareProps", "CfnCloudFormationProduct", "CfnCloudFormationProductProps", "CfnCloudFormationProvisionedProduct", "CfnCloudFormationProvisionedProductProps", "CfnLaunchNotificationConstraint", "CfnLaunchNotificationConstraintProps", "CfnLaunchRoleConstraint", "CfnLaunchRoleConstraintProps", "CfnLaunchTemplateConstraint", "CfnLaunchTemplateConstraintProps", "CfnPortfolio", "CfnPortfolioPrincipalAssociation", "CfnPortfolioPrincipalAssociationProps", "CfnPortfolioProductAssociation", "CfnPortfolioProductAssociationProps", "CfnPortfolioProps", "CfnPortfolioShare", "CfnPortfolioShareProps", "CfnResourceUpdateConstraint", "CfnResourceUpdateConstraintProps", "CfnTagOption", "CfnTagOptionAssociation", "CfnTagOptionAssociationProps", "CfnTagOptionProps", "__jsii_assembly__"]

publication.publish()
