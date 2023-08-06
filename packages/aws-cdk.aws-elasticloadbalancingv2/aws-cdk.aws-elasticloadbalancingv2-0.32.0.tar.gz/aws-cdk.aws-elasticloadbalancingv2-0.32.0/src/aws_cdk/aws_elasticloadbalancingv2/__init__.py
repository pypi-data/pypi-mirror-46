import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticloadbalancingv2", "0.32.0", __name__, "aws-elasticloadbalancingv2@0.32.0.jsii.tgz")
@jsii.data_type_optionals(jsii_struct_bases=[])
class _AddNetworkTargetsProps(jsii.compat.TypedDict, total=False):
    deregistrationDelaySec: jsii.Number
    """The amount of time for Elastic Load Balancing to wait before deregistering a target.

    The range is 0-3600 seconds.

    Default:
        300
    """
    healthCheck: "HealthCheck"
    """Health check configuration.

    Default:
        No health check
    """
    proxyProtocolV2: bool
    """Indicates whether Proxy Protocol version 2 is enabled.

    Default:
        false
    """
    targetGroupName: str
    """The name of the target group.

    This name must be unique per region per account, can have a maximum of
    32 characters, must contain only alphanumeric characters or hyphens, and
    must not begin or end with a hyphen.

    Default:
        Automatically generated
    """
    targets: typing.List["INetworkLoadBalancerTarget"]
    """The targets to add to this target group.

    Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
    target. If you use either ``Instance`` or ``IPAddress`` as targets, all
    target must be of the same type.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddNetworkTargetsProps", jsii_struct_bases=[_AddNetworkTargetsProps])
class AddNetworkTargetsProps(_AddNetworkTargetsProps):
    """Properties for adding new network targets to a listener."""
    port: jsii.Number
    """The port on which the listener listens for requests.

    Default:
        Determined from protocol if known
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddRuleProps", jsii_struct_bases=[])
class AddRuleProps(jsii.compat.TypedDict, total=False):
    """Properties for adding a conditional load balancing rule."""
    hostHeader: str
    """Rule applies if the requested host matches the indicated host.

    May contain up to three '*' wildcards.

    Requires that priority is set.

    Default:
        No host condition

    See:
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
    """

    pathPattern: str
    """Rule applies if the requested path matches the given path pattern.

    May contain up to three '*' wildcards.

    Requires that priority is set.

    Default:
        No path condition

    See:
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
    """

    priority: jsii.Number
    """Priority of this target group.

    The rule with the lowest priority will be used for every request.
    If priority is not given, these target groups will be added as
    defaults, and must not have conditions.

    Priorities must be unique.

    Default:
        Target groups are used as defaults
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddApplicationTargetGroupsProps", jsii_struct_bases=[AddRuleProps])
class AddApplicationTargetGroupsProps(AddRuleProps, jsii.compat.TypedDict):
    """Properties for adding a new target group to a listener."""
    targetGroups: typing.List["IApplicationTargetGroup"]
    """Target groups to forward requests to."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddApplicationTargetsProps", jsii_struct_bases=[AddRuleProps])
class AddApplicationTargetsProps(AddRuleProps, jsii.compat.TypedDict, total=False):
    """Properties for adding new targets to a listener."""
    deregistrationDelaySec: jsii.Number
    """The amount of time for Elastic Load Balancing to wait before deregistering a target.

    The range is 0–3600 seconds.

    Default:
        300
    """

    healthCheck: "HealthCheck"
    """Health check configuration.

    Default:
        No health check
    """

    port: jsii.Number
    """The port on which the listener listens for requests.

    Default:
        Determined from protocol if known
    """

    protocol: "ApplicationProtocol"
    """The protocol to use.

    Default:
        Determined from port if known
    """

    slowStartSec: jsii.Number
    """The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group.

    The range is 30–900 seconds (15 minutes).

    Default:
        0
    """

    stickinessCookieDurationSec: jsii.Number
    """The stickiness cookie expiration period.

    Setting this value enables load balancer stickiness.

    After this period, the cookie is considered stale. The minimum value is
    1 second and the maximum value is 7 days (604800 seconds).

    Default:
        86400 (1 day)
    """

    targetGroupName: str
    """The name of the target group.

    This name must be unique per region per account, can have a maximum of
    32 characters, must contain only alphanumeric characters or hyphens, and
    must not begin or end with a hyphen.

    Default:
        Automatically generated
    """

    targets: typing.List["IApplicationLoadBalancerTarget"]
    """The targets to add to this target group.

    Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
    target. If you use either ``Instance`` or ``IPAddress`` as targets, all
    target must be of the same type.
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _ApplicationListenerAttributes(jsii.compat.TypedDict, total=False):
    defaultPort: jsii.Number
    """The default port on which this listener is listening."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerAttributes", jsii_struct_bases=[_ApplicationListenerAttributes])
class ApplicationListenerAttributes(_ApplicationListenerAttributes):
    """Properties to reference an existing listener."""
    listenerArn: str
    """ARN of the listener."""

    securityGroupId: str
    """Security group ID of the load balancer this listener is associated with."""

