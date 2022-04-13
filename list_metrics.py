#!/usr/bin/env python3
import boto3

boto3.setup_default_session(profile_name="<profile>")

client = boto3.client('cloudwatch')

params = {
        'Namespace':"<custom_namespace>"

        }

metric_data = []
response = client.list_metrics(**params)
metric_data.extend(response["Metrics"])


while (response.get('NextToken')):
    params['NextToken']= response['NextToken']
    response = client.list_metrics(**params)
    metric_data.extend(response["Metrics"])

metric_names = {}
for metric in metric_data:
    if metric["MetricName"] not in metric_names:
        metric_names[metric["MetricName"]]= metric["Dimensions"]
    else:
        dimensions = metric_names[metric["MetricName"]]
        dimensions.extend(metric["Dimensions"])
        metric_names[metric["MetricName"]]=dimensions


with open("result.txt","w") as f:
    for i in metric_names:
        f.write(i+"\n")

with open("result_detail.txt","w") as f:
    total = 0
    for i in metric_names:
        f.write("Metric:" + i+""+"dimensions :"+str(len(metric_names[i]))+"\n")
        total = total + len(metric_names[i])
        for data in metric_names[i]:
            f.write("\t"+ str(data))
        f.write("\n")
    f.write("total dimensions: "+ str(total))
