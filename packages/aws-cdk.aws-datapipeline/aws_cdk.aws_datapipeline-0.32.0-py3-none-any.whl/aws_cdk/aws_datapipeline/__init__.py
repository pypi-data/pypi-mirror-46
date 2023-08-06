import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-datapipeline", "0.32.0", __name__, "aws-datapipeline@0.32.0.jsii.tgz")
class CfnPipeline(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline"):
    """A CloudFormation ``AWS::DataPipeline::Pipeline``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html
    cloudformationResource:
        AWS::DataPipeline::Pipeline
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, parameter_objects: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["ParameterObjectProperty", aws_cdk.cdk.Token]]], activate: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, description: typing.Optional[str]=None, parameter_values: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ParameterValueProperty"]]]]]=None, pipeline_objects: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "PipelineObjectProperty"]]]]]=None, pipeline_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "PipelineTagProperty"]]]]]=None) -> None:
        """Create a new ``AWS::DataPipeline::Pipeline``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::DataPipeline::Pipeline.Name``.
            parameterObjects: ``AWS::DataPipeline::Pipeline.ParameterObjects``.
            activate: ``AWS::DataPipeline::Pipeline.Activate``.
            description: ``AWS::DataPipeline::Pipeline.Description``.
            parameterValues: ``AWS::DataPipeline::Pipeline.ParameterValues``.
            pipelineObjects: ``AWS::DataPipeline::Pipeline.PipelineObjects``.
            pipelineTags: ``AWS::DataPipeline::Pipeline.PipelineTags``.
        """
        props: CfnPipelineProps = {"name": name, "parameterObjects": parameter_objects}

        if activate is not None:
            props["activate"] = activate

        if description is not None:
            props["description"] = description

        if parameter_values is not None:
            props["parameterValues"] = parameter_values

        if pipeline_objects is not None:
            props["pipelineObjects"] = pipeline_objects

        if pipeline_tags is not None:
            props["pipelineTags"] = pipeline_tags

        jsii.create(CfnPipeline, self, [scope, id, props])

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
    @jsii.member(jsii_name="pipelineId")
    def pipeline_id(self) -> str:
        return jsii.get(self, "pipelineId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPipelineProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FieldProperty(jsii.compat.TypedDict, total=False):
        refValue: str
        """``CfnPipeline.FieldProperty.RefValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects-fields.html#cfn-datapipeline-pipeline-pipelineobjects-fields-refvalue
        """
        stringValue: str
        """``CfnPipeline.FieldProperty.StringValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects-fields.html#cfn-datapipeline-pipeline-pipelineobjects-fields-stringvalue
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.FieldProperty", jsii_struct_bases=[_FieldProperty])
    class FieldProperty(_FieldProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects-fields.html
        """
        key: str
        """``CfnPipeline.FieldProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects-fields.html#cfn-datapipeline-pipeline-pipelineobjects-fields-key
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.ParameterAttributeProperty", jsii_struct_bases=[])
    class ParameterAttributeProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects-attributes.html
        """
        key: str
        """``CfnPipeline.ParameterAttributeProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects-attributes.html#cfn-datapipeline-pipeline-parameterobjects-attribtues-key
        """

        stringValue: str
        """``CfnPipeline.ParameterAttributeProperty.StringValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects-attributes.html#cfn-datapipeline-pipeline-parameterobjects-attribtues-stringvalue
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.ParameterObjectProperty", jsii_struct_bases=[])
    class ParameterObjectProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects.html
        """
        attributes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ParameterAttributeProperty"]]]
        """``CfnPipeline.ParameterObjectProperty.Attributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects.html#cfn-datapipeline-pipeline-parameterobjects-attributes
        """

        id: str
        """``CfnPipeline.ParameterObjectProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobjects.html#cfn-datapipeline-pipeline-parameterobjects-id
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.ParameterValueProperty", jsii_struct_bases=[])
    class ParameterValueProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalues.html
        """
        id: str
        """``CfnPipeline.ParameterValueProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalues.html#cfn-datapipeline-pipeline-parametervalues-id
        """

        stringValue: str
        """``CfnPipeline.ParameterValueProperty.StringValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalues.html#cfn-datapipeline-pipeline-parametervalues-stringvalue
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.PipelineObjectProperty", jsii_struct_bases=[])
    class PipelineObjectProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects.html
        """
        fields: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.FieldProperty"]]]
        """``CfnPipeline.PipelineObjectProperty.Fields``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects.html#cfn-datapipeline-pipeline-pipelineobjects-fields
        """

        id: str
        """``CfnPipeline.PipelineObjectProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects.html#cfn-datapipeline-pipeline-pipelineobjects-id
        """

        name: str
        """``CfnPipeline.PipelineObjectProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobjects.html#cfn-datapipeline-pipeline-pipelineobjects-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.PipelineTagProperty", jsii_struct_bases=[])
    class PipelineTagProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetags.html
        """
        key: str
        """``CfnPipeline.PipelineTagProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetags.html#cfn-datapipeline-pipeline-pipelinetags-key
        """

        value: str
        """``CfnPipeline.PipelineTagProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetags.html#cfn-datapipeline-pipeline-pipelinetags-value
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnPipelineProps(jsii.compat.TypedDict, total=False):
    activate: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::DataPipeline::Pipeline.Activate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-activate
    """
    description: str
    """``AWS::DataPipeline::Pipeline.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-description
    """
    parameterValues: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ParameterValueProperty"]]]
    """``AWS::DataPipeline::Pipeline.ParameterValues``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parametervalues
    """
    pipelineObjects: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.PipelineObjectProperty"]]]
    """``AWS::DataPipeline::Pipeline.PipelineObjects``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelineobjects
    """
    pipelineTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.PipelineTagProperty"]]]
    """``AWS::DataPipeline::Pipeline.PipelineTags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelinetags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-datapipeline.CfnPipelineProps", jsii_struct_bases=[_CfnPipelineProps])
class CfnPipelineProps(_CfnPipelineProps):
    """Properties for defining a ``AWS::DataPipeline::Pipeline``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html
    """
    name: str
    """``AWS::DataPipeline::Pipeline.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-name
    """

    parameterObjects: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnPipeline.ParameterObjectProperty", aws_cdk.cdk.Token]]]
    """``AWS::DataPipeline::Pipeline.ParameterObjects``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parameterobjects
    """

__all__ = ["CfnPipeline", "CfnPipelineProps", "__jsii_assembly__"]

publication.publish()