class ApplicationListenerCertificate(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerCertificate"):
    """Add certificates to a listener."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, certificate_arns: typing.List[str], listener: "IApplicationListener") -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            certificateArns: ARNs of certificates to attach. Duplicates are not allowed.
            listener: The listener to attach the rule to.
        """
        props: ApplicationListenerCertificateProps = {"certificateArns": certificate_arns, "listener": listener}

        jsii.create(ApplicationListenerCertificate, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerCertificateProps", jsii_struct_bases=[])
class ApplicationListenerCertificateProps(jsii.compat.TypedDict):
    """Properties for adding a set of certificates to a listener."""
    certificateArns: typing.List[str]
    """ARNs of certificates to attach.

    Duplicates are not allowed.
    """

    listener: "IApplicationListener"
    """The listener to attach the rule to."""

class ApplicationListenerRule(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerRule"):
    """Define a new listener rule."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, listener: "IApplicationListener", priority: jsii.Number, fixed_response: typing.Optional["FixedResponse"]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            listener: The listener to attach the rule to.
            priority: Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
            fixedResponse: Fixed response to return. Only one of ``fixedResponse`` or ``targetGroups`` can be specified. Default: - No fixed response.
            hostHeader: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Default: - No host condition.
            pathPattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Default: - No path condition.
            targetGroups: Target groups to forward requests to. Only one of ``targetGroups`` or ``fixedResponse`` can be specified. Default: - No target groups.
        """
        props: ApplicationListenerRuleProps = {"listener": listener, "priority": priority}

        if fixed_response is not None:
            props["fixedResponse"] = fixed_response

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if target_groups is not None:
            props["targetGroups"] = target_groups

        jsii.create(ApplicationListenerRule, self, [scope, id, props])

    @jsii.member(jsii_name="addFixedResponse")
    def add_fixed_response(self, *, status_code: str, content_type: typing.Optional["ContentType"]=None, message_body: typing.Optional[str]=None) -> None:
        """Add a fixed response.

        Arguments:
            fixedResponse: -
            statusCode: The HTTP response code (2XX, 4XX or 5XX).
            contentType: The content type. Default: text/plain
            messageBody: The message. Default: no message
        """
        fixed_response: FixedResponse = {"statusCode": status_code}

        if content_type is not None:
            fixed_response["contentType"] = content_type

        if message_body is not None:
            fixed_response["messageBody"] = message_body

        return jsii.invoke(self, "addFixedResponse", [fixed_response])

    @jsii.member(jsii_name="addTargetGroup")
    def add_target_group(self, target_group: "IApplicationTargetGroup") -> None:
        """Add a TargetGroup to load balance to.

        Arguments:
            targetGroup: -
        """
        return jsii.invoke(self, "addTargetGroup", [target_group])

    @jsii.member(jsii_name="setCondition")
    def set_condition(self, field: str, values: typing.Optional[typing.List[str]]=None) -> None:
        """Add a non-standard condition to this rule.

        Arguments:
            field: -
            values: -
        """
        return jsii.invoke(self, "setCondition", [field, values])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the rule."""
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="listenerRuleArn")
    def listener_rule_arn(self) -> str:
        """The ARN of this rule."""
        return jsii.get(self, "listenerRuleArn")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ApplicationLoadBalancerAttributes(jsii.compat.TypedDict, total=False):
    loadBalancerCanonicalHostedZoneId: str
    """The canonical hosted zone ID of this load balancer.

    Default:
        - When not provided, LB cannot be used as Route53 Alias target.
    """
    loadBalancerDnsName: str
    """The DNS name of this load balancer.

    Default:
        - When not provided, LB cannot be used as Route53 Alias target.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerAttributes", jsii_struct_bases=[_ApplicationLoadBalancerAttributes])
class ApplicationLoadBalancerAttributes(_ApplicationLoadBalancerAttributes):
    """Properties to reference an existing load balancer."""
    loadBalancerArn: str
    """ARN of the load balancer."""

    securityGroupId: str
    """ID of the load balancer's security group."""

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationProtocol")
class ApplicationProtocol(enum.Enum):
    """Load balancing protocol for application load balancers."""
    Http = "Http"
    """HTTP."""
    Https = "Https"
    """HTTPS."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseApplicationListenerProps", jsii_struct_bases=[])
class BaseApplicationListenerProps(jsii.compat.TypedDict, total=False):
    """Basic properties for an ApplicationListener."""
    certificateArns: typing.List[str]
    """The certificates to use on this listener.

    Default:
        - No certificates.
    """

    defaultTargetGroups: typing.List["IApplicationTargetGroup"]
    """Default target groups to load balance to.

    Default:
        - None.
    """

    open: bool
    """Allow anyone to connect to this listener.

    If this is specified, the listener will be opened up to anyone who can reach it.
    For internal load balancers this is anyone in the same VPC. For public load
    balancers, this is anyone on the internet.

    If you want to be more selective about who can access this load
    balancer, set this to ``false`` and use the listener's ``connections``
    object to selectively grant access to the listener.

    Default:
        true
    """

    port: jsii.Number
    """The port on which the listener listens for requests.

    Default:
        - Determined from protocol if known.
    """

    protocol: "ApplicationProtocol"
    """The protocol to use.

    Default:
        - Determined from port if known.
    """

    sslPolicy: "SslPolicy"
    """The security policy that defines which ciphers and protocols are supported.

    Default:
        - The current predefined security policy.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerProps", jsii_struct_bases=[BaseApplicationListenerProps])
class ApplicationListenerProps(BaseApplicationListenerProps, jsii.compat.TypedDict):
    """Properties for defining a standalone ApplicationListener."""
    loadBalancer: "IApplicationLoadBalancer"
    """The load balancer to attach this listener to."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BaseApplicationListenerRuleProps(jsii.compat.TypedDict, total=False):
    fixedResponse: "FixedResponse"
    """Fixed response to return.

    Only one of ``fixedResponse`` or
    ``targetGroups`` can be specified.

    Default:
        - No fixed response.
    """
    hostHeader: str
    """Rule applies if the requested host matches the indicated host.

    May contain up to three '*' wildcards.

    Default:
        - No host condition.

    See:
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
    """
    pathPattern: str
    """Rule applies if the requested path matches the given path pattern.

    May contain up to three '*' wildcards.

    Default:
        - No path condition.

    See:
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
    """
    targetGroups: typing.List["IApplicationTargetGroup"]
    """Target groups to forward requests to.

    Only one of ``targetGroups`` or
    ``fixedResponse`` can be specified.

    Default:
        - No target groups.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseApplicationListenerRuleProps", jsii_struct_bases=[_BaseApplicationListenerRuleProps])
class BaseApplicationListenerRuleProps(_BaseApplicationListenerRuleProps):
    """Basic properties for defining a rule on a listener."""
    priority: jsii.Number
    """Priority of the rule.

    The rule with the lowest priority will be used for every request.

    Priorities must be unique.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListenerRuleProps", jsii_struct_bases=[BaseApplicationListenerRuleProps])
class ApplicationListenerRuleProps(BaseApplicationListenerRuleProps, jsii.compat.TypedDict):
    """Properties for defining a listener rule."""
    listener: "IApplicationListener"
    """The listener to attach the rule to."""

class BaseListener(aws_cdk.cdk.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseListener"):
    """Base class for listeners."""
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseListenerProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, additional_props: typing.Any) -> None:
        """
        Arguments:
            scope: -
            id: -
            additionalProps: -
        """
        jsii.create(BaseListener, self, [scope, id, additional_props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate this listener."""
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "listenerArn")


class _BaseListenerProxy(BaseListener, jsii.proxy_for(aws_cdk.cdk.Resource)):
    pass

class BaseLoadBalancer(aws_cdk.cdk.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseLoadBalancer"):
    """Base class for both Application and Network Load Balancers."""
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseLoadBalancerProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, base_props: "BaseLoadBalancerProps", additional_props: typing.Any) -> None:
        """
        Arguments:
            scope: -
            id: -
            baseProps: -
            additionalProps: -
        """
        jsii.create(BaseLoadBalancer, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="removeAttribute")
    def remove_attribute(self, key: str) -> None:
        """Remove an attribute from the load balancer.

        Arguments:
            key: -
        """
        return jsii.invoke(self, "removeAttribute", [key])

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(self, key: str, value: typing.Optional[str]=None) -> None:
        """Set a non-standard attribute on the load balancer.

        Arguments:
            key: -
            value: -

        See:
            https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#load-balancer-attributes
        """
        return jsii.invoke(self, "setAttribute", [key, value])

    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        """The ARN of this load balancer.

        attribute:
            true

        Example::
            arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-internal-load-balancer/50dc6c495c0c9188
        """
        return jsii.get(self, "loadBalancerArn")

    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> str:
        """The canonical hosted zone ID of this load balancer.

        attribute:
            true

        Example::
            Z2P70J7EXAMPLE
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneId")

    @property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        """The DNS name of this load balancer.

        attribute:
            true

        Example::
            my-load-balancer-424835706.us-west-2.elb.amazonaws.com
        """
        return jsii.get(self, "loadBalancerDnsName")

    @property
    @jsii.member(jsii_name="loadBalancerFullName")
    def load_balancer_full_name(self) -> str:
        """The full name of this load balancer.

        attribute:
            true

        Example::
            app/my-load-balancer/50dc6c495c0c9188
        """
        return jsii.get(self, "loadBalancerFullName")

    @property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> str:
        """The name of this load balancer.

        attribute:
            true

        Example::
            my-load-balancer
        """
        return jsii.get(self, "loadBalancerName")

    @property
    @jsii.member(jsii_name="loadBalancerSecurityGroups")
    def load_balancer_security_groups(self) -> typing.List[str]:
        """
        attribute:
            true
        """
        return jsii.get(self, "loadBalancerSecurityGroups")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in, if available.

        If the Load Balancer was imported, the VPC is not available.
        """
        return jsii.get(self, "vpc")


class _BaseLoadBalancerProxy(BaseLoadBalancer, jsii.proxy_for(aws_cdk.cdk.Resource)):
    pass

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BaseLoadBalancerProps(jsii.compat.TypedDict, total=False):
    deletionProtection: bool
    """Indicates whether deletion protection is enabled.

    Default:
        false
    """
    internetFacing: bool
    """Whether the load balancer has an internet-routable address.

    Default:
        false
    """
    loadBalancerName: str
    """Name of the load balancer.

    Default:
        - Automatically generated name.
    """
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection
    """Where in the VPC to place the load balancer.

    Default:
        - Public subnets if internetFacing, otherwise private subnets.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseLoadBalancerProps", jsii_struct_bases=[_BaseLoadBalancerProps])
class BaseLoadBalancerProps(_BaseLoadBalancerProps):
    """Shared properties of both Application and Network Load Balancers."""
    vpc: aws_cdk.aws_ec2.IVpc
    """The VPC network to place the load balancer in."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancerProps", jsii_struct_bases=[BaseLoadBalancerProps])
class ApplicationLoadBalancerProps(BaseLoadBalancerProps, jsii.compat.TypedDict, total=False):
    """Properties for defining an Application Load Balancer."""
    http2Enabled: bool
    """Indicates whether HTTP/2 is enabled.

    Default:
        true
    """

    idleTimeoutSecs: jsii.Number
    """The load balancer idle timeout, in seconds.

    Default:
        60
    """

    ipAddressType: "IpAddressType"
    """The type of IP addresses to use.

    Only applies to application load balancers.

    Default:
        IpAddressType.Ipv4
    """

    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    """Security group to associate with this load balancer.

    Default:
        A security group is created
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BaseNetworkListenerProps(jsii.compat.TypedDict, total=False):
    certificates: typing.List["INetworkListenerCertificateProps"]
    """Certificate list of ACM cert ARNs.

    Default:
        - No certificates.
    """
    defaultTargetGroups: typing.List["INetworkTargetGroup"]
    """Default target groups to load balance to.

    Default:
        - None.
    """
    protocol: "Protocol"
    """Protocol for listener, expects TCP or TLS.

    Default:
        - TLS if certificates are provided. TCP otherwise.
    """
    sslPolicy: "SslPolicy"
    """SSL Policy.

    Default:
        - Current predefined security policy.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseNetworkListenerProps", jsii_struct_bases=[_BaseNetworkListenerProps])
class BaseNetworkListenerProps(_BaseNetworkListenerProps):
    """Basic properties for a Network Listener."""
    port: jsii.Number
    """The port on which the listener listens for requests."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BaseTargetGroupProps(jsii.compat.TypedDict, total=False):
    deregistrationDelaySec: jsii.Number
    """The amount of time for Elastic Load Balancing to wait before deregistering a target.

    The range is 0-3600 seconds.

    Default:
        300
    """
    healthCheck: "HealthCheck"
    """Health check configuration.

    Default:
        - None.
    """
    targetGroupName: str
    """The name of the target group.

    This name must be unique per region per account, can have a maximum of
    32 characters, must contain only alphanumeric characters or hyphens, and
    must not begin or end with a hyphen.

    Default:
        - Automatically generated.
    """
    targetType: "TargetType"
    """The type of targets registered to this TargetGroup, either IP or Instance.

    All targets registered into the group must be of this type. If you
    register targets to the TargetGroup in the CDK app, the TargetType is
    determined automatically.

    Default:
        - Determined automatically.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.BaseTargetGroupProps", jsii_struct_bases=[_BaseTargetGroupProps])
class BaseTargetGroupProps(_BaseTargetGroupProps):
    """Basic properties of both Application and Network Target Groups."""
    vpc: aws_cdk.aws_ec2.IVpc
    """The virtual private cloud (VPC)."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationTargetGroupProps", jsii_struct_bases=[BaseTargetGroupProps])
class ApplicationTargetGroupProps(BaseTargetGroupProps, jsii.compat.TypedDict, total=False):
    """Properties for defining an Application Target Group."""
    port: jsii.Number
    """The port on which the listener listens for requests.

    Default:
        - Determined from protocol if known.
    """

    protocol: "ApplicationProtocol"
    """The protocol to use.

    Default:
        - Determined from port if known.
    """

    slowStartSec: jsii.Number
    """The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group.

    The range is 30–900 seconds (15 minutes).

    Default:
        0
    """

    stickinessCookieDurationSec: jsii.Number
    """The stickiness cookie expiration period.

    Setting this value enables load balancer stickiness.

    After this period, the cookie is considered stale. The minimum value is
    1 second and the maximum value is 7 days (604800 seconds).

    Default:
        86400 (1 day)
    """

    targets: typing.List["IApplicationLoadBalancerTarget"]
    """The targets to add to this target group.

    Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
    target. If you use either ``Instance`` or ``IPAddress`` as targets, all
    target must be of the same type.

    Default:
        - No targets.
    """

class CfnListener(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::Listener``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
    cloudformationResource:
        AWS::ElasticLoadBalancingV2::Listener
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, default_actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ActionProperty", aws_cdk.cdk.Token]]], load_balancer_arn: str, port: typing.Union[jsii.Number, aws_cdk.cdk.Token], protocol: str, certificates: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "CertificateProperty"]]]]]=None, ssl_policy: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::Listener``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            defaultActions: ``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.
            loadBalancerArn: ``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.
            port: ``AWS::ElasticLoadBalancingV2::Listener.Port``.
            protocol: ``AWS::ElasticLoadBalancingV2::Listener.Protocol``.
            certificates: ``AWS::ElasticLoadBalancingV2::Listener.Certificates``.
            sslPolicy: ``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.
        """
        props: CfnListenerProps = {"defaultActions": default_actions, "loadBalancerArn": load_balancer_arn, "port": port, "protocol": protocol}

        if certificates is not None:
            props["certificates"] = certificates

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        jsii.create(CfnListener, self, [scope, id, props])

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
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        return jsii.get(self, "listenerArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnListenerProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ActionProperty(jsii.compat.TypedDict, total=False):
        authenticateCognitoConfig: typing.Union[aws_cdk.cdk.Token, "CfnListener.AuthenticateCognitoConfigProperty"]
        """``CfnListener.ActionProperty.AuthenticateCognitoConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-authenticatecognitoconfig
        """
        authenticateOidcConfig: typing.Union[aws_cdk.cdk.Token, "CfnListener.AuthenticateOidcConfigProperty"]
        """``CfnListener.ActionProperty.AuthenticateOidcConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-authenticateoidcconfig
        """
        fixedResponseConfig: typing.Union[aws_cdk.cdk.Token, "CfnListener.FixedResponseConfigProperty"]
        """``CfnListener.ActionProperty.FixedResponseConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-fixedresponseconfig
        """
        order: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnListener.ActionProperty.Order``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-order
        """
        redirectConfig: typing.Union[aws_cdk.cdk.Token, "CfnListener.RedirectConfigProperty"]
        """``CfnListener.ActionProperty.RedirectConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-action-redirectconfig
        """
        targetGroupArn: str
        """``CfnListener.ActionProperty.TargetGroupArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-defaultactions-targetgrouparn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.ActionProperty", jsii_struct_bases=[_ActionProperty])
    class ActionProperty(_ActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html
        """
        type: str
        """``CfnListener.ActionProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-defaultactions.html#cfn-elasticloadbalancingv2-listener-defaultactions-type
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _AuthenticateCognitoConfigProperty(jsii.compat.TypedDict, total=False):
        authenticationRequestExtraParams: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnListener.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-authenticationrequestextraparams
        """
        onUnauthenticatedRequest: str
        """``CfnListener.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-onunauthenticatedrequest
        """
        scope: str
        """``CfnListener.AuthenticateCognitoConfigProperty.Scope``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-scope
        """
        sessionCookieName: str
        """``CfnListener.AuthenticateCognitoConfigProperty.SessionCookieName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessioncookiename
        """
        sessionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnListener.AuthenticateCognitoConfigProperty.SessionTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessiontimeout
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.AuthenticateCognitoConfigProperty", jsii_struct_bases=[_AuthenticateCognitoConfigProperty])
    class AuthenticateCognitoConfigProperty(_AuthenticateCognitoConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html
        """
        userPoolArn: str
        """``CfnListener.AuthenticateCognitoConfigProperty.UserPoolArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolarn
        """

        userPoolClientId: str
        """``CfnListener.AuthenticateCognitoConfigProperty.UserPoolClientId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolclientid
        """

        userPoolDomain: str
        """``CfnListener.AuthenticateCognitoConfigProperty.UserPoolDomain``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpooldomain
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _AuthenticateOidcConfigProperty(jsii.compat.TypedDict, total=False):
        authenticationRequestExtraParams: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnListener.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authenticationrequestextraparams
        """
        onUnauthenticatedRequest: str
        """``CfnListener.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-onunauthenticatedrequest
        """
        scope: str
        """``CfnListener.AuthenticateOidcConfigProperty.Scope``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-scope
        """
        sessionCookieName: str
        """``CfnListener.AuthenticateOidcConfigProperty.SessionCookieName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessioncookiename
        """
        sessionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnListener.AuthenticateOidcConfigProperty.SessionTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessiontimeout
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.AuthenticateOidcConfigProperty", jsii_struct_bases=[_AuthenticateOidcConfigProperty])
    class AuthenticateOidcConfigProperty(_AuthenticateOidcConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html
        """
        authorizationEndpoint: str
        """``CfnListener.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authorizationendpoint
        """

        clientId: str
        """``CfnListener.AuthenticateOidcConfigProperty.ClientId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientid
        """

        clientSecret: str
        """``CfnListener.AuthenticateOidcConfigProperty.ClientSecret``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientsecret
        """

        issuer: str
        """``CfnListener.AuthenticateOidcConfigProperty.Issuer``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-issuer
        """

        tokenEndpoint: str
        """``CfnListener.AuthenticateOidcConfigProperty.TokenEndpoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-tokenendpoint
        """

        userInfoEndpoint: str
        """``CfnListener.AuthenticateOidcConfigProperty.UserInfoEndpoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-userinfoendpoint
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.CertificateProperty", jsii_struct_bases=[])
    class CertificateProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html
        """
        certificateArn: str
        """``CfnListener.CertificateProperty.CertificateArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html#cfn-elasticloadbalancingv2-listener-certificates-certificatearn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FixedResponseConfigProperty(jsii.compat.TypedDict, total=False):
        contentType: str
        """``CfnListener.FixedResponseConfigProperty.ContentType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-contenttype
        """
        messageBody: str
        """``CfnListener.FixedResponseConfigProperty.MessageBody``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-messagebody
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.FixedResponseConfigProperty", jsii_struct_bases=[_FixedResponseConfigProperty])
    class FixedResponseConfigProperty(_FixedResponseConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html
        """
        statusCode: str
        """``CfnListener.FixedResponseConfigProperty.StatusCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-statuscode
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RedirectConfigProperty(jsii.compat.TypedDict, total=False):
        host: str
        """``CfnListener.RedirectConfigProperty.Host``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-host
        """
        path: str
        """``CfnListener.RedirectConfigProperty.Path``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-path
        """
        port: str
        """``CfnListener.RedirectConfigProperty.Port``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-port
        """
        protocol: str
        """``CfnListener.RedirectConfigProperty.Protocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-protocol
        """
        query: str
        """``CfnListener.RedirectConfigProperty.Query``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-query
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListener.RedirectConfigProperty", jsii_struct_bases=[_RedirectConfigProperty])
    class RedirectConfigProperty(_RedirectConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html
        """
        statusCode: str
        """``CfnListener.RedirectConfigProperty.StatusCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-statuscode
        """


class CfnListenerCertificate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificate"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
    cloudformationResource:
        AWS::ElasticLoadBalancingV2::ListenerCertificate
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, certificates: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CertificateProperty"]]], listener_arn: str) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            certificates: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.
            listenerArn: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.
        """
        props: CfnListenerCertificateProps = {"certificates": certificates, "listenerArn": listener_arn}

        jsii.create(CfnListenerCertificate, self, [scope, id, props])

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
    @jsii.member(jsii_name="listenerCertificateArn")
    def listener_certificate_arn(self) -> str:
        return jsii.get(self, "listenerCertificateArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnListenerCertificateProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificate.CertificateProperty", jsii_struct_bases=[])
    class CertificateProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html
        """
        certificateArn: str
        """``CfnListenerCertificate.CertificateProperty.CertificateArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html#cfn-elasticloadbalancingv2-listener-certificates-certificatearn
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerCertificateProps", jsii_struct_bases=[])
class CfnListenerCertificateProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
    """
    certificates: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnListenerCertificate.CertificateProperty"]]]
    """``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-certificates
    """

    listenerArn: str
    """``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-listenerarn
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnListenerProps(jsii.compat.TypedDict, total=False):
    certificates: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnListener.CertificateProperty"]]]
    """``AWS::ElasticLoadBalancingV2::Listener.Certificates``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-certificates
    """
    sslPolicy: str
    """``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-sslpolicy
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerProps", jsii_struct_bases=[_CfnListenerProps])
class CfnListenerProps(_CfnListenerProps):
    """Properties for defining a ``AWS::ElasticLoadBalancingV2::Listener``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
    """
    defaultActions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnListener.ActionProperty", aws_cdk.cdk.Token]]]
    """``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-defaultactions
    """

    loadBalancerArn: str
    """``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-loadbalancerarn
    """

    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::ElasticLoadBalancingV2::Listener.Port``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-port
    """

    protocol: str
    """``AWS::ElasticLoadBalancingV2::Listener.Protocol``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-protocol
    """

class CfnListenerRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::ListenerRule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
    cloudformationResource:
        AWS::ElasticLoadBalancingV2::ListenerRule
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ActionProperty"]]], conditions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "RuleConditionProperty"]]], listener_arn: str, priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::ListenerRule``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            actions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.
            conditions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.
            listenerArn: ``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.
            priority: ``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.
        """
        props: CfnListenerRuleProps = {"actions": actions, "conditions": conditions, "listenerArn": listener_arn, "priority": priority}

        jsii.create(CfnListenerRule, self, [scope, id, props])

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
    @jsii.member(jsii_name="listenerRuleArn")
    def listener_rule_arn(self) -> str:
        return jsii.get(self, "listenerRuleArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnListenerRuleProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ActionProperty(jsii.compat.TypedDict, total=False):
        authenticateCognitoConfig: typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.AuthenticateCognitoConfigProperty"]
        """``CfnListenerRule.ActionProperty.AuthenticateCognitoConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticatecognitoconfig
        """
        authenticateOidcConfig: typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.AuthenticateOidcConfigProperty"]
        """``CfnListenerRule.ActionProperty.AuthenticateOidcConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticateoidcconfig
        """
        fixedResponseConfig: typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.FixedResponseConfigProperty"]
        """``CfnListenerRule.ActionProperty.FixedResponseConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-fixedresponseconfig
        """
        order: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnListenerRule.ActionProperty.Order``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-order
        """
        redirectConfig: typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.RedirectConfigProperty"]
        """``CfnListenerRule.ActionProperty.RedirectConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listenerrule-action-redirectconfig
        """
        targetGroupArn: str
        """``CfnListenerRule.ActionProperty.TargetGroupArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listener-actions-targetgrouparn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.ActionProperty", jsii_struct_bases=[_ActionProperty])
    class ActionProperty(_ActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html
        """
        type: str
        """``CfnListenerRule.ActionProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-actions.html#cfn-elasticloadbalancingv2-listener-actions-type
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _AuthenticateCognitoConfigProperty(jsii.compat.TypedDict, total=False):
        authenticationRequestExtraParams: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnListenerRule.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-authenticationrequestextraparams
        """
        onUnauthenticatedRequest: str
        """``CfnListenerRule.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-onunauthenticatedrequest
        """
        scope: str
        """``CfnListenerRule.AuthenticateCognitoConfigProperty.Scope``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-scope
        """
        sessionCookieName: str
        """``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionCookieName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessioncookiename
        """
        sessionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessiontimeout
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.AuthenticateCognitoConfigProperty", jsii_struct_bases=[_AuthenticateCognitoConfigProperty])
    class AuthenticateCognitoConfigProperty(_AuthenticateCognitoConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html
        """
        userPoolArn: str
        """``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolarn
        """

        userPoolClientId: str
        """``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolClientId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolclientid
        """

        userPoolDomain: str
        """``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolDomain``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpooldomain
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _AuthenticateOidcConfigProperty(jsii.compat.TypedDict, total=False):
        authenticationRequestExtraParams: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnListenerRule.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authenticationrequestextraparams
        """
        onUnauthenticatedRequest: str
        """``CfnListenerRule.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-onunauthenticatedrequest
        """
        scope: str
        """``CfnListenerRule.AuthenticateOidcConfigProperty.Scope``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-scope
        """
        sessionCookieName: str
        """``CfnListenerRule.AuthenticateOidcConfigProperty.SessionCookieName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessioncookiename
        """
        sessionTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnListenerRule.AuthenticateOidcConfigProperty.SessionTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessiontimeout
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.AuthenticateOidcConfigProperty", jsii_struct_bases=[_AuthenticateOidcConfigProperty])
    class AuthenticateOidcConfigProperty(_AuthenticateOidcConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html
        """
        authorizationEndpoint: str
        """``CfnListenerRule.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authorizationendpoint
        """

        clientId: str
        """``CfnListenerRule.AuthenticateOidcConfigProperty.ClientId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientid
        """

        clientSecret: str
        """``CfnListenerRule.AuthenticateOidcConfigProperty.ClientSecret``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientsecret
        """

        issuer: str
        """``CfnListenerRule.AuthenticateOidcConfigProperty.Issuer``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-issuer
        """

        tokenEndpoint: str
        """``CfnListenerRule.AuthenticateOidcConfigProperty.TokenEndpoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-tokenendpoint
        """

        userInfoEndpoint: str
        """``CfnListenerRule.AuthenticateOidcConfigProperty.UserInfoEndpoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-userinfoendpoint
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FixedResponseConfigProperty(jsii.compat.TypedDict, total=False):
        contentType: str
        """``CfnListenerRule.FixedResponseConfigProperty.ContentType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-contenttype
        """
        messageBody: str
        """``CfnListenerRule.FixedResponseConfigProperty.MessageBody``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-messagebody
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.FixedResponseConfigProperty", jsii_struct_bases=[_FixedResponseConfigProperty])
    class FixedResponseConfigProperty(_FixedResponseConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html
        """
        statusCode: str
        """``CfnListenerRule.FixedResponseConfigProperty.StatusCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-statuscode
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RedirectConfigProperty(jsii.compat.TypedDict, total=False):
        host: str
        """``CfnListenerRule.RedirectConfigProperty.Host``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-host
        """
        path: str
        """``CfnListenerRule.RedirectConfigProperty.Path``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-path
        """
        port: str
        """``CfnListenerRule.RedirectConfigProperty.Port``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-port
        """
        protocol: str
        """``CfnListenerRule.RedirectConfigProperty.Protocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-protocol
        """
        query: str
        """``CfnListenerRule.RedirectConfigProperty.Query``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-query
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.RedirectConfigProperty", jsii_struct_bases=[_RedirectConfigProperty])
    class RedirectConfigProperty(_RedirectConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html
        """
        statusCode: str
        """``CfnListenerRule.RedirectConfigProperty.StatusCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-statuscode
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRule.RuleConditionProperty", jsii_struct_bases=[])
    class RuleConditionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html
        """
        field: str
        """``CfnListenerRule.RuleConditionProperty.Field``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-conditions-field
        """

        values: typing.List[str]
        """``CfnListenerRule.RuleConditionProperty.Values``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-conditions.html#cfn-elasticloadbalancingv2-listenerrule-conditions-values
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnListenerRuleProps", jsii_struct_bases=[])
class CfnListenerRuleProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::ElasticLoadBalancingV2::ListenerRule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
    """
    actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.ActionProperty"]]]
    """``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-actions
    """

    conditions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnListenerRule.RuleConditionProperty"]]]
    """``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-conditions
    """

    listenerArn: str
    """``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-listenerarn
    """

    priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-priority
    """

class CfnLoadBalancer(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
    cloudformationResource:
        AWS::ElasticLoadBalancingV2::LoadBalancer
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ip_address_type: typing.Optional[str]=None, load_balancer_attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "LoadBalancerAttributeProperty"]]]]]=None, name: typing.Optional[str]=None, scheme: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, subnet_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "SubnetMappingProperty"]]]]]=None, subnets: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, type: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            ipAddressType: ``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.
            loadBalancerAttributes: ``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.
            name: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.
            scheme: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.
            securityGroups: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.
            subnetMappings: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.
            subnets: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.
            tags: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.
            type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.
        """
        props: CfnLoadBalancerProps = {}

        if ip_address_type is not None:
            props["ipAddressType"] = ip_address_type

        if load_balancer_attributes is not None:
            props["loadBalancerAttributes"] = load_balancer_attributes

        if name is not None:
            props["name"] = name

        if scheme is not None:
            props["scheme"] = scheme

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if subnet_mappings is not None:
            props["subnetMappings"] = subnet_mappings

        if subnets is not None:
            props["subnets"] = subnets

        if tags is not None:
            props["tags"] = tags

        if type is not None:
            props["type"] = type

        jsii.create(CfnLoadBalancer, self, [scope, id, props])

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
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        return jsii.get(self, "loadBalancerArn")

    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> str:
        """
        cloudformationAttribute:
            CanonicalHostedZoneID
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneId")

    @property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        """
        cloudformationAttribute:
            DNSName
        """
        return jsii.get(self, "loadBalancerDnsName")

    @property
    @jsii.member(jsii_name="loadBalancerFullName")
    def load_balancer_full_name(self) -> str:
        """
        cloudformationAttribute:
            LoadBalancerFullName
        """
        return jsii.get(self, "loadBalancerFullName")

    @property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> str:
        """
        cloudformationAttribute:
            LoadBalancerName
        """
        return jsii.get(self, "loadBalancerName")

    @property
    @jsii.member(jsii_name="loadBalancerSecurityGroups")
    def load_balancer_security_groups(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            SecurityGroups
        """
        return jsii.get(self, "loadBalancerSecurityGroups")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLoadBalancerProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer.LoadBalancerAttributeProperty", jsii_struct_bases=[])
    class LoadBalancerAttributeProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html
        """
        key: str
        """``CfnLoadBalancer.LoadBalancerAttributeProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes-key
        """

        value: str
        """``CfnLoadBalancer.LoadBalancerAttributeProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancer.SubnetMappingProperty", jsii_struct_bases=[])
    class SubnetMappingProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html
        """
        allocationId: str
        """``CfnLoadBalancer.SubnetMappingProperty.AllocationId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-allocationid
        """

        subnetId: str
        """``CfnLoadBalancer.SubnetMappingProperty.SubnetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-subnetid
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnLoadBalancerProps", jsii_struct_bases=[])
class CfnLoadBalancerProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
    """
    ipAddressType: str
    """``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-ipaddresstype
    """

    loadBalancerAttributes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.LoadBalancerAttributeProperty"]]]
    """``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes
    """

    name: str
    """``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-name
    """

    scheme: str
    """``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-scheme
    """

    securityGroups: typing.List[str]
    """``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-securitygroups
    """

    subnetMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLoadBalancer.SubnetMappingProperty"]]]
    """``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmappings
    """

    subnets: typing.List[str]
    """``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnets
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-tags
    """

    type: str
    """``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-type
    """

class CfnTargetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup"):
    """A CloudFormation ``AWS::ElasticLoadBalancingV2::TargetGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
    cloudformationResource:
        AWS::ElasticLoadBalancingV2::TargetGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, health_check_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, health_check_interval_seconds: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, health_check_path: typing.Optional[str]=None, health_check_port: typing.Optional[str]=None, health_check_protocol: typing.Optional[str]=None, health_check_timeout_seconds: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, healthy_threshold_count: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, matcher: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["MatcherProperty"]]]=None, name: typing.Optional[str]=None, port: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, protocol: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, target_group_attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "TargetGroupAttributeProperty"]]]]]=None, targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "TargetDescriptionProperty"]]]]]=None, target_type: typing.Optional[str]=None, unhealthy_threshold_count: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, vpc_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ElasticLoadBalancingV2::TargetGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            healthCheckEnabled: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.
            healthCheckIntervalSeconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.
            healthCheckPath: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.
            healthCheckPort: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.
            healthCheckProtocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.
            healthCheckTimeoutSeconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.
            healthyThresholdCount: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.
            matcher: ``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.
            name: ``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.
            port: ``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.
            protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.
            tags: ``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.
            targetGroupAttributes: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.
            targets: ``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.
            targetType: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.
            unhealthyThresholdCount: ``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.
            vpcId: ``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.
        """
        props: CfnTargetGroupProps = {}

        if health_check_enabled is not None:
            props["healthCheckEnabled"] = health_check_enabled

        if health_check_interval_seconds is not None:
            props["healthCheckIntervalSeconds"] = health_check_interval_seconds

        if health_check_path is not None:
            props["healthCheckPath"] = health_check_path

        if health_check_port is not None:
            props["healthCheckPort"] = health_check_port

        if health_check_protocol is not None:
            props["healthCheckProtocol"] = health_check_protocol

        if health_check_timeout_seconds is not None:
            props["healthCheckTimeoutSeconds"] = health_check_timeout_seconds

        if healthy_threshold_count is not None:
            props["healthyThresholdCount"] = healthy_threshold_count

        if matcher is not None:
            props["matcher"] = matcher

        if name is not None:
            props["name"] = name

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if tags is not None:
            props["tags"] = tags

        if target_group_attributes is not None:
            props["targetGroupAttributes"] = target_group_attributes

        if targets is not None:
            props["targets"] = targets

        if target_type is not None:
            props["targetType"] = target_type

        if unhealthy_threshold_count is not None:
            props["unhealthyThresholdCount"] = unhealthy_threshold_count

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        jsii.create(CfnTargetGroup, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTargetGroupProps":
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

    @property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        return jsii.get(self, "targetGroupArn")

    @property
    @jsii.member(jsii_name="targetGroupFullName")
    def target_group_full_name(self) -> str:
        """
        cloudformationAttribute:
            TargetGroupFullName
        """
        return jsii.get(self, "targetGroupFullName")

    @property
    @jsii.member(jsii_name="targetGroupLoadBalancerArns")
    def target_group_load_balancer_arns(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            LoadBalancerArns
        """
        return jsii.get(self, "targetGroupLoadBalancerArns")

    @property
    @jsii.member(jsii_name="targetGroupName")
    def target_group_name(self) -> str:
        """
        cloudformationAttribute:
            TargetGroupName
        """
        return jsii.get(self, "targetGroupName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.MatcherProperty", jsii_struct_bases=[])
    class MatcherProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html
        """
        httpCode: str
        """``CfnTargetGroup.MatcherProperty.HttpCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html#cfn-elasticloadbalancingv2-targetgroup-matcher-httpcode
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TargetDescriptionProperty(jsii.compat.TypedDict, total=False):
        availabilityZone: str
        """``CfnTargetGroup.TargetDescriptionProperty.AvailabilityZone``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-availabilityzone
        """
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnTargetGroup.TargetDescriptionProperty.Port``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-port
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.TargetDescriptionProperty", jsii_struct_bases=[_TargetDescriptionProperty])
    class TargetDescriptionProperty(_TargetDescriptionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html
        """
        id: str
        """``CfnTargetGroup.TargetDescriptionProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-id
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroup.TargetGroupAttributeProperty", jsii_struct_bases=[])
    class TargetGroupAttributeProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html
        """
        key: str
        """``CfnTargetGroup.TargetGroupAttributeProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-key
        """

        value: str
        """``CfnTargetGroup.TargetGroupAttributeProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-value
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.CfnTargetGroupProps", jsii_struct_bases=[])
class CfnTargetGroupProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::ElasticLoadBalancingV2::TargetGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
    """
    healthCheckEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckenabled
    """

    healthCheckIntervalSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckintervalseconds
    """

    healthCheckPath: str
    """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckpath
    """

    healthCheckPort: str
    """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckport
    """

    healthCheckProtocol: str
    """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckprotocol
    """

    healthCheckTimeoutSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthchecktimeoutseconds
    """

    healthyThresholdCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthythresholdcount
    """

    matcher: typing.Union[aws_cdk.cdk.Token, "CfnTargetGroup.MatcherProperty"]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-matcher
    """

    name: str
    """``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-name
    """

    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-port
    """

    protocol: str
    """``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocol
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-tags
    """

    targetGroupAttributes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTargetGroup.TargetGroupAttributeProperty"]]]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattributes
    """

    targets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTargetGroup.TargetDescriptionProperty"]]]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targets
    """

    targetType: str
    """``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targettype
    """

    unhealthyThresholdCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-unhealthythresholdcount
    """

    vpcId: str
    """``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-vpcid
    """

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ContentType")
class ContentType(enum.Enum):
    """The content type for a fixed response."""
    TEXT_PLAIN = "TEXT_PLAIN"
    TEXT_CSS = "TEXT_CSS"
    TEXT_HTML = "TEXT_HTML"
    APPLICATION_JAVASCRIPT = "APPLICATION_JAVASCRIPT"
    APPLICATION_JSON = "APPLICATION_JSON"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _FixedResponse(jsii.compat.TypedDict, total=False):
    contentType: "ContentType"
    """The content type.

    Default:
        text/plain
    """
    messageBody: str
    """The message.

    Default:
        no message
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.FixedResponse", jsii_struct_bases=[_FixedResponse])
class FixedResponse(_FixedResponse):
    """A fixed response."""
    statusCode: str
    """The HTTP response code (2XX, 4XX or 5XX)."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.AddFixedResponseProps", jsii_struct_bases=[AddRuleProps, FixedResponse])
