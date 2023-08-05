## The CDK Construct Library for AWS Systems Manager
This module is part of the [AWS Cloud Development Kit](https://github.com/awslabs/aws-cdk) project.

### Installation
Install the module:

```console
$ npm i @aws-cdk/aws-ssm
```

Import it into your code:

```ts
import ssm = require('@aws-cdk/aws-ssm');
```

### Using existing SSM Parameters in your CDK app

You can reference existing SSM Parameter Store values that you want to use in
your CDK app by using `ssm.ParameterStoreString`:

```ts
    // Retrieve the latest value of the non-secret parameter
    // with name "/My/String/Parameter".
    const stringValue = new ssm.ParameterStoreString(this, 'MyValue', {
      parameterName: '/My/Public/Parameter',
      // 'version' can be specified but is optional.
    }).stringValue;

    // Retrieve a specific version of the secret (SecureString) parameter.
    // 'version' is always required.
    const secretValue = new ssm.ParameterStoreSecureString({
      parameterName: '/My/Secret/Parameter',
      version: 5
    });
```

### Creating new SSM Parameters in your CDK app

You can create either `ssm.StringParameter` or `ssm.StringListParameter`s in
a CDK app. These are public (not secret) values. Parameters of type
*SecretString* cannot be created directly from a CDK application; if you want
to provision secrets automatically, use Secrets Manager Secrets (see the
`@aws-cdk/aws-secretsmanager` package).

```ts
// Create a new SSM Parameter holding a String
const param = new ssm.StringParameter(stack, 'StringParameter', {
  // description: 'Some user-friendly description',
  // name: 'ParameterName',
  stringValue: 'Initial parameter value',
  // allowedPattern: '.*',
});

// Grant read access to some Role
param.grantRead(role);

// Create a new SSM Parameter holding a StringList
const listParameter = new ssm.StringListParameter(stack, 'StringListParameter', {
  // description: 'Some user-friendly description',
  // name: 'ParameterName',
  stringListValue: ['Initial parameter value A', 'Initial parameter value B'],
  // allowedPattern: '.*',
});
```

When specifying an `allowedPattern`, the values provided as string literals
are validated against the pattern and an exception is raised if a value
provided does not comply.

