from config.log import default_logger
from graph.build_graph import build_graph
from graph.state import State
from loader.connect import connect_db


# from utils import get_graph_image


def main():
    connect_db()
    initial_state: State = State(
        sites=[],
        parallel_result={},
    )
    graph = build_graph(initial_state)
    #     get_graph_image(graph)
    return graph.invoke(initial_state)


if __name__ == "__main__":
    result = main()
    default_logger.info(result)
# FIXME 자세한 로그를 보기 위해 우선 주석
#     try:
#         result = main()
#         logger.info(result)
#         exit(0)  # 성공적으로 종료
#     except Exception as e:
#         logger.error(f"An error occurred: {e}")
#         exit(1)  # 오류로 인한 종료
