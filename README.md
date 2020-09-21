# cdk-samples

[Cloud Development Kit](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-python.html) Samples in Python

## Prerequisites

- Install CDK CLI
```
npm install -g aws-cdk
```

## Manage Projects

### Create a new Project (new-stample)

```bash
mkdir new-sample
cd new-sample && cdk init app --language python
./env/bin/pip install -r requirements.txt
```

### Generate CloudFormation Template

```bash
cdk synth
```

### Deploy Project

```bash
cdk deploy
```