class AddFixedResponseProps(AddRuleProps, FixedResponse, jsii.compat.TypedDict):
    """Properties for adding a fixed response to a listener."""
    pass

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HealthCheck", jsii_struct_bases=[])
class HealthCheck(jsii.compat.TypedDict, total=False):
    """Properties for configuring a health check."""
    healthyHttpCodes: str
    """HTTP code to use when checking for a successful response from a target.

    For Application Load Balancers, you can specify values between 200 and
    499, and the default value is 200. You can specify multiple values (for
    example, "200,202") or a range of values (for example, "200-299").
    """

    healthyThresholdCount: jsii.Number
    """The number of consecutive health checks successes required before considering an unhealthy target healthy.

    For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3.

    Default:
        5 for ALBs, 3 for NLBs
    """

    intervalSecs: jsii.Number
    """The approximate number of seconds between health checks for an individual target.

    Default:
        30
    """

    path: str
    """The ping path destination where Elastic Load Balancing sends health check requests.

    Default:
        /
    """

    port: str
    """The port that the load balancer uses when performing health checks on the targets.

    Default:
        'traffic-port'
    """

    protocol: "Protocol"
    """The protocol the load balancer uses when performing health checks on targets.

    The TCP protocol is supported only if the protocol of the target group
    is TCP.

    Default:
        HTTP for ALBs, TCP for NLBs
    """

    timeoutSeconds: jsii.Number
    """The amount of time, in seconds, during which no response from a target means a failed health check.

    For Application Load Balancers, the range is 2–60 seconds and the
    default is 5 seconds. For Network Load Balancers, this is 10 seconds for
    TCP and HTTPS health checks and 6 seconds for HTTP health checks.

    Default:
        5 for ALBs, 10 or 6 for NLBs
    """

    unhealthyThresholdCount: jsii.Number
    """The number of consecutive health check failures required before considering a target unhealthy.

    For Application Load Balancers, the default is 2. For Network Load
    Balancers, this value must be the same as the healthy threshold count.

    Default:
        2
    """

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HttpCodeElb")
class HttpCodeElb(enum.Enum):
    """Count of HTTP status originating from the load balancer.

    This count does not include any response codes generated by the targets.
    """
    Elb3xxCount = "Elb3xxCount"
    """The number of HTTP 3XX redirection codes that originate from the load balancer."""
    Elb4xxCount = "Elb4xxCount"
    """The number of HTTP 4XX client error codes that originate from the load balancer.

    Client errors are generated when requests are malformed or incomplete.
    These requests have not been received by the target. This count does not
    include any response codes generated by the targets.
    """
    Elb5xxCount = "Elb5xxCount"
    """The number of HTTP 5XX server error codes that originate from the load balancer."""

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.HttpCodeTarget")
class HttpCodeTarget(enum.Enum):
    """Count of HTTP status originating from the targets."""
    Target2xxCount = "Target2xxCount"
    """The number of 2xx response codes from targets."""
    Target3xxCount = "Target3xxCount"
    """The number of 3xx response codes from targets."""
    Target4xxCount = "Target4xxCount"
    """The number of 4xx response codes from targets."""
    Target5xxCount = "Target5xxCount"
    """The number of 5xx response codes from targets."""

