# AWS Describe IAM role policy documents

Python Script that describes the following Policy documents for the specified IAM role.

- Attached AWS managed policies
- Attached Customer managed policies
- Inline policies

## Requirements

- \>Python3.7
- boto3
- AWS Permissions
    - iam:ListAttachedRolePolicies
    - iam:GetPolicy
    - iam:GetPolicyVersion
    - iam:ListRolePolicies
    - iam:GetRolePolicy

## Usage

```shell
python3 describe_role_documents.py {role_name}
```

### output sample

```json
---
arn:aws:iam::aws:policy/IAMFullAccess (ATTACHED)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:*",
        "organizations:DescribeAccount",
        "organizations:DescribeOrganization",
        "organizations:DescribeOrganizationalUnit",
        "organizations:DescribePolicy",
        "organizations:ListChildren",
        "organizations:ListParents",
        "organizations:ListPoliciesForTarget",
        "organizations:ListRoots",
        "organizations:ListPolicies",
        "organizations:ListTargetsForPolicy"
      ],
      "Resource": "*"
    }
  ]
}
---
arn:aws:iam::111111111111:policy/custom_policy_xxx (ATTACHED)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "*"
    }
  ]
}
---
inline_policy_test (INLINE)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "lambda:ListProvisionedConcurrencyConfigs",
        "lambda:ListFunctionEventInvokeConfigs",
        "lambda:ListFunctions",
        "lambda:ListFunctionsByCodeSigningConfig",
        "lambda:ListVersionsByFunction",
        "lambda:ListAliases",
        "lambda:ListEventSourceMappings",
        "lambda:ListFunctionUrlConfigs",
        "lambda:ListLayerVersions",
        "lambda:ListLayers",
        "lambda:ListCodeSigningConfigs"
      ],
      "Resource": "*"
    }
  ]
}
---
inline_policy_s3test (INLINE)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::test-bucket-111111111111/*"
    }
  ]
}

```
