import dlt
from dlt.sources.rest_api import rest_api_source
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
import os

os.environ["DESTINATION__POSTGRES__CREDENTIALS"] = os.environ["DATABASE_URL"]

def load_customers():
    
    pipeline = dlt.pipeline(
        pipeline_name="customers_api_pipeline",
        destination="postgres",
        dataset_name="public",
    )

    customers_source = rest_api_source(
        {
            "client": {
                "base_url": "http://mock-server:5000/api",
            },
            "resource_defaults": {
                "endpoint": {
                    "params": {
                        "limit": 5,
                        "page": 1,
                    },
                "data_selector": "data",
                },
            },
            "resources": [{
                "name": "customers",
                "endpoint": {
                    "path": "customers", 
                    "paginator": PageNumberPaginator(
                        base_page=1,
                        page_param="page",
                        total_path=None, # expects total no of pages. Set to none as mock-server provides records.
                        stop_after_empty_page=True,
                    ),
                },
                "primary_key": "customer_id",
                "write_disposition": {"disposition": "merge", "strategy": "upsert"},
            }],
        }
    )

    load_info = pipeline.run(customers_source)
    print(load_info)
    return pipeline.last_trace.last_normalize_info.row_counts["customers"]