@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationListener")
class IApplicationListener(aws_cdk.cdk.IResource, aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    """Properties to reference an existing listener."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IApplicationListenerProxy

    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """ARN of the listener.

        attribute:
            true
        """
        ...

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(self, id: str, arns: typing.List[str]) -> None:
        """Add one or more certificates to this listener.

        Arguments:
            id: -
            arns: -
        """
        ...

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, id: str, *, target_groups: typing.List["IApplicationTargetGroup"], host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        Arguments:
            id: -
            props: -
            targetGroups: Target groups to forward requests to.
            hostHeader: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
            pathPattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
            priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        ...

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start_sec: typing.Optional[jsii.Number]=None, stickiness_cookie_duration_sec: typing.Optional[jsii.Number]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ApplicationTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        Arguments:
            id: -
            props: -
            deregistrationDelaySec: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0–3600 seconds. Default: 300
            healthCheck: Health check configuration. Default: No health check
            port: The port on which the listener listens for requests. Default: Determined from protocol if known
            protocol: The protocol to use. Default: Determined from port if known
            slowStartSec: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30–900 seconds (15 minutes). Default: 0
            stickinessCookieDurationSec: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: 86400 (1 day)
            targetGroupName: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
            targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.
            hostHeader: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
            pathPattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
            priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        Returns:
            The newly created target group
        """
        ...

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: aws_cdk.aws_ec2.IPortRange) -> None:
        """Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        Arguments:
            connectable: -
            portRange: -
        """
        ...


