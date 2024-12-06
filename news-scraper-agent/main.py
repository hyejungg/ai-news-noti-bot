from graph.build_graph import build_graph
from loader.connect import connect_db


def main() -> None:
    connect_db()
    from graph.state import State

    initial_state: State = State(
        sites=[],
        parallel_result={},
    )
    graph = build_graph(initial_state)
    #     get_graph_image(graph)
    graph.invoke(initial_state)


def lambda_handler(event, context) -> None:
    main()


if __name__ == "__main__":
    main()
