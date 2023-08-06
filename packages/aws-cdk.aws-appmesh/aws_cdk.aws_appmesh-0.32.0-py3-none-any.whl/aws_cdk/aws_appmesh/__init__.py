import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-appmesh", "0.32.0", __name__, "aws-appmesh@0.32.0.jsii.tgz")
class CfnMesh(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnMesh"):
    """A CloudFormation ``AWS::AppMesh::Mesh``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html
    cloudformationResource:
        AWS::AppMesh::Mesh
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, spec: typing.Optional[typing.Union[typing.Optional["MeshSpecProperty"], typing.Optional[aws_cdk.cdk.Token]]]=None, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        """Create a new ``AWS::AppMesh::Mesh``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            meshName: ``AWS::AppMesh::Mesh.MeshName``.
            spec: ``AWS::AppMesh::Mesh.Spec``.
            tags: ``AWS::AppMesh::Mesh.Tags``.
        """
        props: CfnMeshProps = {"meshName": mesh_name}

        if spec is not None:
            props["spec"] = spec

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnMesh, self, [scope, id, props])

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
    @jsii.member(jsii_name="meshArn")
    def mesh_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "meshArn")

    @property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        """
        cloudformationAttribute:
            MeshName
        """
        return jsii.get(self, "meshName")

    @property
    @jsii.member(jsii_name="meshUid")
    def mesh_uid(self) -> str:
        """
        cloudformationAttribute:
            Uid
        """
        return jsii.get(self, "meshUid")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMeshProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnMesh.EgressFilterProperty", jsii_struct_bases=[])
    class EgressFilterProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html
        """
        type: str
        """``CfnMesh.EgressFilterProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html#cfn-appmesh-mesh-egressfilter-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnMesh.MeshSpecProperty", jsii_struct_bases=[])
    class MeshSpecProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshspec.html
        """
        egressFilter: typing.Union[aws_cdk.cdk.Token, "CfnMesh.EgressFilterProperty"]
        """``CfnMesh.MeshSpecProperty.EgressFilter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshspec.html#cfn-appmesh-mesh-meshspec-egressfilter
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str
        """``CfnMesh.TagRefProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-tagref.html#cfn-appmesh-mesh-tagref-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnMesh.TagRefProperty", jsii_struct_bases=[_TagRefProperty])
    class TagRefProperty(_TagRefProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-tagref.html
        """
        key: str
        """``CfnMesh.TagRefProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-tagref.html#cfn-appmesh-mesh-tagref-key
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnMeshProps(jsii.compat.TypedDict, total=False):
    spec: typing.Union["CfnMesh.MeshSpecProperty", aws_cdk.cdk.Token]
    """``AWS::AppMesh::Mesh.Spec``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-spec
    """
    tags: typing.List["CfnMesh.TagRefProperty"]
    """``AWS::AppMesh::Mesh.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnMeshProps", jsii_struct_bases=[_CfnMeshProps])
class CfnMeshProps(_CfnMeshProps):
    """Properties for defining a ``AWS::AppMesh::Mesh``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html
    """
    meshName: str
    """``AWS::AppMesh::Mesh.MeshName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-meshname
    """

class CfnRoute(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnRoute"):
    """A CloudFormation ``AWS::AppMesh::Route``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html
    cloudformationResource:
        AWS::AppMesh::Route
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, route_name: str, spec: typing.Union[aws_cdk.cdk.Token, "RouteSpecProperty"], virtual_router_name: str, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        """Create a new ``AWS::AppMesh::Route``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            meshName: ``AWS::AppMesh::Route.MeshName``.
            routeName: ``AWS::AppMesh::Route.RouteName``.
            spec: ``AWS::AppMesh::Route.Spec``.
            virtualRouterName: ``AWS::AppMesh::Route.VirtualRouterName``.
            tags: ``AWS::AppMesh::Route.Tags``.
        """
        props: CfnRouteProps = {"meshName": mesh_name, "routeName": route_name, "spec": spec, "virtualRouterName": virtual_router_name}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnRoute, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRouteProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "routeArn")

    @property
    @jsii.member(jsii_name="routeMeshName")
    def route_mesh_name(self) -> str:
        """
        cloudformationAttribute:
            MeshName
        """
        return jsii.get(self, "routeMeshName")

    @property
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> str:
        """
        cloudformationAttribute:
            RouteName
        """
        return jsii.get(self, "routeName")

    @property
    @jsii.member(jsii_name="routeUid")
    def route_uid(self) -> str:
        """
        cloudformationAttribute:
            Uid
        """
        return jsii.get(self, "routeUid")

    @property
    @jsii.member(jsii_name="routeVirtualRouterName")
    def route_virtual_router_name(self) -> str:
        """
        cloudformationAttribute:
            VirtualRouterName
        """
        return jsii.get(self, "routeVirtualRouterName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteActionProperty", jsii_struct_bases=[])
    class HttpRouteActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteaction.html
        """
        weightedTargets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRoute.WeightedTargetProperty"]]]
        """``CfnRoute.HttpRouteActionProperty.WeightedTargets``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteaction.html#cfn-appmesh-route-httprouteaction-weightedtargets
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteMatchProperty", jsii_struct_bases=[])
    class HttpRouteMatchProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html
        """
        prefix: str
        """``CfnRoute.HttpRouteMatchProperty.Prefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-prefix
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.HttpRouteProperty", jsii_struct_bases=[])
    class HttpRouteProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html
        """
        action: typing.Union[aws_cdk.cdk.Token, "CfnRoute.HttpRouteActionProperty"]
        """``CfnRoute.HttpRouteProperty.Action``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-action
        """

        match: typing.Union[aws_cdk.cdk.Token, "CfnRoute.HttpRouteMatchProperty"]
        """``CfnRoute.HttpRouteProperty.Match``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-match
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.RouteSpecProperty", jsii_struct_bases=[])
    class RouteSpecProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html
        """
        httpRoute: typing.Union[aws_cdk.cdk.Token, "CfnRoute.HttpRouteProperty"]
        """``CfnRoute.RouteSpecProperty.HttpRoute``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-httproute
        """

        tcpRoute: typing.Union[aws_cdk.cdk.Token, "CfnRoute.TcpRouteProperty"]
        """``CfnRoute.RouteSpecProperty.TcpRoute``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-tcproute
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str
        """``CfnRoute.TagRefProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tagref.html#cfn-appmesh-route-tagref-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.TagRefProperty", jsii_struct_bases=[_TagRefProperty])
    class TagRefProperty(_TagRefProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tagref.html
        """
        key: str
        """``CfnRoute.TagRefProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tagref.html#cfn-appmesh-route-tagref-key
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.TcpRouteActionProperty", jsii_struct_bases=[])
    class TcpRouteActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcprouteaction.html
        """
        weightedTargets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRoute.WeightedTargetProperty"]]]
        """``CfnRoute.TcpRouteActionProperty.WeightedTargets``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcprouteaction.html#cfn-appmesh-route-tcprouteaction-weightedtargets
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.TcpRouteProperty", jsii_struct_bases=[])
    class TcpRouteProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html
        """
        action: typing.Union[aws_cdk.cdk.Token, "CfnRoute.TcpRouteActionProperty"]
        """``CfnRoute.TcpRouteProperty.Action``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html#cfn-appmesh-route-tcproute-action
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRoute.WeightedTargetProperty", jsii_struct_bases=[])
    class WeightedTargetProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html
        """
        virtualNode: str
        """``CfnRoute.WeightedTargetProperty.VirtualNode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html#cfn-appmesh-route-weightedtarget-virtualnode
        """

        weight: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnRoute.WeightedTargetProperty.Weight``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html#cfn-appmesh-route-weightedtarget-weight
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnRouteProps(jsii.compat.TypedDict, total=False):
    tags: typing.List["CfnRoute.TagRefProperty"]
    """``AWS::AppMesh::Route.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnRouteProps", jsii_struct_bases=[_CfnRouteProps])
class CfnRouteProps(_CfnRouteProps):
    """Properties for defining a ``AWS::AppMesh::Route``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html
    """
    meshName: str
    """``AWS::AppMesh::Route.MeshName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshname
    """

    routeName: str
    """``AWS::AppMesh::Route.RouteName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-routename
    """

    spec: typing.Union[aws_cdk.cdk.Token, "CfnRoute.RouteSpecProperty"]
    """``AWS::AppMesh::Route.Spec``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-spec
    """

    virtualRouterName: str
    """``AWS::AppMesh::Route.VirtualRouterName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-virtualroutername
    """

class CfnVirtualNode(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode"):
    """A CloudFormation ``AWS::AppMesh::VirtualNode``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html
    cloudformationResource:
        AWS::AppMesh::VirtualNode
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, spec: typing.Union[aws_cdk.cdk.Token, "VirtualNodeSpecProperty"], virtual_node_name: str, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        """Create a new ``AWS::AppMesh::VirtualNode``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            meshName: ``AWS::AppMesh::VirtualNode.MeshName``.
            spec: ``AWS::AppMesh::VirtualNode.Spec``.
            virtualNodeName: ``AWS::AppMesh::VirtualNode.VirtualNodeName``.
            tags: ``AWS::AppMesh::VirtualNode.Tags``.
        """
        props: CfnVirtualNodeProps = {"meshName": mesh_name, "spec": spec, "virtualNodeName": virtual_node_name}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVirtualNode, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVirtualNodeProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="virtualNodeArn")
    def virtual_node_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "virtualNodeArn")

    @property
    @jsii.member(jsii_name="virtualNodeMeshName")
    def virtual_node_mesh_name(self) -> str:
        """
        cloudformationAttribute:
            MeshName
        """
        return jsii.get(self, "virtualNodeMeshName")

    @property
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> str:
        """
        cloudformationAttribute:
            VirtualNodeName
        """
        return jsii.get(self, "virtualNodeName")

    @property
    @jsii.member(jsii_name="virtualNodeUid")
    def virtual_node_uid(self) -> str:
        """
        cloudformationAttribute:
            Uid
        """
        return jsii.get(self, "virtualNodeUid")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.AccessLogProperty", jsii_struct_bases=[])
    class AccessLogProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-accesslog.html
        """
        file: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.FileAccessLogProperty"]
        """``CfnVirtualNode.AccessLogProperty.File``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-accesslog.html#cfn-appmesh-virtualnode-accesslog-file
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.BackendProperty", jsii_struct_bases=[])
    class BackendProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backend.html
        """
        virtualService: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.VirtualServiceBackendProperty"]
        """``CfnVirtualNode.BackendProperty.VirtualService``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backend.html#cfn-appmesh-virtualnode-backend-virtualservice
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.DnsServiceDiscoveryProperty", jsii_struct_bases=[])
    class DnsServiceDiscoveryProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html
        """
        hostname: str
        """``CfnVirtualNode.DnsServiceDiscoveryProperty.Hostname``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html#cfn-appmesh-virtualnode-dnsservicediscovery-hostname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.FileAccessLogProperty", jsii_struct_bases=[])
    class FileAccessLogProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-fileaccesslog.html
        """
        path: str
        """``CfnVirtualNode.FileAccessLogProperty.Path``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-fileaccesslog.html#cfn-appmesh-virtualnode-fileaccesslog-path
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _HealthCheckProperty(jsii.compat.TypedDict, total=False):
        path: str
        """``CfnVirtualNode.HealthCheckProperty.Path``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-path
        """
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnVirtualNode.HealthCheckProperty.Port``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-port
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.HealthCheckProperty", jsii_struct_bases=[_HealthCheckProperty])
    class HealthCheckProperty(_HealthCheckProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html
        """
        healthyThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnVirtualNode.HealthCheckProperty.HealthyThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-healthythreshold
        """

        intervalMillis: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnVirtualNode.HealthCheckProperty.IntervalMillis``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-intervalmillis
        """

        protocol: str
        """``CfnVirtualNode.HealthCheckProperty.Protocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-protocol
        """

        timeoutMillis: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnVirtualNode.HealthCheckProperty.TimeoutMillis``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-timeoutmillis
        """

        unhealthyThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnVirtualNode.HealthCheckProperty.UnhealthyThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-unhealthythreshold
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ListenerProperty(jsii.compat.TypedDict, total=False):
        healthCheck: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.HealthCheckProperty"]
        """``CfnVirtualNode.ListenerProperty.HealthCheck``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-healthcheck
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ListenerProperty", jsii_struct_bases=[_ListenerProperty])
    class ListenerProperty(_ListenerProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html
        """
        portMapping: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.PortMappingProperty"]
        """``CfnVirtualNode.ListenerProperty.PortMapping``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-portmapping
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.LoggingProperty", jsii_struct_bases=[])
    class LoggingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-logging.html
        """
        accessLog: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.AccessLogProperty"]
        """``CfnVirtualNode.LoggingProperty.AccessLog``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-logging.html#cfn-appmesh-virtualnode-logging-accesslog
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.PortMappingProperty", jsii_struct_bases=[])
    class PortMappingProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html
        """
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnVirtualNode.PortMappingProperty.Port``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html#cfn-appmesh-virtualnode-portmapping-port
        """

        protocol: str
        """``CfnVirtualNode.PortMappingProperty.Protocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html#cfn-appmesh-virtualnode-portmapping-protocol
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.ServiceDiscoveryProperty", jsii_struct_bases=[])
    class ServiceDiscoveryProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html
        """
        dns: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.DnsServiceDiscoveryProperty"]
        """``CfnVirtualNode.ServiceDiscoveryProperty.DNS``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html#cfn-appmesh-virtualnode-servicediscovery-dns
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str
        """``CfnVirtualNode.TagRefProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tagref.html#cfn-appmesh-virtualnode-tagref-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.TagRefProperty", jsii_struct_bases=[_TagRefProperty])
    class TagRefProperty(_TagRefProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tagref.html
        """
        key: str
        """``CfnVirtualNode.TagRefProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tagref.html#cfn-appmesh-virtualnode-tagref-key
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualNodeSpecProperty", jsii_struct_bases=[])
    class VirtualNodeSpecProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html
        """
        backends: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.BackendProperty"]]]
        """``CfnVirtualNode.VirtualNodeSpecProperty.Backends``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-backends
        """

        listeners: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.ListenerProperty"]]]
        """``CfnVirtualNode.VirtualNodeSpecProperty.Listeners``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-listeners
        """

        logging: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.LoggingProperty"]
        """``CfnVirtualNode.VirtualNodeSpecProperty.Logging``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-logging
        """

        serviceDiscovery: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.ServiceDiscoveryProperty"]
        """``CfnVirtualNode.VirtualNodeSpecProperty.ServiceDiscovery``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-servicediscovery
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNode.VirtualServiceBackendProperty", jsii_struct_bases=[])
    class VirtualServiceBackendProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html
        """
        virtualServiceName: str
        """``CfnVirtualNode.VirtualServiceBackendProperty.VirtualServiceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html#cfn-appmesh-virtualnode-virtualservicebackend-virtualservicename
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVirtualNodeProps(jsii.compat.TypedDict, total=False):
    tags: typing.List["CfnVirtualNode.TagRefProperty"]
    """``AWS::AppMesh::VirtualNode.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualNodeProps", jsii_struct_bases=[_CfnVirtualNodeProps])
class CfnVirtualNodeProps(_CfnVirtualNodeProps):
    """Properties for defining a ``AWS::AppMesh::VirtualNode``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html
    """
    meshName: str
    """``AWS::AppMesh::VirtualNode.MeshName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshname
    """

    spec: typing.Union[aws_cdk.cdk.Token, "CfnVirtualNode.VirtualNodeSpecProperty"]
    """``AWS::AppMesh::VirtualNode.Spec``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-spec
    """

    virtualNodeName: str
    """``AWS::AppMesh::VirtualNode.VirtualNodeName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-virtualnodename
    """

class CfnVirtualRouter(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter"):
    """A CloudFormation ``AWS::AppMesh::VirtualRouter``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html
    cloudformationResource:
        AWS::AppMesh::VirtualRouter
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, spec: typing.Union[aws_cdk.cdk.Token, "VirtualRouterSpecProperty"], virtual_router_name: str, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        """Create a new ``AWS::AppMesh::VirtualRouter``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            meshName: ``AWS::AppMesh::VirtualRouter.MeshName``.
            spec: ``AWS::AppMesh::VirtualRouter.Spec``.
            virtualRouterName: ``AWS::AppMesh::VirtualRouter.VirtualRouterName``.
            tags: ``AWS::AppMesh::VirtualRouter.Tags``.
        """
        props: CfnVirtualRouterProps = {"meshName": mesh_name, "spec": spec, "virtualRouterName": virtual_router_name}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVirtualRouter, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVirtualRouterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="virtualRouterArn")
    def virtual_router_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "virtualRouterArn")

    @property
    @jsii.member(jsii_name="virtualRouterMeshName")
    def virtual_router_mesh_name(self) -> str:
        """
        cloudformationAttribute:
            MeshName
        """
        return jsii.get(self, "virtualRouterMeshName")

    @property
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> str:
        """
        cloudformationAttribute:
            VirtualRouterName
        """
        return jsii.get(self, "virtualRouterName")

    @property
    @jsii.member(jsii_name="virtualRouterUid")
    def virtual_router_uid(self) -> str:
        """
        cloudformationAttribute:
            Uid
        """
        return jsii.get(self, "virtualRouterUid")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.PortMappingProperty", jsii_struct_bases=[])
    class PortMappingProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html
        """
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnVirtualRouter.PortMappingProperty.Port``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html#cfn-appmesh-virtualrouter-portmapping-port
        """

        protocol: str
        """``CfnVirtualRouter.PortMappingProperty.Protocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html#cfn-appmesh-virtualrouter-portmapping-protocol
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str
        """``CfnVirtualRouter.TagRefProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-tagref.html#cfn-appmesh-virtualrouter-tagref-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.TagRefProperty", jsii_struct_bases=[_TagRefProperty])
    class TagRefProperty(_TagRefProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-tagref.html
        """
        key: str
        """``CfnVirtualRouter.TagRefProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-tagref.html#cfn-appmesh-virtualrouter-tagref-key
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.VirtualRouterListenerProperty", jsii_struct_bases=[])
    class VirtualRouterListenerProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterlistener.html
        """
        portMapping: typing.Union[aws_cdk.cdk.Token, "CfnVirtualRouter.PortMappingProperty"]
        """``CfnVirtualRouter.VirtualRouterListenerProperty.PortMapping``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterlistener.html#cfn-appmesh-virtualrouter-virtualrouterlistener-portmapping
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouter.VirtualRouterSpecProperty", jsii_struct_bases=[])
    class VirtualRouterSpecProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterspec.html
        """
        listeners: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnVirtualRouter.VirtualRouterListenerProperty"]]]
        """``CfnVirtualRouter.VirtualRouterSpecProperty.Listeners``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterspec.html#cfn-appmesh-virtualrouter-virtualrouterspec-listeners
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVirtualRouterProps(jsii.compat.TypedDict, total=False):
    tags: typing.List["CfnVirtualRouter.TagRefProperty"]
    """``AWS::AppMesh::VirtualRouter.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualRouterProps", jsii_struct_bases=[_CfnVirtualRouterProps])
class CfnVirtualRouterProps(_CfnVirtualRouterProps):
    """Properties for defining a ``AWS::AppMesh::VirtualRouter``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html
    """
    meshName: str
    """``AWS::AppMesh::VirtualRouter.MeshName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshname
    """

    spec: typing.Union[aws_cdk.cdk.Token, "CfnVirtualRouter.VirtualRouterSpecProperty"]
    """``AWS::AppMesh::VirtualRouter.Spec``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-spec
    """

    virtualRouterName: str
    """``AWS::AppMesh::VirtualRouter.VirtualRouterName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-virtualroutername
    """

class CfnVirtualService(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService"):
    """A CloudFormation ``AWS::AppMesh::VirtualService``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html
    cloudformationResource:
        AWS::AppMesh::VirtualService
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, mesh_name: str, spec: typing.Union[aws_cdk.cdk.Token, "VirtualServiceSpecProperty"], virtual_service_name: str, tags: typing.Optional[typing.List["TagRefProperty"]]=None) -> None:
        """Create a new ``AWS::AppMesh::VirtualService``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            meshName: ``AWS::AppMesh::VirtualService.MeshName``.
            spec: ``AWS::AppMesh::VirtualService.Spec``.
            virtualServiceName: ``AWS::AppMesh::VirtualService.VirtualServiceName``.
            tags: ``AWS::AppMesh::VirtualService.Tags``.
        """
        props: CfnVirtualServiceProps = {"meshName": mesh_name, "spec": spec, "virtualServiceName": virtual_service_name}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVirtualService, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVirtualServiceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="virtualServiceArn")
    def virtual_service_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "virtualServiceArn")

    @property
    @jsii.member(jsii_name="virtualServiceMeshName")
    def virtual_service_mesh_name(self) -> str:
        """
        cloudformationAttribute:
            MeshName
        """
        return jsii.get(self, "virtualServiceMeshName")

    @property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> str:
        """
        cloudformationAttribute:
            VirtualServiceName
        """
        return jsii.get(self, "virtualServiceName")

    @property
    @jsii.member(jsii_name="virtualServiceUid")
    def virtual_service_uid(self) -> str:
        """
        cloudformationAttribute:
            Uid
        """
        return jsii.get(self, "virtualServiceUid")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TagRefProperty(jsii.compat.TypedDict, total=False):
        value: str
        """``CfnVirtualService.TagRefProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-tagref.html#cfn-appmesh-virtualservice-tagref-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.TagRefProperty", jsii_struct_bases=[_TagRefProperty])
    class TagRefProperty(_TagRefProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-tagref.html
        """
        key: str
        """``CfnVirtualService.TagRefProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-tagref.html#cfn-appmesh-virtualservice-tagref-key
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualNodeServiceProviderProperty", jsii_struct_bases=[])
    class VirtualNodeServiceProviderProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualnodeserviceprovider.html
        """
        virtualNodeName: str
        """``CfnVirtualService.VirtualNodeServiceProviderProperty.VirtualNodeName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualnodeserviceprovider.html#cfn-appmesh-virtualservice-virtualnodeserviceprovider-virtualnodename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualRouterServiceProviderProperty", jsii_struct_bases=[])
    class VirtualRouterServiceProviderProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualrouterserviceprovider.html
        """
        virtualRouterName: str
        """``CfnVirtualService.VirtualRouterServiceProviderProperty.VirtualRouterName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualrouterserviceprovider.html#cfn-appmesh-virtualservice-virtualrouterserviceprovider-virtualroutername
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualServiceProviderProperty", jsii_struct_bases=[])
    class VirtualServiceProviderProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html
        """
        virtualNode: typing.Union[aws_cdk.cdk.Token, "CfnVirtualService.VirtualNodeServiceProviderProperty"]
        """``CfnVirtualService.VirtualServiceProviderProperty.VirtualNode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html#cfn-appmesh-virtualservice-virtualserviceprovider-virtualnode
        """

        virtualRouter: typing.Union[aws_cdk.cdk.Token, "CfnVirtualService.VirtualRouterServiceProviderProperty"]
        """``CfnVirtualService.VirtualServiceProviderProperty.VirtualRouter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html#cfn-appmesh-virtualservice-virtualserviceprovider-virtualrouter
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualService.VirtualServiceSpecProperty", jsii_struct_bases=[])
    class VirtualServiceSpecProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualservicespec.html
        """
        provider: typing.Union[aws_cdk.cdk.Token, "CfnVirtualService.VirtualServiceProviderProperty"]
        """``CfnVirtualService.VirtualServiceSpecProperty.Provider``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualservicespec.html#cfn-appmesh-virtualservice-virtualservicespec-provider
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVirtualServiceProps(jsii.compat.TypedDict, total=False):
    tags: typing.List["CfnVirtualService.TagRefProperty"]
    """``AWS::AppMesh::VirtualService.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appmesh.CfnVirtualServiceProps", jsii_struct_bases=[_CfnVirtualServiceProps])
class CfnVirtualServiceProps(_CfnVirtualServiceProps):
    """Properties for defining a ``AWS::AppMesh::VirtualService``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html
    """
    meshName: str
    """``AWS::AppMesh::VirtualService.MeshName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshname
    """

    spec: typing.Union[aws_cdk.cdk.Token, "CfnVirtualService.VirtualServiceSpecProperty"]
    """``AWS::AppMesh::VirtualService.Spec``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-spec
    """

    virtualServiceName: str
    """``AWS::AppMesh::VirtualService.VirtualServiceName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-virtualservicename
    """

__all__ = ["CfnMesh", "CfnMeshProps", "CfnRoute", "CfnRouteProps", "CfnVirtualNode", "CfnVirtualNodeProps", "CfnVirtualRouter", "CfnVirtualRouterProps", "CfnVirtualService", "CfnVirtualServiceProps", "__jsii_assembly__"]

publication.publish()
