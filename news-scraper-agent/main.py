from graph import build_graph
from loader.connect import connect_db
# from utils import get_graph_image

def main():
    connect_db()
    graph = build_graph()
    initial_state = {
        "sites": [],
        "out_values": [],
        "prompts": [],
        "crawling_results": [],
        "filtering_result": [],
        "send_messages": []
    }
#     get_graph_image(graph)
    result = graph.invoke(initial_state)
    return result

if __name__ == "__main__":
    result = main()
    print(result)
# FIXME 자세한 로그를 보기 위해 우선 주석
#     try:
#         result = main()
#         print(result)
#         exit(0)  # 성공적으로 종료
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         exit(1)  # 오류로 인한 종료
