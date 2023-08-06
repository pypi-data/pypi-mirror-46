import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-guardduty", "0.32.0", __name__, "aws-guardduty@0.32.0.jsii.tgz")
class CfnDetector(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnDetector"):
    """A CloudFormation ``AWS::GuardDuty::Detector``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html
    cloudformationResource:
        AWS::GuardDuty::Detector
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, enable: typing.Union[bool, aws_cdk.cdk.Token], finding_publishing_frequency: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GuardDuty::Detector``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            enable: ``AWS::GuardDuty::Detector.Enable``.
            findingPublishingFrequency: ``AWS::GuardDuty::Detector.FindingPublishingFrequency``.
        """
        props: CfnDetectorProps = {"enable": enable}

        if finding_publishing_frequency is not None:
            props["findingPublishingFrequency"] = finding_publishing_frequency

        jsii.create(CfnDetector, self, [scope, id, props])

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
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> str:
        return jsii.get(self, "detectorId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDetectorProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDetectorProps(jsii.compat.TypedDict, total=False):
    findingPublishingFrequency: str
    """``AWS::GuardDuty::Detector.FindingPublishingFrequency``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-findingpublishingfrequency
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnDetectorProps", jsii_struct_bases=[_CfnDetectorProps])
class CfnDetectorProps(_CfnDetectorProps):
    """Properties for defining a ``AWS::GuardDuty::Detector``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html
    """
    enable: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::GuardDuty::Detector.Enable``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html#cfn-guardduty-detector-enable
    """

class CfnFilter(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnFilter"):
    """A CloudFormation ``AWS::GuardDuty::Filter``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html
    cloudformationResource:
        AWS::GuardDuty::Filter
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, action: str, description: str, detector_id: str, finding_criteria: typing.Union[aws_cdk.cdk.Token, "FindingCriteriaProperty"], rank: typing.Union[jsii.Number, aws_cdk.cdk.Token], name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GuardDuty::Filter``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            action: ``AWS::GuardDuty::Filter.Action``.
            description: ``AWS::GuardDuty::Filter.Description``.
            detectorId: ``AWS::GuardDuty::Filter.DetectorId``.
            findingCriteria: ``AWS::GuardDuty::Filter.FindingCriteria``.
            rank: ``AWS::GuardDuty::Filter.Rank``.
            name: ``AWS::GuardDuty::Filter.Name``.
        """
        props: CfnFilterProps = {"action": action, "description": description, "detectorId": detector_id, "findingCriteria": finding_criteria, "rank": rank}

        if name is not None:
            props["name"] = name

        jsii.create(CfnFilter, self, [scope, id, props])

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
    @jsii.member(jsii_name="filterName")
    def filter_name(self) -> str:
        return jsii.get(self, "filterName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFilterProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnFilter.ConditionProperty", jsii_struct_bases=[])
    class ConditionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html
        """
        eq: typing.List[str]
        """``CfnFilter.ConditionProperty.Eq``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-eq
        """

        gte: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnFilter.ConditionProperty.Gte``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-gte
        """

        lt: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnFilter.ConditionProperty.Lt``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lt
        """

        lte: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnFilter.ConditionProperty.Lte``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-lte
        """

        neq: typing.List[str]
        """``CfnFilter.ConditionProperty.Neq``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-condition.html#cfn-guardduty-filter-condition-neq
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnFilter.FindingCriteriaProperty", jsii_struct_bases=[])
    class FindingCriteriaProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-findingcriteria.html
        """
        criterion: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        """``CfnFilter.FindingCriteriaProperty.Criterion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-findingcriteria.html#cfn-guardduty-filter-findingcriteria-criterion
        """

        itemType: typing.Union[aws_cdk.cdk.Token, "CfnFilter.ConditionProperty"]
        """``CfnFilter.FindingCriteriaProperty.ItemType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-guardduty-filter-findingcriteria.html#cfn-guardduty-filter-findingcriteria-itemtype
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnFilterProps(jsii.compat.TypedDict, total=False):
    name: str
    """``AWS::GuardDuty::Filter.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-name
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnFilterProps", jsii_struct_bases=[_CfnFilterProps])
class CfnFilterProps(_CfnFilterProps):
    """Properties for defining a ``AWS::GuardDuty::Filter``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html
    """
    action: str
    """``AWS::GuardDuty::Filter.Action``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-action
    """

    description: str
    """``AWS::GuardDuty::Filter.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-description
    """

    detectorId: str
    """``AWS::GuardDuty::Filter.DetectorId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-detectorid
    """

    findingCriteria: typing.Union[aws_cdk.cdk.Token, "CfnFilter.FindingCriteriaProperty"]
    """``AWS::GuardDuty::Filter.FindingCriteria``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-findingcriteria
    """

    rank: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::GuardDuty::Filter.Rank``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html#cfn-guardduty-filter-rank
    """

class CfnIPSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnIPSet"):
    """A CloudFormation ``AWS::GuardDuty::IPSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html
    cloudformationResource:
        AWS::GuardDuty::IPSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, activate: typing.Union[bool, aws_cdk.cdk.Token], detector_id: str, format: str, location: str, name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GuardDuty::IPSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            activate: ``AWS::GuardDuty::IPSet.Activate``.
            detectorId: ``AWS::GuardDuty::IPSet.DetectorId``.
            format: ``AWS::GuardDuty::IPSet.Format``.
            location: ``AWS::GuardDuty::IPSet.Location``.
            name: ``AWS::GuardDuty::IPSet.Name``.
        """
        props: CfnIPSetProps = {"activate": activate, "detectorId": detector_id, "format": format, "location": location}

        if name is not None:
            props["name"] = name

        jsii.create(CfnIPSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="ipSetId")
    def ip_set_id(self) -> str:
        return jsii.get(self, "ipSetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnIPSetProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnIPSetProps(jsii.compat.TypedDict, total=False):
    name: str
    """``AWS::GuardDuty::IPSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-name
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnIPSetProps", jsii_struct_bases=[_CfnIPSetProps])
class CfnIPSetProps(_CfnIPSetProps):
    """Properties for defining a ``AWS::GuardDuty::IPSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html
    """
    activate: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::GuardDuty::IPSet.Activate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-activate
    """

    detectorId: str
    """``AWS::GuardDuty::IPSet.DetectorId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-detectorid
    """

    format: str
    """``AWS::GuardDuty::IPSet.Format``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-format
    """

    location: str
    """``AWS::GuardDuty::IPSet.Location``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html#cfn-guardduty-ipset-location
    """

class CfnMaster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnMaster"):
    """A CloudFormation ``AWS::GuardDuty::Master``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html
    cloudformationResource:
        AWS::GuardDuty::Master
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, detector_id: str, master_id: str, invitation_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GuardDuty::Master``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            detectorId: ``AWS::GuardDuty::Master.DetectorId``.
            masterId: ``AWS::GuardDuty::Master.MasterId``.
            invitationId: ``AWS::GuardDuty::Master.InvitationId``.
        """
        props: CfnMasterProps = {"detectorId": detector_id, "masterId": master_id}

        if invitation_id is not None:
            props["invitationId"] = invitation_id

        jsii.create(CfnMaster, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnMasterProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnMasterProps(jsii.compat.TypedDict, total=False):
    invitationId: str
    """``AWS::GuardDuty::Master.InvitationId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-invitationid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnMasterProps", jsii_struct_bases=[_CfnMasterProps])
class CfnMasterProps(_CfnMasterProps):
    """Properties for defining a ``AWS::GuardDuty::Master``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html
    """
    detectorId: str
    """``AWS::GuardDuty::Master.DetectorId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-detectorid
    """

    masterId: str
    """``AWS::GuardDuty::Master.MasterId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html#cfn-guardduty-master-masterid
    """

class CfnMember(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnMember"):
    """A CloudFormation ``AWS::GuardDuty::Member``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html
    cloudformationResource:
        AWS::GuardDuty::Member
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, detector_id: str, email: str, member_id: str, disable_email_notification: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, message: typing.Optional[str]=None, status: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GuardDuty::Member``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            detectorId: ``AWS::GuardDuty::Member.DetectorId``.
            email: ``AWS::GuardDuty::Member.Email``.
            memberId: ``AWS::GuardDuty::Member.MemberId``.
            disableEmailNotification: ``AWS::GuardDuty::Member.DisableEmailNotification``.
            message: ``AWS::GuardDuty::Member.Message``.
            status: ``AWS::GuardDuty::Member.Status``.
        """
        props: CfnMemberProps = {"detectorId": detector_id, "email": email, "memberId": member_id}

        if disable_email_notification is not None:
            props["disableEmailNotification"] = disable_email_notification

        if message is not None:
            props["message"] = message

        if status is not None:
            props["status"] = status

        jsii.create(CfnMember, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnMemberProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnMemberProps(jsii.compat.TypedDict, total=False):
    disableEmailNotification: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::GuardDuty::Member.DisableEmailNotification``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-disableemailnotification
    """
    message: str
    """``AWS::GuardDuty::Member.Message``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-message
    """
    status: str
    """``AWS::GuardDuty::Member.Status``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-status
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnMemberProps", jsii_struct_bases=[_CfnMemberProps])
class CfnMemberProps(_CfnMemberProps):
    """Properties for defining a ``AWS::GuardDuty::Member``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html
    """
    detectorId: str
    """``AWS::GuardDuty::Member.DetectorId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-detectorid
    """

    email: str
    """``AWS::GuardDuty::Member.Email``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-email
    """

    memberId: str
    """``AWS::GuardDuty::Member.MemberId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html#cfn-guardduty-member-memberid
    """

class CfnThreatIntelSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-guardduty.CfnThreatIntelSet"):
    """A CloudFormation ``AWS::GuardDuty::ThreatIntelSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html
    cloudformationResource:
        AWS::GuardDuty::ThreatIntelSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, activate: typing.Union[bool, aws_cdk.cdk.Token], detector_id: str, format: str, location: str, name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GuardDuty::ThreatIntelSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            activate: ``AWS::GuardDuty::ThreatIntelSet.Activate``.
            detectorId: ``AWS::GuardDuty::ThreatIntelSet.DetectorId``.
            format: ``AWS::GuardDuty::ThreatIntelSet.Format``.
            location: ``AWS::GuardDuty::ThreatIntelSet.Location``.
            name: ``AWS::GuardDuty::ThreatIntelSet.Name``.
        """
        props: CfnThreatIntelSetProps = {"activate": activate, "detectorId": detector_id, "format": format, "location": location}

        if name is not None:
            props["name"] = name

        jsii.create(CfnThreatIntelSet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnThreatIntelSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="threatIntelSetId")
    def threat_intel_set_id(self) -> str:
        return jsii.get(self, "threatIntelSetId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnThreatIntelSetProps(jsii.compat.TypedDict, total=False):
    name: str
    """``AWS::GuardDuty::ThreatIntelSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-name
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-guardduty.CfnThreatIntelSetProps", jsii_struct_bases=[_CfnThreatIntelSetProps])
class CfnThreatIntelSetProps(_CfnThreatIntelSetProps):
    """Properties for defining a ``AWS::GuardDuty::ThreatIntelSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html
    """
    activate: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::GuardDuty::ThreatIntelSet.Activate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-activate
    """

    detectorId: str
    """``AWS::GuardDuty::ThreatIntelSet.DetectorId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-detectorid
    """

    format: str
    """``AWS::GuardDuty::ThreatIntelSet.Format``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-format
    """

    location: str
    """``AWS::GuardDuty::ThreatIntelSet.Location``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html#cfn-guardduty-threatintelset-location
    """

__all__ = ["CfnDetector", "CfnDetectorProps", "CfnFilter", "CfnFilterProps", "CfnIPSet", "CfnIPSetProps", "CfnMaster", "CfnMasterProps", "CfnMember", "CfnMemberProps", "CfnThreatIntelSet", "CfnThreatIntelSetProps", "__jsii_assembly__"]

publication.publish()
