#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { FastApiLambdaStack } from "../lib/cdk-stack";
import { CdkContextProps } from "../lib/stack-props";
import { StackProps } from "aws-cdk-lib";

export interface AppStackProps extends StackProps {
  readonly cdkContext: CdkContextProps;
}

const app = new cdk.App();

const stage = app.node.tryGetContext("stage");

if (!stage)
  throw new Error(
    "Missing stage context. Pass in as `dev|stag|prod` in last command line argument."
  );

let cdkContextProps: CdkContextProps = app.node.tryGetContext(stage);
let stackName = `FastApiLambda-${stage}`;

const stackProps: AppStackProps = {
  cdkContext: cdkContextProps,
};
cdk.Tags.of(app).add("App", stackName);
cdk.Tags.of(app).add("Environment", cdkContextProps.env);
cdk.Tags.of(app).add("Version", cdkContextProps.version);

new FastApiLambdaStack(app, stackName, stackProps);