class _IApplicationListenerProxy(jsii.proxy_for(aws_cdk.cdk.IResource), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    """Properties to reference an existing listener."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationListener"
    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """ARN of the listener.

        attribute:
            true
        """
        return jsii.get(self, "listenerArn")

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(self, id: str, arns: typing.List[str]) -> None:
        """Add one or more certificates to this listener.

        Arguments:
            id: -
            arns: -
        """
        return jsii.invoke(self, "addCertificateArns", [id, arns])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, id: str, *, target_groups: typing.List["IApplicationTargetGroup"], host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        Arguments:
            id: -
            props: -
            targetGroups: Target groups to forward requests to.
            hostHeader: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
            pathPattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
            priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        props: AddApplicationTargetGroupsProps = {"targetGroups": target_groups}

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if priority is not None:
            props["priority"] = priority

        return jsii.invoke(self, "addTargetGroups", [id, props])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start_sec: typing.Optional[jsii.Number]=None, stickiness_cookie_duration_sec: typing.Optional[jsii.Number]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ApplicationTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        Arguments:
            id: -
            props: -
            deregistrationDelaySec: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0–3600 seconds. Default: 300
            healthCheck: Health check configuration. Default: No health check
            port: The port on which the listener listens for requests. Default: Determined from protocol if known
            protocol: The protocol to use. Default: Determined from port if known
            slowStartSec: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30–900 seconds (15 minutes). Default: 0
            stickinessCookieDurationSec: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: 86400 (1 day)
            targetGroupName: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
            targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.
            hostHeader: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
            pathPattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
            priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        Returns:
            The newly created target group
        """
        props: AddApplicationTargetsProps = {}

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if slow_start_sec is not None:
            props["slowStartSec"] = slow_start_sec

        if stickiness_cookie_duration_sec is not None:
            props["stickinessCookieDurationSec"] = stickiness_cookie_duration_sec

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if targets is not None:
            props["targets"] = targets

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if priority is not None:
            props["priority"] = priority

        return jsii.invoke(self, "addTargets", [id, props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: aws_cdk.aws_ec2.IPortRange) -> None:
        """Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        Arguments:
            connectable: -
            portRange: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])


@jsii.implements(IApplicationListener)
class ApplicationListener(BaseListener, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationListener"):
    """Define an ApplicationListener.

    resource:
        AWS::ElasticLoadBalancingV2::Listener
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, load_balancer: "IApplicationLoadBalancer", certificate_arns: typing.Optional[typing.List[str]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            loadBalancer: The load balancer to attach this listener to.
            certificateArns: The certificates to use on this listener. Default: - No certificates.
            defaultTargetGroups: Default target groups to load balance to. Default: - None.
            open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
            port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
            protocol: The protocol to use. Default: - Determined from port if known.
            sslPolicy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        props: ApplicationListenerProps = {"loadBalancer": load_balancer}

        if certificate_arns is not None:
            props["certificateArns"] = certificate_arns

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        if open is not None:
            props["open"] = open

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        jsii.create(ApplicationListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationListenerAttributes")
    @classmethod
    def from_application_listener_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, listener_arn: str, security_group_id: str, default_port: typing.Optional[jsii.Number]=None) -> "IApplicationListener":
        """Import an existing listener.

        Arguments:
            scope: -
            id: -
            attrs: -
            listenerArn: ARN of the listener.
            securityGroupId: Security group ID of the load balancer this listener is associated with.
            defaultPort: The default port on which this listener is listening.
        """
        attrs: ApplicationListenerAttributes = {"listenerArn": listener_arn, "securityGroupId": security_group_id}

        if default_port is not None:
            attrs["defaultPort"] = default_port

        return jsii.sinvoke(cls, "fromApplicationListenerAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addCertificateArns")
    def add_certificate_arns(self, _id: str, arns: typing.List[str]) -> None:
        """Add one or more certificates to this listener.

        Arguments:
            _id: -
            arns: -
        """
        return jsii.invoke(self, "addCertificateArns", [_id, arns])

    @jsii.member(jsii_name="addFixedResponse")
    def add_fixed_response(self, id: str, *, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None, status_code: str, content_type: typing.Optional["ContentType"]=None, message_body: typing.Optional[str]=None) -> None:
        """Add a fixed response.

        Arguments:
            id: -
            props: -
            hostHeader: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
            pathPattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
            priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
            statusCode: The HTTP response code (2XX, 4XX or 5XX).
            contentType: The content type. Default: text/plain
            messageBody: The message. Default: no message
        """
        props: AddFixedResponseProps = {"statusCode": status_code}

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if priority is not None:
            props["priority"] = priority

        if content_type is not None:
            props["contentType"] = content_type

        if message_body is not None:
            props["messageBody"] = message_body

        return jsii.invoke(self, "addFixedResponse", [id, props])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, id: str, *, target_groups: typing.List["IApplicationTargetGroup"], host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> None:
        """Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        Arguments:
            id: -
            props: -
            targetGroups: Target groups to forward requests to.
            hostHeader: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
            pathPattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
            priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        props: AddApplicationTargetGroupsProps = {"targetGroups": target_groups}

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if priority is not None:
            props["priority"] = priority

        return jsii.invoke(self, "addTargetGroups", [id, props])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start_sec: typing.Optional[jsii.Number]=None, stickiness_cookie_duration_sec: typing.Optional[jsii.Number]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ApplicationTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        Arguments:
            id: -
            props: -
            deregistrationDelaySec: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0–3600 seconds. Default: 300
            healthCheck: Health check configuration. Default: No health check
            port: The port on which the listener listens for requests. Default: Determined from protocol if known
            protocol: The protocol to use. Default: Determined from port if known
            slowStartSec: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30–900 seconds (15 minutes). Default: 0
            stickinessCookieDurationSec: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: 86400 (1 day)
            targetGroupName: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
            targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.
            hostHeader: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
            pathPattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
            priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        Returns:
            The newly created target group
        """
        props: AddApplicationTargetsProps = {}

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if slow_start_sec is not None:
            props["slowStartSec"] = slow_start_sec

        if stickiness_cookie_duration_sec is not None:
            props["stickinessCookieDurationSec"] = stickiness_cookie_duration_sec

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if targets is not None:
            props["targets"] = targets

        if host_header is not None:
            props["hostHeader"] = host_header

        if path_pattern is not None:
            props["pathPattern"] = path_pattern

        if priority is not None:
            props["priority"] = priority

        return jsii.invoke(self, "addTargets", [id, props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: aws_cdk.aws_ec2.IPortRange) -> None:
        """Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        Arguments:
            connectable: -
            portRange: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate this listener."""
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage connections to this ApplicationListener."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "IApplicationLoadBalancer":
        """Load balancer this listener is associated with."""
        return jsii.get(self, "loadBalancer")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancerTarget")
class IApplicationLoadBalancerTarget(jsii.compat.Protocol):
    """Interface for constructs that can be targets of an application load balancer."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IApplicationLoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "ApplicationTargetGroup") -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        Arguments:
            targetGroup: -
        """
        ...


class _IApplicationLoadBalancerTargetProxy():
    """Interface for constructs that can be targets of an application load balancer."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancerTarget"
    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "ApplicationTargetGroup") -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        Arguments:
            targetGroup: -
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ILoadBalancerV2")
class ILoadBalancerV2(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ILoadBalancerV2Proxy

    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> str:
        """The canonical hosted zone ID of this load balancer.

        attribute:
            true

        Example::
            Z2P70J7EXAMPLE
        """
        ...

    @property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        """The DNS name of this load balancer.

        attribute:
            true

        Example::
            my-load-balancer-424835706.us-west-2.elb.amazonaws.com
        """
        ...


class _ILoadBalancerV2Proxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.ILoadBalancerV2"
    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> str:
        """The canonical hosted zone ID of this load balancer.

        attribute:
            true

        Example::
            Z2P70J7EXAMPLE
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneId")

    @property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        """The DNS name of this load balancer.

        attribute:
            true

        Example::
            my-load-balancer-424835706.us-west-2.elb.amazonaws.com
        """
        return jsii.get(self, "loadBalancerDnsName")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancer")
class IApplicationLoadBalancer(ILoadBalancerV2, aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    """An application load balancer."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IApplicationLoadBalancerProxy

    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        """The ARN of this load balancer."""
        ...

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, certificate_arns: typing.Optional[typing.List[str]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "ApplicationListener":
        """Add a new listener to this load balancer.

        Arguments:
            id: -
            props: -
            certificateArns: The certificates to use on this listener. Default: - No certificates.
            defaultTargetGroups: Default target groups to load balance to. Default: - None.
            open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
            port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
            protocol: The protocol to use. Default: - Determined from port if known.
            sslPolicy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        ...


class _IApplicationLoadBalancerProxy(jsii.proxy_for(ILoadBalancerV2), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    """An application load balancer."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationLoadBalancer"
    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        """The ARN of this load balancer."""
        return jsii.get(self, "loadBalancerArn")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        return jsii.get(self, "vpc")

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, certificate_arns: typing.Optional[typing.List[str]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "ApplicationListener":
        """Add a new listener to this load balancer.

        Arguments:
            id: -
            props: -
            certificateArns: The certificates to use on this listener. Default: - No certificates.
            defaultTargetGroups: Default target groups to load balance to. Default: - None.
            open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
            port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
            protocol: The protocol to use. Default: - Determined from port if known.
            sslPolicy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        props: BaseApplicationListenerProps = {}

        if certificate_arns is not None:
            props["certificateArns"] = certificate_arns

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        if open is not None:
            props["open"] = open

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        return jsii.invoke(self, "addListener", [id, props])


@jsii.implements(IApplicationLoadBalancer)
class ApplicationLoadBalancer(BaseLoadBalancer, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationLoadBalancer"):
    """Define an Application Load Balancer.

    resource:
        AWS::ElasticLoadBalancingV2::LoadBalancer
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, http2_enabled: typing.Optional[bool]=None, idle_timeout_secs: typing.Optional[jsii.Number]=None, ip_address_type: typing.Optional["IpAddressType"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc: aws_cdk.aws_ec2.IVpc, deletion_protection: typing.Optional[bool]=None, internet_facing: typing.Optional[bool]=None, load_balancer_name: typing.Optional[str]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            http2Enabled: Indicates whether HTTP/2 is enabled. Default: true
            idleTimeoutSecs: The load balancer idle timeout, in seconds. Default: 60
            ipAddressType: The type of IP addresses to use. Only applies to application load balancers. Default: IpAddressType.Ipv4
            securityGroup: Security group to associate with this load balancer. Default: A security group is created
            vpc: The VPC network to place the load balancer in.
            deletionProtection: Indicates whether deletion protection is enabled. Default: false
            internetFacing: Whether the load balancer has an internet-routable address. Default: false
            loadBalancerName: Name of the load balancer. Default: - Automatically generated name.
            vpcSubnets: Where in the VPC to place the load balancer. Default: - Public subnets if internetFacing, otherwise private subnets.
        """
        props: ApplicationLoadBalancerProps = {"vpc": vpc}

        if http2_enabled is not None:
            props["http2Enabled"] = http2_enabled

        if idle_timeout_secs is not None:
            props["idleTimeoutSecs"] = idle_timeout_secs

        if ip_address_type is not None:
            props["ipAddressType"] = ip_address_type

        if security_group is not None:
            props["securityGroup"] = security_group

        if deletion_protection is not None:
            props["deletionProtection"] = deletion_protection

        if internet_facing is not None:
            props["internetFacing"] = internet_facing

        if load_balancer_name is not None:
            props["loadBalancerName"] = load_balancer_name

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        jsii.create(ApplicationLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationLoadBalancerAttributes")
    @classmethod
    def from_application_load_balancer_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, load_balancer_arn: str, security_group_id: str, load_balancer_canonical_hosted_zone_id: typing.Optional[str]=None, load_balancer_dns_name: typing.Optional[str]=None) -> "IApplicationLoadBalancer":
        """Import an existing Application Load Balancer.

        Arguments:
            scope: -
            id: -
            attrs: -
            loadBalancerArn: ARN of the load balancer.
            securityGroupId: ID of the load balancer's security group.
            loadBalancerCanonicalHostedZoneId: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
            loadBalancerDnsName: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        attrs: ApplicationLoadBalancerAttributes = {"loadBalancerArn": load_balancer_arn, "securityGroupId": security_group_id}

        if load_balancer_canonical_hosted_zone_id is not None:
            attrs["loadBalancerCanonicalHostedZoneId"] = load_balancer_canonical_hosted_zone_id

        if load_balancer_dns_name is not None:
            attrs["loadBalancerDnsName"] = load_balancer_dns_name

        return jsii.sinvoke(cls, "fromApplicationLoadBalancerAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, certificate_arns: typing.Optional[typing.List[str]]=None, default_target_groups: typing.Optional[typing.List["IApplicationTargetGroup"]]=None, open: typing.Optional[bool]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "ApplicationListener":
        """Add a new listener to this load balancer.

        Arguments:
            id: -
            props: -
            certificateArns: The certificates to use on this listener. Default: - No certificates.
            defaultTargetGroups: Default target groups to load balance to. Default: - None.
            open: Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
            port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
            protocol: The protocol to use. Default: - Determined from port if known.
            sslPolicy: The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        """
        props: BaseApplicationListenerProps = {}

        if certificate_arns is not None:
            props["certificateArns"] = certificate_arns

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        if open is not None:
            props["open"] = open

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="logAccessLogs")
    def log_access_logs(self, bucket: aws_cdk.aws_s3.IBucket, prefix: typing.Optional[str]=None) -> None:
        """Enable access logging for this load balancer.

        Arguments:
            bucket: -
            prefix: -
        """
        return jsii.invoke(self, "logAccessLogs", [bucket, prefix])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Application Load Balancer.

        Arguments:
            metricName: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricActiveConnectionCount")
    def metric_active_connection_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of concurrent TCP connections active from clients to the load balancer and from the load balancer to targets.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricActiveConnectionCount", [props])

    @jsii.member(jsii_name="metricClientTlsNegotiationErrorCount")
    def metric_client_tls_negotiation_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of TLS connections initiated by the client that did not establish a session with the load balancer.

        Possible causes include a
        mismatch of ciphers or protocols.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricClientTlsNegotiationErrorCount", [props])

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of load balancer capacity units (LCU) used by your load balancer.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricConsumedLCUs", [props])

    @jsii.member(jsii_name="metricElbAuthError")
    def metric_elb_auth_error(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of user authentications that could not be completed.

        Because an authenticate action was misconfigured, the load balancer
        couldn't establish a connection with the IdP, or the load balancer
        couldn't complete the authentication flow due to an internal error.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricElbAuthError", [props])

    @jsii.member(jsii_name="metricElbAuthFailure")
    def metric_elb_auth_failure(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of user authentications that could not be completed because the IdP denied access to the user or an authorization code was used more than once.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricElbAuthFailure", [props])

    @jsii.member(jsii_name="metricElbAuthLatency")
    def metric_elb_auth_latency(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The time elapsed, in milliseconds, to query the IdP for the ID token and user info.

        If one or more of these operations fail, this is the time to failure.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricElbAuthLatency", [props])

    @jsii.member(jsii_name="metricElbAuthSuccess")
    def metric_elb_auth_success(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of authenticate actions that were successful.

        This metric is incremented at the end of the authentication workflow,
        after the load balancer has retrieved the user claims from the IdP.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricElbAuthSuccess", [props])

    @jsii.member(jsii_name="metricHttpCodeElb")
    def metric_http_code_elb(self, code: "HttpCodeElb", *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of HTTP 3xx/4xx/5xx codes that originate from the load balancer.

        This does not include any response codes generated by the targets.

        Arguments:
            code: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpCodeElb", [code, props])

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(self, code: "HttpCodeTarget", *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of HTTP 2xx/3xx/4xx/5xx response codes generated by all targets in the load balancer.

        This does not include any response codes generated by the load balancer.

        Arguments:
            code: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpCodeTarget", [code, props])

    @jsii.member(jsii_name="metricHttpFixedResponseCount")
    def metric_http_fixed_response_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of fixed-response actions that were successful.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpFixedResponseCount", [props])

    @jsii.member(jsii_name="metricHttpRedirectCount")
    def metric_http_redirect_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of redirect actions that were successful.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpRedirectCount", [props])

    @jsii.member(jsii_name="metricHttpRedirectUrlLimitExceededCount")
    def metric_http_redirect_url_limit_exceeded_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of redirect actions that couldn't be completed because the URL in the response location header is larger than 8K.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpRedirectUrlLimitExceededCount", [props])

    @jsii.member(jsii_name="metricIPv6ProcessedBytes")
    def metric_i_pv6_processed_bytes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of bytes processed by the load balancer over IPv6.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricIPv6ProcessedBytes", [props])

    @jsii.member(jsii_name="metricIPv6RequestCount")
    def metric_i_pv6_request_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of IPv6 requests received by the load balancer.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricIPv6RequestCount", [props])

    @jsii.member(jsii_name="metricNewConnectionCount")
    def metric_new_connection_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of new TCP connections established from clients to the load balancer and from the load balancer to targets.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricNewConnectionCount", [props])

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of bytes processed by the load balancer over IPv4 and IPv6.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricProcessedBytes", [props])

    @jsii.member(jsii_name="metricRejectedConnectionCount")
    def metric_rejected_connection_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of connections that were rejected because the load balancer had reached its maximum number of connections.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRejectedConnectionCount", [props])

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of requests processed over IPv4 and IPv6.

        This count includes only the requests with a response generated by a target of the load balancer.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRequestCount", [props])

    @jsii.member(jsii_name="metricRuleEvaluations")
    def metric_rule_evaluations(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of rules processed by the load balancer given a request rate averaged over an hour.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRuleEvaluations", [props])

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of connections that were not successfully established between the load balancer and target.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetConnectionErrorCount", [props])

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The time elapsed, in seconds, after the request leaves the load balancer until a response from the target is received.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetResponseTime", [props])

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of TLS connections initiated by the load balancer that did not establish a session with the target.

        Possible causes include a mismatch of ciphers or protocols.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkListener")
class INetworkListener(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    """Properties to reference an existing listener."""
    @staticmethod
    def __jsii_proxy_class__():
        return _INetworkListenerProxy

    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """ARN of the listener.

        attribute:
            true
        """
        ...


class _INetworkListenerProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    """Properties to reference an existing listener."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkListener"
    @property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """ARN of the listener.

        attribute:
            true
        """
        return jsii.get(self, "listenerArn")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkListenerCertificateProps")
class INetworkListenerCertificateProps(jsii.compat.Protocol):
    """Properties for adding a certificate to a listener."""
    @staticmethod
    def __jsii_proxy_class__():
        return _INetworkListenerCertificatePropsProxy

    @property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """Certificate ARN from ACM."""
        ...


class _INetworkListenerCertificatePropsProxy():
    """Properties for adding a certificate to a listener."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkListenerCertificateProps"
    @property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """Certificate ARN from ACM."""
        return jsii.get(self, "certificateArn")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancer")
class INetworkLoadBalancer(ILoadBalancerV2, jsii.compat.Protocol):
    """A network load balancer."""
    @staticmethod
    def __jsii_proxy_class__():
        return _INetworkLoadBalancerProxy

    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        """The ARN of this load balancer."""
        ...

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, port: jsii.Number, certificates: typing.Optional[typing.List["INetworkListenerCertificateProps"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "NetworkListener":
        """Add a listener to this load balancer.

        Arguments:
            id: -
            props: -
            port: The port on which the listener listens for requests.
            certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
            defaultTargetGroups: Default target groups to load balance to. Default: - None.
            protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
            sslPolicy: SSL Policy. Default: - Current predefined security policy.

        Returns:
            The newly created listener
        """
        ...


class _INetworkLoadBalancerProxy(jsii.proxy_for(ILoadBalancerV2)):
    """A network load balancer."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancer"
    @property
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> str:
        """The ARN of this load balancer."""
        return jsii.get(self, "loadBalancerArn")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC this load balancer has been created in (if available)."""
        return jsii.get(self, "vpc")

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, port: jsii.Number, certificates: typing.Optional[typing.List["INetworkListenerCertificateProps"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "NetworkListener":
        """Add a listener to this load balancer.

        Arguments:
            id: -
            props: -
            port: The port on which the listener listens for requests.
            certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
            defaultTargetGroups: Default target groups to load balance to. Default: - None.
            protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
            sslPolicy: SSL Policy. Default: - Current predefined security policy.

        Returns:
            The newly created listener
        """
        props: BaseNetworkListenerProps = {"port": port}

        if certificates is not None:
            props["certificates"] = certificates

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        if protocol is not None:
            props["protocol"] = protocol

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        return jsii.invoke(self, "addListener", [id, props])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancerTarget")
class INetworkLoadBalancerTarget(jsii.compat.Protocol):
    """Interface for constructs that can be targets of an network load balancer."""
    @staticmethod
    def __jsii_proxy_class__():
        return _INetworkLoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "NetworkTargetGroup") -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        Arguments:
            targetGroup: -
        """
        ...


class _INetworkLoadBalancerTargetProxy():
    """Interface for constructs that can be targets of an network load balancer."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkLoadBalancerTarget"
    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "NetworkTargetGroup") -> "LoadBalancerTargetProps":
        """Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        Arguments:
            targetGroup: -
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ITargetGroup")
class ITargetGroup(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    """A target group."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ITargetGroupProxy

    @property
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> str:
        """A token representing a list of ARNs of the load balancers that route traffic to this target group."""
        ...

    @property
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.cdk.IDependable:
        """Return an object to depend on the listeners added to this target group."""
        ...

    @property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        """ARN of the target group."""
        ...


class _ITargetGroupProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    """A target group."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.ITargetGroup"
    @property
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> str:
        """A token representing a list of ARNs of the load balancers that route traffic to this target group."""
        return jsii.get(self, "loadBalancerArns")

    @property
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.cdk.IDependable:
        """Return an object to depend on the listeners added to this target group."""
        return jsii.get(self, "loadBalancerAttached")

    @property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        """ARN of the target group."""
        return jsii.get(self, "targetGroupArn")


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IApplicationTargetGroup")
class IApplicationTargetGroup(ITargetGroup, jsii.compat.Protocol):
    """A Target Group for Application Load Balancers."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IApplicationTargetGroupProxy

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "IApplicationListener", associating_construct: typing.Optional[aws_cdk.cdk.IConstruct]=None) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        Arguments:
            listener: -
            associatingConstruct: -
        """
        ...


class _IApplicationTargetGroupProxy(jsii.proxy_for(ITargetGroup)):
    """A Target Group for Application Load Balancers."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.IApplicationTargetGroup"
    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "IApplicationListener", associating_construct: typing.Optional[aws_cdk.cdk.IConstruct]=None) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        Arguments:
            listener: -
            associatingConstruct: -
        """
        return jsii.invoke(self, "registerListener", [listener, associating_construct])


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.INetworkTargetGroup")
class INetworkTargetGroup(ITargetGroup, jsii.compat.Protocol):
    """A network target group."""
    @staticmethod
    def __jsii_proxy_class__():
        return _INetworkTargetGroupProxy

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "INetworkListener") -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        Arguments:
            listener: -
        """
        ...


class _INetworkTargetGroupProxy(jsii.proxy_for(ITargetGroup)):
    """A network target group."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancingv2.INetworkTargetGroup"
    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "INetworkListener") -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        Arguments:
            listener: -
        """
        return jsii.invoke(self, "registerListener", [listener])


@jsii.implements(IApplicationLoadBalancerTarget, INetworkLoadBalancerTarget)
class InstanceTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.InstanceTarget"):
    """An EC2 instance that is the target for load balancing.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can connect to the instance.
    """
    def __init__(self, instance_id: str, port: typing.Optional[jsii.Number]=None) -> None:
        """Create a new Instance target.

        Arguments:
            instanceId: Instance ID of the instance to register to.
            port: Override the default port for the target group.
        """
        jsii.create(InstanceTarget, self, [instance_id, port])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "ApplicationTargetGroup") -> "LoadBalancerTargetProps":
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        Arguments:
            targetGroup: -
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "NetworkTargetGroup") -> "LoadBalancerTargetProps":
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        Arguments:
            targetGroup: -
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        """Instance ID of the instance to register to."""
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """Override the default port for the target group."""
        return jsii.get(self, "port")


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IpAddressType")
class IpAddressType(enum.Enum):
    """What kind of addresses to allocate to the load balancer."""
    Ipv4 = "Ipv4"
    """Allocate IPv4 addresses."""
    DualStack = "DualStack"
    """Allocate both IPv4 and IPv6 addresses."""

@jsii.implements(IApplicationLoadBalancerTarget, INetworkLoadBalancerTarget)
class IpTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.IpTarget"):
    """An IP address that is a target for load balancing.

    Specify IP addresses from the subnets of the virtual private cloud (VPC) for
    the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and
    192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify
    publicly routable IP addresses.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can send packets to the IP address.
    """
    def __init__(self, ip_address: str, port: typing.Optional[jsii.Number]=None, availability_zone: typing.Optional[str]=None) -> None:
        """Create a new IPAddress target.

        The availabilityZone parameter determines whether the target receives
        traffic from the load balancer nodes in the specified Availability Zone
        or from all enabled Availability Zones for the load balancer.

        This parameter is not supported if the target type of the target group
        is instance. If the IP address is in a subnet of the VPC for the target
        group, the Availability Zone is automatically detected and this
        parameter is optional. If the IP address is outside the VPC, this
        parameter is required.

        With an Application Load Balancer, if the IP address is outside the VPC
        for the target group, the only supported value is all.

        Default is automatic.

        Arguments:
            ipAddress: The IP Address to load balance to.
            port: Override the group's default port.
            availabilityZone: Availability zone to send traffic from.
        """
        jsii.create(IpTarget, self, [ip_address, port, availability_zone])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: "ApplicationTargetGroup") -> "LoadBalancerTargetProps":
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        Arguments:
            targetGroup: -
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: "NetworkTargetGroup") -> "LoadBalancerTargetProps":
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        Arguments:
            targetGroup: -
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> str:
        """The IP Address to load balance to."""
        return jsii.get(self, "ipAddress")

    @property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[str]:
        """Availability zone to send traffic from."""
        return jsii.get(self, "availabilityZone")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """Override the group's default port."""
        return jsii.get(self, "port")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _LoadBalancerTargetProps(jsii.compat.TypedDict, total=False):
    targetJson: typing.Any
    """JSON representing the target's direct addition to the TargetGroup list.

    May be omitted if the target is going to register itself later.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.LoadBalancerTargetProps", jsii_struct_bases=[_LoadBalancerTargetProps])
class LoadBalancerTargetProps(_LoadBalancerTargetProps):
    """Result of attaching a target to load balancer."""
    targetType: "TargetType"
    """What kind of target this is."""

@jsii.implements(INetworkListener)
class NetworkListener(BaseListener, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListener"):
    """Define a Network Listener.

    resource:
        AWS::ElasticLoadBalancingV2::Listener
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, load_balancer: "INetworkLoadBalancer", port: jsii.Number, certificates: typing.Optional[typing.List["INetworkListenerCertificateProps"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            loadBalancer: The load balancer to attach this listener to.
            port: The port on which the listener listens for requests.
            certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
            defaultTargetGroups: Default target groups to load balance to. Default: - None.
            protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
            sslPolicy: SSL Policy. Default: - Current predefined security policy.
        """
        props: NetworkListenerProps = {"loadBalancer": load_balancer, "port": port}

        if certificates is not None:
            props["certificates"] = certificates

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        if protocol is not None:
            props["protocol"] = protocol

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        jsii.create(NetworkListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromNetworkListenerArn")
    @classmethod
    def from_network_listener_arn(cls, scope: aws_cdk.cdk.Construct, id: str, network_listener_arn: str) -> "INetworkListener":
        """Import an existing listener.

        Arguments:
            scope: -
            id: -
            networkListenerArn: -
        """
        return jsii.sinvoke(cls, "fromNetworkListenerArn", [scope, id, network_listener_arn])

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(self, _id: str, *target_groups: "INetworkTargetGroup") -> None:
        """Load balance incoming requests to the given target groups.

        Arguments:
            _id: -
            targetGroups: -
        """
        return jsii.invoke(self, "addTargetGroups", [_id, target_groups])

    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, *, port: jsii.Number, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, proxy_protocol_v2: typing.Optional[bool]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List["INetworkLoadBalancerTarget"]]=None) -> "NetworkTargetGroup":
        """Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        Arguments:
            id: -
            props: -
            port: The port on which the listener listens for requests. Default: Determined from protocol if known
            deregistrationDelaySec: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
            healthCheck: Health check configuration. Default: No health check
            proxyProtocolV2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
            targetGroupName: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
            targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.

        Returns:
            The newly created target group
        """
        props: AddNetworkTargetsProps = {"port": port}

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if proxy_protocol_v2 is not None:
            props["proxyProtocolV2"] = proxy_protocol_v2

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if targets is not None:
            props["targets"] = targets

        return jsii.invoke(self, "addTargets", [id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkListenerProps", jsii_struct_bases=[BaseNetworkListenerProps])
class NetworkListenerProps(BaseNetworkListenerProps, jsii.compat.TypedDict):
    """Properties for a Network Listener attached to a Load Balancer."""
    loadBalancer: "INetworkLoadBalancer"
    """The load balancer to attach this listener to."""

@jsii.implements(INetworkLoadBalancer)
class NetworkLoadBalancer(BaseLoadBalancer, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancer"):
    """Define a new network load balancer.

    resource:
        AWS::ElasticLoadBalancingV2::LoadBalancer
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cross_zone_enabled: typing.Optional[bool]=None, vpc: aws_cdk.aws_ec2.IVpc, deletion_protection: typing.Optional[bool]=None, internet_facing: typing.Optional[bool]=None, load_balancer_name: typing.Optional[str]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            crossZoneEnabled: Indicates whether cross-zone load balancing is enabled. Default: false
            vpc: The VPC network to place the load balancer in.
            deletionProtection: Indicates whether deletion protection is enabled. Default: false
            internetFacing: Whether the load balancer has an internet-routable address. Default: false
            loadBalancerName: Name of the load balancer. Default: - Automatically generated name.
            vpcSubnets: Where in the VPC to place the load balancer. Default: - Public subnets if internetFacing, otherwise private subnets.
        """
        props: NetworkLoadBalancerProps = {"vpc": vpc}

        if cross_zone_enabled is not None:
            props["crossZoneEnabled"] = cross_zone_enabled

        if deletion_protection is not None:
            props["deletionProtection"] = deletion_protection

        if internet_facing is not None:
            props["internetFacing"] = internet_facing

        if load_balancer_name is not None:
            props["loadBalancerName"] = load_balancer_name

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        jsii.create(NetworkLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="fromNetworkLoadBalancerAttributes")
    @classmethod
    def from_network_load_balancer_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, load_balancer_arn: str, load_balancer_canonical_hosted_zone_id: typing.Optional[str]=None, load_balancer_dns_name: typing.Optional[str]=None) -> "INetworkLoadBalancer":
        """
        Arguments:
            scope: -
            id: -
            attrs: -
            loadBalancerArn: ARN of the load balancer.
            loadBalancerCanonicalHostedZoneId: The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
            loadBalancerDnsName: The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        """
        attrs: NetworkLoadBalancerAttributes = {"loadBalancerArn": load_balancer_arn}

        if load_balancer_canonical_hosted_zone_id is not None:
            attrs["loadBalancerCanonicalHostedZoneId"] = load_balancer_canonical_hosted_zone_id

        if load_balancer_dns_name is not None:
            attrs["loadBalancerDnsName"] = load_balancer_dns_name

        return jsii.sinvoke(cls, "fromNetworkLoadBalancerAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addListener")
    def add_listener(self, id: str, *, port: jsii.Number, certificates: typing.Optional[typing.List["INetworkListenerCertificateProps"]]=None, default_target_groups: typing.Optional[typing.List["INetworkTargetGroup"]]=None, protocol: typing.Optional["Protocol"]=None, ssl_policy: typing.Optional["SslPolicy"]=None) -> "NetworkListener":
        """Add a listener to this load balancer.

        Arguments:
            id: -
            props: -
            port: The port on which the listener listens for requests.
            certificates: Certificate list of ACM cert ARNs. Default: - No certificates.
            defaultTargetGroups: Default target groups to load balance to. Default: - None.
            protocol: Protocol for listener, expects TCP or TLS. Default: - TLS if certificates are provided. TCP otherwise.
            sslPolicy: SSL Policy. Default: - Current predefined security policy.

        Returns:
            The newly created listener
        """
        props: BaseNetworkListenerProps = {"port": port}

        if certificates is not None:
            props["certificates"] = certificates

        if default_target_groups is not None:
            props["defaultTargetGroups"] = default_target_groups

        if protocol is not None:
            props["protocol"] = protocol

        if ssl_policy is not None:
            props["sslPolicy"] = ssl_policy

        return jsii.invoke(self, "addListener", [id, props])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Network Load Balancer.

        Arguments:
            metricName: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricActiveFlowCount")
    def metric_active_flow_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of concurrent TCP flows (or connections) from clients to targets.

        This metric includes connections in the SYN_SENT and ESTABLISHED states.
        TCP connections are not terminated at the load balancer, so a client
        opening a TCP connection to a target counts as a single flow.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricActiveFlowCount", [props])

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of load balancer capacity units (LCU) used by your load balancer.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricConsumedLCUs", [props])

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of targets that are considered healthy.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHealthyHostCount", [props])

    @jsii.member(jsii_name="metricNewFlowCount")
    def metric_new_flow_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of new TCP flows (or connections) established from clients to targets in the time period.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricNewFlowCount", [props])

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of bytes processed by the load balancer, including TCP/IP headers.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricProcessedBytes", [props])

    @jsii.member(jsii_name="metricTcpClientResetCount")
    def metric_tcp_client_reset_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of reset (RST) packets sent from a client to a target.

        These resets are generated by the client and forwarded by the load balancer.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTcpClientResetCount", [props])

    @jsii.member(jsii_name="metricTcpElbResetCount")
    def metric_tcp_elb_reset_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of reset (RST) packets generated by the load balancer.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTcpElbResetCount", [props])

    @jsii.member(jsii_name="metricTcpTargetResetCount")
    def metric_tcp_target_reset_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The total number of reset (RST) packets sent from a target to a client.

        These resets are generated by the target and forwarded by the load balancer.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTcpTargetResetCount", [props])

    @jsii.member(jsii_name="metricUnHealthyHostCount")
    def metric_un_healthy_host_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of targets that are considered unhealthy.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricUnHealthyHostCount", [props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _NetworkLoadBalancerAttributes(jsii.compat.TypedDict, total=False):
    loadBalancerCanonicalHostedZoneId: str
    """The canonical hosted zone ID of this load balancer.

    Default:
        - When not provided, LB cannot be used as Route53 Alias target.
    """
    loadBalancerDnsName: str
    """The DNS name of this load balancer.

    Default:
        - When not provided, LB cannot be used as Route53 Alias target.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancerAttributes", jsii_struct_bases=[_NetworkLoadBalancerAttributes])
class NetworkLoadBalancerAttributes(_NetworkLoadBalancerAttributes):
    """Properties to reference an existing load balancer."""
    loadBalancerArn: str
    """ARN of the load balancer."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkLoadBalancerProps", jsii_struct_bases=[BaseLoadBalancerProps])
class NetworkLoadBalancerProps(BaseLoadBalancerProps, jsii.compat.TypedDict, total=False):
    """Properties for a network load balancer."""
    crossZoneEnabled: bool
    """Indicates whether cross-zone load balancing is enabled.

    Default:
        false
    """

@jsii.data_type_optionals(jsii_struct_bases=[BaseTargetGroupProps])
class _NetworkTargetGroupProps(BaseTargetGroupProps, jsii.compat.TypedDict, total=False):
    proxyProtocolV2: bool
    """Indicates whether Proxy Protocol version 2 is enabled.

    Default:
        false
    """
    targets: typing.List["INetworkLoadBalancerTarget"]
    """The targets to add to this target group.

    Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
    target. If you use either ``Instance`` or ``IPAddress`` as targets, all
    target must be of the same type.

    Default:
        - No targets.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkTargetGroupProps", jsii_struct_bases=[_NetworkTargetGroupProps])
class NetworkTargetGroupProps(_NetworkTargetGroupProps):
    """Properties for a new Network Target Group."""
    port: jsii.Number
    """The port on which the listener listens for requests."""

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.Protocol")
class Protocol(enum.Enum):
    """Backend protocol for health checks."""
    Http = "Http"
    """HTTP."""
    Https = "Https"
    """HTTPS."""
    Tcp = "Tcp"
    """TCP."""
    Tls = "Tls"
    """TLS."""

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.SslPolicy")
class SslPolicy(enum.Enum):
    """Elastic Load Balancing provides the following security policies for Application Load Balancers.

    We recommend the Recommended policy for general use. You can
    use the ForwardSecrecy policy if you require Forward Secrecy
    (FS).

    You can use one of the TLS policies to meet compliance and security
    standards that require disabling certain TLS protocol versions, or to
    support legacy clients that require deprecated ciphers.

    See:
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html
    """
    Recommended = "Recommended"
    """The recommended security policy."""
    ForwardSecrecy = "ForwardSecrecy"
    """Forward secrecy ciphers only."""
    TLS12 = "TLS12"
    """TLS1.2 only and no SHA ciphers."""
    TLS12Ext = "TLS12Ext"
    """TLS1.2 only with all ciphers."""
    TLS11 = "TLS11"
    """TLS1.1 and higher with all ciphers."""
    Legacy = "Legacy"
    """Support for DES-CBC3-SHA.

    Do not use this security policy unless you must support a legacy client
    that requires the DES-CBC3-SHA cipher, which is a weak cipher.
    """

@jsii.implements(ITargetGroup)
class TargetGroupBase(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupBase"):
    """Define the target of a load balancer."""
    @staticmethod
    def __jsii_proxy_class__():
        return _TargetGroupBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, base_props: "BaseTargetGroupProps", additional_props: typing.Any) -> None:
        """
        Arguments:
            scope: -
            id: -
            baseProps: -
            additionalProps: -
        """
        jsii.create(TargetGroupBase, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="addLoadBalancerTarget")
    def _add_load_balancer_target(self, *, target_type: "TargetType", target_json: typing.Any=None) -> None:
        """Register the given load balancing target as part of this group.

        Arguments:
            props: -
            targetType: What kind of target this is.
            targetJson: JSON representing the target's direct addition to the TargetGroup list. May be omitted if the target is going to register itself later.
        """
        props: LoadBalancerTargetProps = {"targetType": target_type}

        if target_json is not None:
            props["targetJson"] = target_json

        return jsii.invoke(self, "addLoadBalancerTarget", [props])

    @jsii.member(jsii_name="configureHealthCheck")
    def configure_health_check(self, *, healthy_http_codes: typing.Optional[str]=None, healthy_threshold_count: typing.Optional[jsii.Number]=None, interval_secs: typing.Optional[jsii.Number]=None, path: typing.Optional[str]=None, port: typing.Optional[str]=None, protocol: typing.Optional["Protocol"]=None, timeout_seconds: typing.Optional[jsii.Number]=None, unhealthy_threshold_count: typing.Optional[jsii.Number]=None) -> None:
        """Set/replace the target group's health check.

        Arguments:
            healthCheck: -
            healthyHttpCodes: HTTP code to use when checking for a successful response from a target. For Application Load Balancers, you can specify values between 200 and 499, and the default value is 200. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").
            healthyThresholdCount: The number of consecutive health checks successes required before considering an unhealthy target healthy. For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3. Default: 5 for ALBs, 3 for NLBs
            intervalSecs: The approximate number of seconds between health checks for an individual target. Default: 30
            path: The ping path destination where Elastic Load Balancing sends health check requests. Default: /
            port: The port that the load balancer uses when performing health checks on the targets. Default: 'traffic-port'
            protocol: The protocol the load balancer uses when performing health checks on targets. The TCP protocol is supported only if the protocol of the target group is TCP. Default: HTTP for ALBs, TCP for NLBs
            timeoutSeconds: The amount of time, in seconds, during which no response from a target means a failed health check. For Application Load Balancers, the range is 2–60 seconds and the default is 5 seconds. For Network Load Balancers, this is 10 seconds for TCP and HTTPS health checks and 6 seconds for HTTP health checks. Default: 5 for ALBs, 10 or 6 for NLBs
            unhealthyThresholdCount: The number of consecutive health check failures required before considering a target unhealthy. For Application Load Balancers, the default is 2. For Network Load Balancers, this value must be the same as the healthy threshold count. Default: 2
        """
        health_check: HealthCheck = {}

        if healthy_http_codes is not None:
            health_check["healthyHttpCodes"] = healthy_http_codes

        if healthy_threshold_count is not None:
            health_check["healthyThresholdCount"] = healthy_threshold_count

        if interval_secs is not None:
            health_check["intervalSecs"] = interval_secs

        if path is not None:
            health_check["path"] = path

        if port is not None:
            health_check["port"] = port

        if protocol is not None:
            health_check["protocol"] = protocol

        if timeout_seconds is not None:
            health_check["timeoutSeconds"] = timeout_seconds

        if unhealthy_threshold_count is not None:
            health_check["unhealthyThresholdCount"] = unhealthy_threshold_count

        return jsii.invoke(self, "configureHealthCheck", [health_check])

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(self, key: str, value: typing.Optional[str]=None) -> None:
        """Set a non-standard attribute on the target group.

        Arguments:
            key: -
            value: -

        See:
            https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html#target-group-attributes
        """
        return jsii.invoke(self, "setAttribute", [key, value])

    @property
    @jsii.member(jsii_name="defaultPort")
    def _default_port(self) -> jsii.Number:
        """Default port configured for members of this target group."""
        return jsii.get(self, "defaultPort")

    @property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    @abc.abstractmethod
    def first_load_balancer_full_name(self) -> str:
        """Full name of first load balancer.

        This identifier is emitted as a dimensions of the metrics of this target
        group.

        Example::
            app/my-load-balancer/123456789
        """
        ...

    @property
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> str:
        """Health check for the members of this target group A token representing a list of ARNs of the load balancers that route traffic to this target group."""
        return jsii.get(self, "loadBalancerArns")

    @property
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> aws_cdk.cdk.IDependable:
        """List of constructs that need to be depended on to ensure the TargetGroup is associated to a load balancer."""
        return jsii.get(self, "loadBalancerAttached")

    @property
    @jsii.member(jsii_name="loadBalancerAttachedDependencies")
    def _load_balancer_attached_dependencies(self) -> aws_cdk.cdk.ConcreteDependable:
        """Configurable dependable with all resources that lead to load balancer attachment."""
        return jsii.get(self, "loadBalancerAttachedDependencies")

    @property
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> str:
        """The ARN of the target group."""
        return jsii.get(self, "targetGroupArn")

    @property
    @jsii.member(jsii_name="targetGroupFullName")
    def target_group_full_name(self) -> str:
        """The full name of the target group."""
        return jsii.get(self, "targetGroupFullName")

    @property
    @jsii.member(jsii_name="targetGroupLoadBalancerArns")
    def target_group_load_balancer_arns(self) -> typing.List[str]:
        """ARNs of load balancers load balancing to this TargetGroup."""
        return jsii.get(self, "targetGroupLoadBalancerArns")

    @property
    @jsii.member(jsii_name="targetGroupName")
    def target_group_name(self) -> str:
        """The name of the target group."""
        return jsii.get(self, "targetGroupName")

    @property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> "HealthCheck":
        return jsii.get(self, "healthCheck")

    @health_check.setter
    def health_check(self, value: "HealthCheck"):
        return jsii.set(self, "healthCheck", value)


class _TargetGroupBaseProxy(TargetGroupBase):
    @property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> str:
        """Full name of first load balancer.

        This identifier is emitted as a dimensions of the metrics of this target
        group.

        Example::
            app/my-load-balancer/123456789
        """
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.implements(IApplicationTargetGroup)
class ApplicationTargetGroup(TargetGroupBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.ApplicationTargetGroup"):
    """Define an Application Target Group."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["ApplicationProtocol"]=None, slow_start_sec: typing.Optional[jsii.Number]=None, stickiness_cookie_duration_sec: typing.Optional[jsii.Number]=None, targets: typing.Optional[typing.List["IApplicationLoadBalancerTarget"]]=None, vpc: aws_cdk.aws_ec2.IVpc, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, target_group_name: typing.Optional[str]=None, target_type: typing.Optional["TargetType"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
            protocol: The protocol to use. Default: - Determined from port if known.
            slowStartSec: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30–900 seconds (15 minutes). Default: 0
            stickinessCookieDurationSec: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: 86400 (1 day)
            targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
            vpc: The virtual private cloud (VPC).
            deregistrationDelaySec: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
            healthCheck: Health check configuration. Default: - None.
            targetGroupName: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
            targetType: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        """
        props: ApplicationTargetGroupProps = {"vpc": vpc}

        if port is not None:
            props["port"] = port

        if protocol is not None:
            props["protocol"] = protocol

        if slow_start_sec is not None:
            props["slowStartSec"] = slow_start_sec

        if stickiness_cookie_duration_sec is not None:
            props["stickinessCookieDurationSec"] = stickiness_cookie_duration_sec

        if targets is not None:
            props["targets"] = targets

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if target_type is not None:
            props["targetType"] = target_type

        jsii.create(ApplicationTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, default_port: str, target_group_arn: str, load_balancer_arns: typing.Optional[str]=None) -> "IApplicationTargetGroup":
        """Import an existing target group.

        Arguments:
            scope: -
            id: -
            props: -
            defaultPort: Port target group is listening on.
            targetGroupArn: ARN of the target group.
            loadBalancerArns: A Token representing the list of ARNs for the load balancer routing to this target group.
        """
        props: TargetGroupImportProps = {"defaultPort": default_port, "targetGroupArn": target_group_arn}

        if load_balancer_arns is not None:
            props["loadBalancerArns"] = load_balancer_arns

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "IApplicationLoadBalancerTarget") -> None:
        """Add a load balancing target to this target group.

        Arguments:
            targets: -
        """
        return jsii.invoke(self, "addTarget", [targets])

    @jsii.member(jsii_name="enableCookieStickiness")
    def enable_cookie_stickiness(self, duration_sec: jsii.Number) -> None:
        """Enable sticky routing via a cookie to members of this target group.

        Arguments:
            durationSec: -
        """
        return jsii.invoke(self, "enableCookieStickiness", [duration_sec])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Application Load Balancer Target Group.

        Returns the metric for this target group from the point of view of the first
        load balancer load balancing to it. If you have multiple load balancers load
        sending traffic to the same target group, you will have to override the dimensions
        on this metric.

        Arguments:
            metricName: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of healthy hosts in the target group.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHealthyHostCount", [props])

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(self, code: "HttpCodeTarget", *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of HTTP 2xx/3xx/4xx/5xx response codes generated by all targets in this target group.

        This does not include any response codes generated by the load balancer.

        Arguments:
            code: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricHttpCodeTarget", [code, props])

    @jsii.member(jsii_name="metricIPv6RequestCount")
    def metric_i_pv6_request_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of IPv6 requests received by the target group.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricIPv6RequestCount", [props])

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of requests processed over IPv4 and IPv6.

        This count includes only the requests with a response generated by a target of the load balancer.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRequestCount", [props])

    @jsii.member(jsii_name="metricRequestCountPerTarget")
    def metric_request_count_per_target(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The average number of requests received by each target in a target group.

        The only valid statistic is Sum. Note that this represents the average not the sum.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricRequestCountPerTarget", [props])

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of connections that were not successfully established between the load balancer and target.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetConnectionErrorCount", [props])

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The time elapsed, in seconds, after the request leaves the load balancer until a response from the target is received.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetResponseTime", [props])

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of TLS connections initiated by the load balancer that did not establish a session with the target.

        Possible causes include a mismatch of ciphers or protocols.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props])

    @jsii.member(jsii_name="metricUnhealthyHostCount")
    def metric_unhealthy_host_count(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of unhealthy hosts in the target group.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            Average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricUnhealthyHostCount", [props])

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(self, connectable: aws_cdk.aws_ec2.IConnectable, port_range: typing.Optional[aws_cdk.aws_ec2.IPortRange]=None) -> None:
        """Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        Arguments:
            connectable: -
            portRange: -
        """
        return jsii.invoke(self, "registerConnectable", [connectable, port_range])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "IApplicationListener", associating_construct: typing.Optional[aws_cdk.cdk.IConstruct]=None) -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        Arguments:
            listener: -
            associatingConstruct: -
        """
        return jsii.invoke(self, "registerListener", [listener, associating_construct])

    @property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> str:
        """Full name of first load balancer."""
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.implements(INetworkTargetGroup)
class NetworkTargetGroup(TargetGroupBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2.NetworkTargetGroup"):
    """Define a Network Target Group."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, port: jsii.Number, proxy_protocol_v2: typing.Optional[bool]=None, targets: typing.Optional[typing.List["INetworkLoadBalancerTarget"]]=None, vpc: aws_cdk.aws_ec2.IVpc, deregistration_delay_sec: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, target_group_name: typing.Optional[str]=None, target_type: typing.Optional["TargetType"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            port: The port on which the listener listens for requests.
            proxyProtocolV2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
            targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
            vpc: The virtual private cloud (VPC).
            deregistrationDelaySec: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
            healthCheck: Health check configuration. Default: - None.
            targetGroupName: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
            targetType: The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        """
        props: NetworkTargetGroupProps = {"port": port, "vpc": vpc}

        if proxy_protocol_v2 is not None:
            props["proxyProtocolV2"] = proxy_protocol_v2

        if targets is not None:
            props["targets"] = targets

        if deregistration_delay_sec is not None:
            props["deregistrationDelaySec"] = deregistration_delay_sec

        if health_check is not None:
            props["healthCheck"] = health_check

        if target_group_name is not None:
            props["targetGroupName"] = target_group_name

        if target_type is not None:
            props["targetType"] = target_type

        jsii.create(NetworkTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, scope: aws_cdk.cdk.Construct, id: str, *, default_port: str, target_group_arn: str, load_balancer_arns: typing.Optional[str]=None) -> "INetworkTargetGroup":
        """Import an existing listener.

        Arguments:
            scope: -
            id: -
            props: -
            defaultPort: Port target group is listening on.
            targetGroupArn: ARN of the target group.
            loadBalancerArns: A Token representing the list of ARNs for the load balancer routing to this target group.
        """
        props: TargetGroupImportProps = {"defaultPort": default_port, "targetGroupArn": target_group_arn}

        if load_balancer_arns is not None:
            props["loadBalancerArns"] = load_balancer_arns

        return jsii.sinvoke(cls, "import", [scope, id, props])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: "INetworkLoadBalancerTarget") -> None:
        """Add a load balancing target to this target group.

        Arguments:
            targets: -
        """
        return jsii.invoke(self, "addTarget", [targets])

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: "INetworkListener") -> None:
        """Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        Arguments:
            listener: -
        """
        return jsii.invoke(self, "registerListener", [listener])

    @property
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> str:
        """Full name of first load balancer."""
        return jsii.get(self, "firstLoadBalancerFullName")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _TargetGroupImportProps(jsii.compat.TypedDict, total=False):
    loadBalancerArns: str
    """A Token representing the list of ARNs for the load balancer routing to this target group."""

@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetGroupImportProps", jsii_struct_bases=[_TargetGroupImportProps])
class TargetGroupImportProps(_TargetGroupImportProps):
    """Properties to reference an existing target group."""
    defaultPort: str
    """Port target group is listening on."""

    targetGroupArn: str
    """ARN of the target group."""

@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancingv2.TargetType")
class TargetType(enum.Enum):
    """How to interpret the load balancing target identifiers."""
    Instance = "Instance"
    """Targets identified by instance ID."""
    Ip = "Ip"
    """Targets identified by IP address."""

__all__ = ["AddApplicationTargetGroupsProps", "AddApplicationTargetsProps", "AddFixedResponseProps", "AddNetworkTargetsProps", "AddRuleProps", "ApplicationListener", "ApplicationListenerAttributes", "ApplicationListenerCertificate", "ApplicationListenerCertificateProps", "ApplicationListenerProps", "ApplicationListenerRule", "ApplicationListenerRuleProps", "ApplicationLoadBalancer", "ApplicationLoadBalancerAttributes", "ApplicationLoadBalancerProps", "ApplicationProtocol", "ApplicationTargetGroup", "ApplicationTargetGroupProps", "BaseApplicationListenerProps", "BaseApplicationListenerRuleProps", "BaseListener", "BaseLoadBalancer", "BaseLoadBalancerProps", "BaseNetworkListenerProps", "BaseTargetGroupProps", "CfnListener", "CfnListenerCertificate", "CfnListenerCertificateProps", "CfnListenerProps", "CfnListenerRule", "CfnListenerRuleProps", "CfnLoadBalancer", "CfnLoadBalancerProps", "CfnTargetGroup", "CfnTargetGroupProps", "ContentType", "FixedResponse", "HealthCheck", "HttpCodeElb", "HttpCodeTarget", "IApplicationListener", "IApplicationLoadBalancer", "IApplicationLoadBalancerTarget", "IApplicationTargetGroup", "ILoadBalancerV2", "INetworkListener", "INetworkListenerCertificateProps", "INetworkLoadBalancer", "INetworkLoadBalancerTarget", "INetworkTargetGroup", "ITargetGroup", "InstanceTarget", "IpAddressType", "IpTarget", "LoadBalancerTargetProps", "NetworkListener", "NetworkListenerProps", "NetworkLoadBalancer", "NetworkLoadBalancerAttributes", "NetworkLoadBalancerProps", "NetworkTargetGroup", "NetworkTargetGroupProps", "Protocol", "SslPolicy", "TargetGroupBase", "TargetGroupImportProps", "TargetType", "__jsii_assembly__"]

publication.publish()
