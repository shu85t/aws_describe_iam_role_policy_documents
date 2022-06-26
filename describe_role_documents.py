import os
import sys
from typing import List
from enum import Enum
from dataclasses import dataclass
import json
import boto3

USAGE = f"""
**USAGE**
python {os.path.basename(__file__)} {{role_name}}
"""


class PolicyType(Enum):
    ATTACHED = 1
    INLINE = 2


@dataclass
class PolicyDocument:
    name: str
    body: str
    type: PolicyType


iam = boto3.client('iam')


def main(role_name: str):
    documents: List[PolicyDocument] = []

    # get attached policy documents
    attached_policy_arns = get_attached_policy_arns(role_name)
    for policy_arn in attached_policy_arns:
        attached_document = get_policy_document(policy_arn)
        documents.append(attached_document)

    # get inline policy documents
    inline_policy_names = get_inline_policy_names(role_name)
    for inline_policy_name in inline_policy_names:
        inline_document = get_inline_policy_document(role_name, inline_policy_name)
        documents.append(inline_document)

    # output
    for d in documents:
        print(f"---")
        print(f"{d.name} ({d.type.name})")
        print(f"{json.dumps(d.body, indent=2)}")


def get_attached_policy_arns(role_name: str) -> List[str]:
    paginator = iam.get_paginator('list_attached_role_policies')
    arns: List[str] = []
    for policies in paginator.paginate(RoleName=role_name):
        for p in policies["AttachedPolicies"]:
            arns.append(p["PolicyArn"])
    return arns


def get_policy_document(arn: str) -> PolicyDocument:
    policy = iam.get_policy(PolicyArn=arn)["Policy"]
    policy_version = iam.get_policy_version(
        PolicyArn=policy["Arn"], VersionId=policy["DefaultVersionId"])["PolicyVersion"]
    return PolicyDocument(
        name=policy["Arn"],
        body=policy_version["Document"],
        type=PolicyType.ATTACHED
    )


def get_inline_policy_names(role_name: str) -> List[str]:
    paginator = iam.get_paginator('list_role_policies')
    policies = paginator.paginate(RoleName=role_name)
    names: List[str] = []
    for policy in policies:
        names.extend(policy["PolicyNames"])
    return names


def get_inline_policy_document(role_name: str, inline_policy_name: str) -> PolicyDocument:
    policy = iam.get_role_policy(
        RoleName=role_name,
        PolicyName=inline_policy_name
    )
    return PolicyDocument(
        name=policy["PolicyName"],
        body=policy["PolicyDocument"],
        type=PolicyType.INLINE
    )


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        main(role_name=args[1])
        sys.exit(0)
    else:
        print("incorrect argument")
        print(USAGE)
        sys.exit(1)
