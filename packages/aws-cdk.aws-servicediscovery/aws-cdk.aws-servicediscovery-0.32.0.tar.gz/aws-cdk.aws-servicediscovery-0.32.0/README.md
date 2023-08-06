## The CDK Construct Library for AWS Service Discovery
This module is part of the [AWS Cloud Development Kit](https://github.com/awslabs/aws-cdk) project.

This package contains constructs for working with **AWS Cloud Map**

AWS Cloud Map is a fully managed service that you can use to create and
maintain a map of the backend services and resources that your applications
depend on.

For further information on AWS Cloud Map,
see the [AWS Cloud Map documentation](https://docs.aws.amazon.com/cloud-map)

The following example creates an AWS Cloud Map namespace that
supports API calls, creates a service in that namespace, and
registers an instance to it:

```ts
import cdk = require('@aws-cdk/cdk');
import servicediscovery = require('../lib');

const app = new cdk.App();
const stack = new cdk.Stack(app, 'aws-servicediscovery-integ');

const namespace = new servicediscovery.HttpNamespace(stack, 'MyNamespace', {
  name: 'covfefe',
});

const service1 = namespace.createService('NonIpService', {
  description: 'service registering non-ip instances',
});

service1.registerNonIpInstance('NonIpInstance', {
  customAttributes: { arn: 'arn:aws:s3:::mybucket' }
});

const service2 = namespace.createService('IpService', {
  description: 'service registering ip instances',
  healthCheck: {
    type: servicediscovery.HealthCheckType.Http,
    resourcePath: '/check'
  }
});

service2.registerIpInstance('IpInstance', {
  ipv4: '54.239.25.192',
});

app.run();

```

The following example creates an AWS Cloud Map namespace that
supports both API calls and DNS queries within a vpc, creates a
service in that namespace, and registers a loadbalancer as an
instance:

```ts
import ec2 = require('@aws-cdk/aws-ec2');
import elbv2 = require('@aws-cdk/aws-elasticloadbalancingv2');
import cdk = require('@aws-cdk/cdk');
import servicediscovery = require('../lib');

const app = new cdk.App();
const stack = new cdk.Stack(app, 'aws-servicediscovery-integ');

const vpc = new ec2.Vpc(stack, 'Vpc', { maxAZs: 2 });

const namespace = new servicediscovery.PrivateDnsNamespace(stack, 'Namespace', {
  name: 'boobar.com',
  vpc,
});

const service = namespace.createService('Service', {
  dnsRecordType: servicediscovery.DnsRecordType.A_AAAA,
  dnsTtlSec: 30,
  loadBalancer: true
});

const loadbalancer = new elbv2.ApplicationLoadBalancer(stack, 'LB', { vpc, internetFacing: true });

service.registerLoadBalancer("Loadbalancer", loadbalancer);

app.run();

```

The following example creates an AWS Cloud Map namespace that
supports both API calls and public DNS queries, creates a service in
that namespace, and registers an IP instance:

```ts
import cdk = require('@aws-cdk/cdk');
import servicediscovery = require('../lib');

const app = new cdk.App();
const stack = new cdk.Stack(app, 'aws-servicediscovery-integ');

const namespace = new servicediscovery.PublicDnsNamespace(stack, 'Namespace', {
  name: 'foobar.com',
});

const service = namespace.createService('Service', {
  name: 'foo',
  dnsRecordType: servicediscovery.DnsRecordType.A,
  dnsTtlSec: 30,
  healthCheck: {
    type: servicediscovery.HealthCheckType.Https,
    resourcePath: '/healthcheck',
    failureThreshold: 2
  }
});

service.registerIpInstance('IpInstance', {
  ipv4: '54.239.25.192',
  port: 443
});

app.run();

```

For DNS namespaces, you can also register instances to services with CNAME records:

```ts
import cdk = require('@aws-cdk/cdk');
import servicediscovery = require('../lib');

const app = new cdk.App();
const stack = new cdk.Stack(app, 'aws-servicediscovery-integ');

const namespace = new servicediscovery.PublicDnsNamespace(stack, 'Namespace', {
  name: 'foobar.com',
});

const service = namespace.createService('Service', {
  name: 'foo',
  dnsRecordType: servicediscovery.DnsRecordType.CNAME,
  dnsTtlSec: 30
});

service.registerCnameInstance('CnameInstance', {
  instanceCname: 'service.pizza',
});

app.run();

```

