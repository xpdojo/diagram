from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Redshift
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Oracle
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Datadog
from diagrams.onprem.network import Apache

graph_attr = {
    "fontsize": "45",
    # "bgcolor": "transparent",
    "bgcolor": "#FFFFFF",
    "size": "5,10!",  # width,heigth
}

node_attr = {
    "fontsize": "16",
    # "orientation": "landscape",
}

with Diagram(
        name="Hell",
        show=False,
        graph_attr=graph_attr,
        node_attr=node_attr):
    proxy = Apache("Web Proxy")

    with Cluster("Services"):
        svc1 = [
            Server("web1"),
            Server("web2"),
        ]
        svc2 = [
            Server("web3"),
        ]
        session = Redis("session")
        svc1 >> Edge(color="brown") >> session
        svc2 >> Edge(color="brown") >> session

    with Cluster("Database"):
        db = Oracle("users")
        db - Edge(color="brown", style="dotted") << Edge(label="collect")
        svc1 >> Edge(color="black") >> db
        svc2 >> Edge(color="black") >> db

    db << Datadog("monitoring")

    with Cluster("Logging"):
        aggregator = Fluentd("collect")
        aggregator >> Edge(label="parse") >> Lambda("function") >> Edge(color="black", style="bold") >> Redshift(
            "Datalake")

        proxy >> Edge(color="darkgreen") << svc1 >> Edge(color="darkorange") >> aggregator
        proxy >> Edge(color="darkgreen") << svc2 >> Edge(color="darkorange") >> aggregator
