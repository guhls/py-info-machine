from pydoc import cli
from minio import Minio
from minio.error import S3Error

import pandas as pd


def push_to_minio(df):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        '172.31.114.213:9000',
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Make 'asiatrip' bucket if not exist.
    found = client.bucket_exists("demo-infos")
    if not found:
        client.make_bucket("demo-infos")
    else:
        print("Bucket 'demo-infos' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    # client.fput_object(
    #     "demo-infos", "gustavopc-infosys.csv", "gustavopc-infosys.csv",
    # )
    # print(
    #     "gustavopc-infosys.csv is successfully uploaded as "
    #     "object 'gustavopc-infosys.csv' to bucket 'demo-infos'."
    # )

    df.to_parquet("archive/test.parquet")

    client.fput_object('demo-infos', 'machine-infos/test.parquet', 'archive/test.parquet')


if __name__ == "__main__":
    try:
        push_to_minio()
    except S3Error as exc:
        print("error occurred.", exc)
